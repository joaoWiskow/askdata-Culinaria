import os
import logging
from functools import lru_cache
from typing import List, Dict, Any

import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception,
    before_sleep_log,
)

# pip install tenacity

load_dotenv()
logger = logging.getLogger("rag")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env!")


# Modelos utilizados
EMBEDDING_MODEL = "gemini-embedding-001"

# Ordem de tentativa: principal -> alternativas (confirme os nomes na sua conta)
MODELOS_GERACAO = [
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

# Erros transitórios que valem a pena repetir
CODIGOS_RETRY = {429, 500, 502, 503, 504}


def _e_transitorio(exc: BaseException) -> bool:
    """True para erros de sobrecarga/instabilidade (503, 429, 5xx)."""
    if isinstance(exc, errors.APIError):
        return getattr(exc, "code", None) in CODIGOS_RETRY
    return isinstance(exc, (ConnectionError, TimeoutError))


def com_retry(max_tentativas: int):
    """Retry com backoff exponencial + jitter apenas para erros transitórios."""
    return retry(
        retry=retry_if_exception(_e_transitorio),
        wait=wait_random_exponential(multiplier=1, max=30),
        stop=stop_after_attempt(max_tentativas),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


class RAGEngine:
    def __init__(
        self,
        path_db: str = "./chroma_db",
        collection_name: str = "askdata_knowledge",
    ):
        """Inicializa a conexão com o ChromaDB e o cliente Gemini."""

        self.client = genai.Client(api_key=api_key)

        self.chroma_client = chromadb.PersistentClient(path=path_db)

        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    # ------------------------------------------------------------------
    # Embedding (com cache + retry)
    # ------------------------------------------------------------------
    @lru_cache(maxsize=512)
    def _gerar_embedding_cached(self, texto: str) -> tuple:
        """Cache em memória: perguntas repetidas não chamam a API de novo."""

        @com_retry(max_tentativas=5)
        def _chamar():
            res = self.client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=texto,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
            )
            return res.embeddings[0].values

        return tuple(_chamar())  # tuple, pois é imutável/cacheável

    def _gerar_embedding(self, texto: str) -> List[float]:
        return list(self._gerar_embedding_cached(texto.strip()))

    # ------------------------------------------------------------------
    # Recuperação
    # ------------------------------------------------------------------
    def recuperar_contexto(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Busca no ChromaDB os chunks mais relevantes para a pergunta."""

        vetor_query = self._gerar_embedding(query)

        resultados = self.collection.query(
            query_embeddings=[vetor_query],
            n_results=top_k,
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
                resultados["distances"][0],
            ):
                meta = meta or {}
                chunks_recuperados.append({
                    "texto": doc,
                    "arquivo": meta.get("arquivo", "desconhecido"),
                    "pagina": meta.get("pagina", 1),
                    "distancia": dist,
                    "similaridade": round(1.0 - dist, 4),
                })

        return chunks_recuperados

    # ------------------------------------------------------------------
    # Geração (retry por modelo + fallback entre modelos)
    # ------------------------------------------------------------------
    def _gerar_resposta(self, prompt: str, system_instruction: str) -> str:
        """
        Tenta cada modelo da lista. Em cada um, faz poucos retries;
        se continuar com 503/429, passa para o próximo modelo.
        """
        ultimo_erro = None

        for modelo in MODELOS_GERACAO:

            @com_retry(max_tentativas=3)
            def _chamar():
                return self.client.models.generate_content(
                    model=modelo,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.1,
                    ),
                )

            try:
                response = _chamar()
                if modelo != MODELOS_GERACAO[0]:
                    logger.warning("Resposta gerada via fallback: %s", modelo)
                return response.text.strip()

            except errors.APIError as e:
                ultimo_erro = e
                logger.warning(
                    "Modelo %s falhou (%s). Tentando próximo...",
                    modelo, getattr(e, "code", "?"),
                )
                # 404 (modelo inexistente) e 5xx/429 -> tenta o próximo.
                # 400/401/403 são erros de requisição/chave: não adianta trocar.
                if getattr(e, "code", None) in (400, 401, 403):
                    raise

        raise RuntimeError(
            f"Todos os modelos de geração falharam: {ultimo_erro}"
        )

    # ------------------------------------------------------------------
    # Pipeline completo
    # ------------------------------------------------------------------
    def responder_pergunta(
        self,
        query: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Executa o pipeline RAG completo."""

        # 1. Recuperar contexto
        try:
            chunks = self.recuperar_contexto(query, top_k=top_k)
        except errors.APIError as e:
            logger.error("Falha ao gerar embedding: %s", e)
            return {
                "resposta": (
                    "O serviço está com alta demanda no momento. "
                    "Tente novamente em alguns instantes."
                ),
                "fontes": [],
                "degradado": True,
            }

        if not chunks:
            return {
                "resposta": (
                    "Nenhum documento encontrado na base de "
                    "conhecimento. Por favor, processe arquivos primeiro."
                ),
                "fontes": [],
            }

        # 2. Formatar o contexto
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
profissional e EXCLUSIVAMENTE baseada nos trechos de documentos
fornecidos no contexto.

REGRAS OBRIGATÓRIAS:

1. Responda apenas com informações presentes no
   <contexto_recuperado>.

2. Se a resposta NÃO estiver no contexto fornecido,
   NÃO tente inventar ou utilizar conhecimentos externos.

3. Quando não houver informação suficiente no contexto,
   responda exatamente:

   "Desculpe, não encontrei informações sobre isso nos
   documentos fornecidos."

4. Ao responder, cite o nome do arquivo e a página de onde
   a informação foi extraída.

5. Mantenha um tom profissional, direto e em bom português.

6. Não invente informações, fontes, páginas ou documentos.
7. Diga sempre "Olá, aluno!" antes da resposta.
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

        # 5. Geração com retry + fallback; se tudo falhar, degrada com elegância
        try:
            texto = self._gerar_resposta(prompt_final, system_instruction)
            return {"resposta": texto, "fontes": chunks}

        except Exception as e:
            logger.error("Geração indisponível: %s", e)
            trechos = "\n\n".join(
                f"[{c['arquivo']} - pág. {c['pagina']}]\n{c['texto']}"
                for c in chunks[:3]
            )
            return {
                "resposta": (
                    "O modelo de linguagem está com alta demanda agora, "
                    "então não consegui redigir a resposta. Estes são os "
                    "trechos mais relevantes encontrados nos documentos:\n\n"
                    + trechos
                ),
                "fontes": chunks,
                "degradado": True,
            }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

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

        resultado = engine.responder_pergunta(pergunta, top_k=5)

        print("\nRESPOSTA DO ASSISTENTE:")
        print(resultado["resposta"])

        print("\nFONTES UTILIZADAS:")
        for fonte in resultado["fontes"]:
            print(
                f"  - {fonte['arquivo']} "
                f"(Página {fonte['pagina']}) "
                f"- Similaridade: {fonte['similaridade']:.2%}"
            )