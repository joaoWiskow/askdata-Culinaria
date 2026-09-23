import os
import glob
import time
import random
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
# FUNÇÃO DE CHAMADA SEGURA COM RETRY DINÂMICO E BACKOFF
# ============================================================

def gerar_embeddings_com_retry(client, model, contents, config, max_tentativas=5):
    """
    Tenta gerar embeddings aplicando backoff exponencial e leitura 
    dinâmica de tempo de espera caso receba erro 429 (Resource Exhausted).
    """
    tentativa = 0
    tempo_espera = 5  # Tempo base inicial em segundos

    while tentativa < max_tentativas:
        try:
            res = client.models.embed_content(
                model=model,
                contents=contents,
                config=config
            )
            return res  # Sucesso! Retorna a resposta

        except Exception as e:
            erro_str = str(e)
            tentativa += 1

            # Verifica se é um erro de limite excedido (429 ou RESOURCE_EXHAUSTED)
            if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                if tentativa >= max_tentativas:
                    print(f"  ❌ Erro 429 persistente após {max_tentativas} tentativas. Abortando.")
                    raise

                # Tenta extrair de forma dinâmica se houver indicação de tempo no erro (ex: headers ou mensagem)
                # O SDK do Google as vezes traz a dica no texto do erro. Caso contrário, usamos backoff exponencial.
                delay_dinamico = None
                if "retry-after" in erro_str.lower():
                    try:
                        # Extração simples caso venha estruturado no texto do erro
                        import re
                        match = re.search(r'retry-after[:\s]+(\d+)', erro_str, re.IGNORECASE)
                        if match:
                            delay_dinamico = int(match.group(1))
                    except:
                        pass

                # Se encontrou um tempo dinâmico na mensagem, usa ele. Senão, dobra o tempo anterior (Exponencial) + Jitter aleatório
                if delay_dinamico:
                    tempo_espera = delay_dinamico
                else:
                    # Backoff exponencial: 5s, 10s, 20s, 40s... + um pequeno fator aleatório (jitter)
                    tempo_espera = (2 ** (tentativa - 1)) * 5 + random.uniform(1, 3)

                print(f"  ⚠️ Limite atingido (429) [Tentativa {tentativa}/{max_tentativas}].")
                print(f"  ⏳ Aguardando {tempo_espera:.1f} segundos antes de tentar novamente...")
                
                time.sleep(tempo_espera)
            else:
                # Se for outro tipo de erro (que não seja 429), propaga imediatamente
                raise


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
        # GERAÇÃO DOS EMBEDDINGS (Com tratamento de retry inteligente)
        # ----------------------------------------------------
        res = gerar_embeddings_com_retry(
            client=client,
            model=EMBEDDING_MODEL,
            contents=textos,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            )
        )

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
        
        # Opcional: Uma pausa sutil e fixa de 1 a 2 segundos entre lotes 
        # para ajudar a manter o script dentro do teto do Free Tier (RPM).
        time.sleep(2)

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