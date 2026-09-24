import os
from typing import List, Dict, Any

import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env!")


# Modelos utilizados
EMBEDDING_MODEL = "gemini-embedding-001"
MODELO_FLASH = "gemini-3.1-flash-lite"


class RAGEngine:
    def __init__(
        self,
        path_db: str = "./chroma_db",
        collection_name: str = "askdata_knowledge"
    ):
        """Inicializa a conexão com o ChromaDB e o cliente Gemini."""

        self.client = genai.Client(api_key=api_key)

        self.chroma_client = chromadb.PersistentClient(
            path=path_db
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def _gerar_embedding(self, texto: str) -> List[float]:
        """Gera o embedding da pergunta do usuário."""

        res = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texto,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY"
            )
        )

        return res.embeddings[0].values

    def recuperar_contexto(
        self,
        query: str,
        top_k: int = 5,
        top_p: int = 5,
    ) -> List[Dict[str, Any]]:
        """Busca no ChromaDB os chunks mais relevantes para a pergunta."""

        vetor_query = self._gerar_embedding(query)

        resultados = self.collection.query(
            query_embeddings=[vetor_query],
            n_results=top_k
        )

        chunks_recuperados = []

        if (
            resultados
            and resultados.get("documents")
            and resultados["documents"][0]
        ):
            for doc, meta, dist in zip(
                resultados["documents"][0],
                resultados["metadatas"][0],
                resultados["distances"][0]
            ):
                meta = meta or {}

                chunks_recuperados.append({
                    "texto": doc,
                    "arquivo": meta.get("arquivo", "desconhecido"),
                    "pagina": meta.get("pagina", 1),
                    "distancia": dist,
                    "similaridade": round(1.0 - dist, 4)
                })

        return chunks_recuperados

    def responder_pergunta(
        self,
        query: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """Executa o pipeline RAG completo."""

        # 1. Recuperar contexto do banco vetorial
        chunks = self.recuperar_contexto(
            query,
            top_k=top_k
        )

        if not chunks:
            return {
                "resposta": (
                    "Nenhum documento encontrado na base de "
                    "conhecimento. Por favor, processe arquivos primeiro."
                ),
                "fontes": []
            }

        # 2. Formatar o contexto recuperado
        contexto_formatado = ""

        for idx, chunk in enumerate(chunks, 1):
            contexto_formatado += (
                f"\n--- [FONTE {idx} | "
                f"Arquivo: {chunk['arquivo']} | "
                f"Página: {chunk['pagina']}] ---\n"
            )

            contexto_formatado += chunk["texto"] + "\n"

        # 3. Instruções do sistema
        system_instruction = """
Você é o 'AskData', um assistente corporativo de inteligência
artificial da DataLakers.

Sua missão é responder à pergunta do usuário de forma clara,
profissional e baseada nos trechos de documentos
fornecidos no contexto.

REGRAS OBRIGATÓRIAS:

1. Responda apenas com informações presentes no
   <contexto_recuperado>.

2. Se a resposta NÃO estiver no contexto fornecido,
   então utilize conhecimentos externos e obedeça o item tres.

3. Quando não houver informação suficiente no contexto fornecido em <contexto_recuperado>,
   responda exatamente:

   "Desculpe, não encontrei informações sobre isso nos
   documentos fornecidos. mas aqui esta minha tentativa: 
   
   [TENTATIVA]" 

   com tentativa sendo a tentativa de responder a pergunta utilizando conhecimentos externos

4. Ao responder, cite o nome do arquivo e a página de onde
   a informação foi extraída.

5. Mantenha um tom profissional, direto e em bom português.

6. Não invente informações, fontes, páginas ou documentos.
"""

        # 4. Prompt final
        prompt_final = f"""
<contexto_recuperado>
{contexto_formatado}
</contexto_recuperado>

<pergunta_do_usuario>
{query}
</pergunta_do_usuario>
"""

        # 5. Geração da resposta
        response = self.client.models.generate_content(
            model=MODELO_FLASH,
            contents=prompt_final,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1
            )
        )

        return {
            "resposta": response.text.strip(),
            "fontes": chunks
        }


if __name__ == "__main__":

    engine = RAGEngine()

    print("=" * 60)
    print("TESTE DO MOTOR RAG (Terminal)")
    print("=" * 60)

    while True:

        pergunta = input(
            "\nFaça uma pergunta sobre seus documentos "
            "('sair' para encerrar): "
        ).strip()

        if pergunta.lower() in ["sair", "exit"]:
            break

        if not pergunta:
            continue

        resultado = engine.responder_pergunta(
            pergunta,
            top_k=5
        )

        print("\nRESPOSTA DO ASSISTENTE:")
        print(resultado["resposta"])

        print("\nFONTES UTILIZADAS:")

        for fonte in resultado["fontes"]:
            print(
                f"  - {fonte['arquivo']} "
                f"(Página {fonte['pagina']}) "
                f"- Similaridade: "
                f"{fonte['similaridade']:.2%}"
            )