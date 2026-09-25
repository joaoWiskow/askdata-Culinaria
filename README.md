# askdata-NAVI

**AskData** — assistente de documentação técnica com RAG (Retrieval-Augmented Generation), citação de fontes e guardrails anti-alucinação.

Destinado ao trabalho produzido ao longo das Sprints 1 a 3.

Piloto A: Enzo
Piloto B: João
Piloto C: Matheus

## Sobre o projeto

O AskData responde perguntas sobre uma base de documentos técnicos (PDFs e Markdown), sempre citando o arquivo e a página de origem da informação. Quando a resposta não está na base, o sistema recusa explicitamente ao invés de inventar conteúdo.

Pipeline completo:

1. **Ingestão** (`src/ingestion.py`) — extração de texto de PDFs/Markdown página a página, chunking com overlap e geração de embeddings via `gemini-embedding-001`, indexados no ChromaDB com retry exponencial contra rate limit.
2. **Motor RAG** (`src/rag_engine.py`) — busca por similaridade no ChromaDB, prompt com regras de prioridade (guardrails), cadeia de fallback entre modelos Gemini, cache de embeddings e degradação graciosa em caso de indisponibilidade.
3. **Front-end** (`src/app.py`) — interface em Streamlit com tema customizado, chat com histórico, exibição de fontes/similaridade e exportação da conversa.
4. **Avaliação** (`src/avaliar_rag.py`) — benchmark automatizado com perguntas dentro e fora do escopo da base, medindo taxa de recusa honesta e alucinação.

## Estrutura do projeto

```text
askdata-NAVI/
├── data/                  # PDFs/Markdown que compõem a base de conhecimento
├── src/
│   ├── ingestion.py       # Extração, chunking e indexação no ChromaDB
│   ├── rag_engine.py      # Motor RAG: recuperação, prompt blindado, geração
│   ├── app.py             # Interface Streamlit
│   ├── avaliar_rag.py     # Benchmark anti-alucinação
│   └── test_chroma_setup.py
├── check_setup.py         # Smoke test do ambiente (imports, chave de API, dados)
├── requirements.txt
└── .env.example
```

## Dependências

O projeto utiliza Python 3 e as seguintes bibliotecas:

```txt
google-genai
chromadb
pypdf
python-dotenv
tenacity
streamlit
```

### Instalação

Recomenda-se utilizar um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows:

```powershell
.venv\Scripts\activate
```

Instale as dependências com:

```bash
pip install -r requirements.txt
```

Ou diretamente:

```bash
pip install google-genai chromadb pypdf python-dotenv tenacity streamlit
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
```

O arquivo `.env` não deve ser versionado no Git.

## Como rodar

1. **Verifique o ambiente** (opcional, mas recomendado):

   ```bash
   python check_setup.py
   ```

2. **Indexe os documentos** (necessário na primeira vez e sempre que a pasta `data/` mudar):

   ```bash
   python src/ingestion.py
   ```

   Isso cria a base vetorial persistente em `./chroma_db`.

3. **Suba a interface**:

   ```bash
   streamlit run src/app.py
   ```

4. **(Opcional) Rode o benchmark anti-alucinação**:

   ```bash
   python src/avaliar_rag.py
   ```

## Principais decisões de engenharia

- **Prompt blindado em camadas**: recusa explícita quando não há informação suficiente no contexto, detecção de tentativa de jailbreak e checagem de aderência temática entre pergunta e fonte recuperada.
- **Resiliência**: cadeia de fallback entre modelos Gemini (`gemini-3.8-flash` → `gemini-3.1-flash-lite`) com retry exponencial via `tenacity`, e resposta degradada (trechos brutos) como último recurso caso toda a geração falhe.
- **Cache de embeddings**: perguntas repetidas não geram novas chamadas à API, reduzindo custo e latência.
- **Citação de fontes**: cada resposta é rastreável até o arquivo e a página exata do documento original.
