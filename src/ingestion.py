import os
import glob
import time
from pathlib import Path

from pypdf import PdfReader
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# CONFIGURAÇÃO
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env!")

client = genai.Client(api_key=api_key)

# Modelo de embeddings do Google
EMBEDDING_MODEL = "gemini-embedding-001"

# Quantidade de chunks enviados por requisição
BATCH_SIZE = 20


# ============================================================
# EXTRAÇÃO DE PDF
# ============================================================

def extrair_texto_pdf(caminho_pdf: str) -> list[dict]:
    """Lê um arquivo PDF e extrai o texto página por página com metadados."""

    reader = PdfReader(caminho_pdf)

    paginas = []

    nome_arquivo = Path(caminho_pdf).name

    for idx, pagina in enumerate(reader.pages):

        texto = pagina.extract_text() or ""

        if texto.strip():
            paginas.append({
                "texto": texto.strip(),
                "arquivo": nome_arquivo,
                "pagina": idx + 1
            })

    return paginas


# ============================================================
# EXTRAÇÃO DE MARKDOWN
# ============================================================

def extrair_texto_markdown(caminho_md: str) -> list[dict]:
    """Lê um arquivo Markdown e extrai o texto com metadados."""

    nome_arquivo = Path(caminho_md).name

    with open(caminho_md, "r", encoding="utf-8") as f:
        texto = f.read().strip()

    if texto:
        return [{
            "texto": texto,
            "arquivo": nome_arquivo,
            "pagina": 1
        }]

    return []


# ============================================================
# CHUNKING
# ============================================================

def criar_chunks(
    documentos_paginas: list[dict],
    chunk_size: int = 700,
    chunk_overlap: int = 100
) -> list[dict]:
    """
    Divide os textos em blocos com sobreposição (overlap)
    para preservar contexto entre os chunks.
    """

    chunks = []

    for item in documentos_paginas:

        texto = item["texto"]

        inicio = 0
        chunk_idx = 1

        while inicio < len(texto):

            fim = inicio + chunk_size

            trecho = texto[inicio:fim]

            chunk_id = (
                f"{item['arquivo']}"
                f"_p{item['pagina']}"
                f"_c{chunk_idx}"
            )

            chunks.append({
                "id": chunk_id,
                "texto": trecho,
                "arquivo": item["arquivo"],
                "pagina": item["pagina"],
                "chunk_idx": chunk_idx
            })

            inicio += chunk_size - chunk_overlap
            chunk_idx += 1

    return chunks


# ============================================================
# INDEXAÇÃO NO CHROMADB
# ============================================================

def indexar_no_chromadb(
    chunks: list[dict],
    path_db: str = "./chroma_db",
    collection_name: str = "askdata_knowledge",
    batch_size: int = BATCH_SIZE
):
    """
    Gera embeddings em batches e salva os chunks no ChromaDB.

    Cada batch gera vários embeddings em uma única requisição
    para a API do Gemini.
    """

    chroma_client = chromadb.PersistentClient(
        path=path_db
    )

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={
            "hnsw:space": "cosine"
        }
    )

    total = len(chunks)

    print(f"Total de chunks a serem indexados: {total}")
    print(f"Tamanho do batch: {batch_size}")

    # Percorre os chunks em lotes
    for inicio in range(0, total, batch_size):

        fim = min(
            inicio + batch_size,
            total
        )

        batch = chunks[inicio:fim]

        textos = [
            ch["texto"]
            for ch in batch
        ]

        print(
            f"  -> Processando chunks "
            f"{inicio + 1}-{fim}/{total}..."
        )

        # ----------------------------------------------------
        # GERAÇÃO DOS EMBEDDINGS
        # ----------------------------------------------------

        try:

            res = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=textos,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT"
                )
            )

        except Exception as e:

            # Tratamento específico para limite de requisições
            if "429" in str(e):

                print(
                    "  !! Limite da API atingido."
                )

                print(
                    "  !! Aguardando 60 segundos "
                    "antes de tentar novamente..."
                )

                time.sleep(60)

                # Tenta novamente o mesmo batch
                res = client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=textos,
                    config=types.EmbedContentConfig(
                        task_type="RETRIEVAL_DOCUMENT"
                    )
                )

            else:
                raise

        # ----------------------------------------------------
        # EXTRAI OS VETORES
        # ----------------------------------------------------

        embeddings = [
            embedding.values
            for embedding in res.embeddings
        ]

        # ----------------------------------------------------
        # PREPARA DADOS PARA O CHROMADB
        # ----------------------------------------------------

        ids = [
            ch["id"]
            for ch in batch
        ]

        documentos = [
            ch["texto"]
            for ch in batch
        ]

        metadatas = [
            {
                "arquivo": ch["arquivo"],
                "pagina": ch["pagina"],
                "chunk_idx": ch["chunk_idx"]
            }
            for ch in batch
        ]

        # ----------------------------------------------------
        # SALVA NO CHROMADB
        # ----------------------------------------------------

        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documentos,
            metadatas=metadatas
        )

        print(
            f"  -> Batch concluído: "
            f"{fim}/{total} chunks"
        )

    print()
    print(
        "Ingestão concluída com sucesso "
        f"no ChromaDB ({path_db})!"
    )

    print(
        f"Total salvo: {collection.count()} chunks."
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    pasta_dados = "./data"

    todos_documentos = []

    # --------------------------------------------------------
    # 1. CARREGAR PDFs
    # --------------------------------------------------------

    for pdf_path in glob.glob(
        f"{pasta_dados}/*.pdf"
    ):

        print(
            f"Processando PDF: {pdf_path}"
        )

        todos_documentos.extend(
            extrair_texto_pdf(pdf_path)
        )

    # --------------------------------------------------------
    # 2. CARREGAR MARKDOWNS
    # --------------------------------------------------------

    for md_path in glob.glob(
        f"{pasta_dados}/*.md"
    ):

        print(
            f"Processando Markdown: {md_path}"
        )

        todos_documentos.extend(
            extrair_texto_markdown(md_path)
        )

    # --------------------------------------------------------
    # VERIFICAR DOCUMENTOS
    # --------------------------------------------------------

    if not todos_documentos:

        print(
            "Nenhum arquivo PDF ou Markdown "
            "encontrado em ./data!"
        )

        print(
            "Adicione arquivos na pasta ./data "
            "para testar."
        )

    else:

        # ----------------------------------------------------
        # 3. GERAR CHUNKS
        # ----------------------------------------------------

        lista_chunks = criar_chunks(
            todos_documentos,
            chunk_size=700,
            chunk_overlap=100
        )

        # ----------------------------------------------------
        # 4. INDEXAR NO CHROMADB
        # ----------------------------------------------------

        indexar_no_chromadb(
            lista_chunks,
            batch_size=BATCH_SIZE
        )