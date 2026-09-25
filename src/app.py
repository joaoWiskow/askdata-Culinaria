import streamlit as st
import os
from rag_engine import RAGEngine
import json
import time

# Configuracao da pagina
st.set_page_config(
    page_title="AskData", layout="wide"
)

# --- CSS GLOBAL: tema high-tech azul aplicado direto pelo app (sem config.toml) ---
st.markdown(
    """
    <style>
    :root {
        --azul-fundo: #0E1420;
        --azul-fundo-2: #161D2E;
        --azul-borda: #1E2A42;
        --azul-primario: #00C2FF;
        --verde-acento: #2ECC71;
    }

    /* Fundo principal */
    .stApp {
        background-color: var(--azul-fundo);
        color: #E6EDF3;
    }

    /* Header superior (barra com "Deploy") */
    header[data-testid="stHeader"] {
        background-color: var(--azul-fundo) !important;
    }

    /* Container fixo inferior (onde fica o campo de input do chat) */
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stBottom"] {
        background-color: var(--azul-fundo) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--azul-fundo-2);
        border-right: 1px solid var(--azul-borda);
    }

    /* Titulos */
    h1, h2, h3 { color: var(--azul-primario); }

    /* Texto padrao e captions */
    p, span, label, .stCaption, div[data-testid="stCaptionContainer"] {
        color: #C9D6E3 !important;
    }

    /* Botoes */
    .stButton button {
        background-color: var(--azul-fundo-2);
        color: var(--azul-primario);
        border: 1px solid var(--azul-borda);
        border-radius: 8px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton button:hover {
        background-color: var(--azul-fundo-2);
        color: var(--azul-primario);
        border: 1px solid var(--azul-primario);
        box-shadow: 0 0 6px rgba(0, 194, 255, 0.5);
    }

    /* Slider (Top-K) em azul marinho */
    div[data-testid="stSlider"] [data-baseweb="slider"] > div {
        background: rgba(10, 31, 68, 0.25) !important;
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] > div:nth-of-type(2) {
        background: #0A1F44 !important;
    }
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #0A1F44 !important;
        border-color: #0A1F44 !important;
        box-shadow: none !important;
    }
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #4C7CD6 !important;
    }
    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
        color: #C9D6E3 !important;
    }

    /* Baloes de chat */
    .stChatMessage {
        background-color: var(--azul-fundo-2);
        border-radius: 12px;
        border: 1px solid var(--azul-borda);
    }
    /* Avatar do assistente no chat (troca o laranja padrão por azul marinho) */
    div[data-testid="stChatMessageAvatarAssistant"] {
        background-color: #0A1F44 !important;
        color: #FFFFFF !important;
    }

    /* Caso queira padronizar também o avatar do usuário */
    div[data-testid="stChatMessageAvatarUser"] {
        background-color: #0A1F44 !important;
        color: #FFFFFF !important;
    }

    /* Expander (Fontes e Chunks) */
    div[data-testid="stExpander"] {
        background-color: var(--azul-fundo-2);
        border: 1px solid var(--azul-borda);
        border-radius: 10px;
    }

    /* Barra de progresso (similaridade) */
    div[data-testid="stProgress"] > div > div {
        background-color: var(--azul-primario);
    }

    /* Caixa de input do chat */
    div[data-testid="stChatInput"] {
        background-color: var(--azul-fundo-2);
        border: 1px solid var(--azul-borda);
        border-radius: 10px;
    }

    /* Links discretos (ex: DataLakers, Navi Hub) */
    a.link-discreto {
        color: inherit !important;
        text-decoration: none !important;
        border-bottom: 1px dotted rgba(0, 194, 255, 0.4);
        transition: color 0.2s ease, border-color 0.2s ease;
    }
    a.link-discreto:hover {
        color: var(--azul-primario) !important;
        border-bottom: 1px solid var(--azul-primario);
    }

    /* Popover (menu "+" de opções) */
    div[data-testid="stPopoverBody"] {
        background-color: var(--azul-fundo-2) !important;
        border: 1px solid var(--azul-borda) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stPopover"] > div > button {
        background-color: var(--azul-fundo-2) !important;
        color: var(--azul-primario) !important;
        border: 1px solid var(--azul-borda) !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stPopover"] > div > button:hover {
        background-color: var(--azul-fundo-2) !important;
        color: var(--azul-primario) !important;
        border: 1px solid var(--azul-primario) !important;
        box-shadow: 0 0 6px rgba(0, 194, 255, 0.5) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Inicializar o motor RAG em cache para evitar recriacao desnecessaria
@st.cache_resource
def get_rag_engine():
    return RAGEngine()


try:
    engine = get_rag_engine()
except Exception as e:
    st.error(
        f"Erro ao inicializar o motor RAG: {e}. Verifique sua GEMINI_API_KEY no arquivo .env!"
    )
    st.stop()

# Perguntas sugeridas para demonstracao ao vivo
PERGUNTAS_SUGERIDAS = [
    "O que define a qualidade de um software?",
    "Qual a diferença entre qualidade de conformidade e qualidade de projeto?",
    "Como identificar e classificar falhas em um sistema?",
    "Quais são as boas práticas no desenvolvimento backend?",
    "O que é confiabilidade de software e como ela é medida?",
]

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("Painel de Controle")
    st.markdown(
        '**AskData** | <i><a href="https://datalakers.com.br/" target="_blank" class="link-discreto">DataLakers</a> & '
        '<a href="https://tecnopuc.pucrs.br/hubs/navi/" target="_blank" class="link-discreto">Navi Hub</a></i>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    with st.popover("Opções de Busca", use_container_width=False):
        top_k = st.slider(
            "Quantidade de Chunks (Top-K):", min_value=1, max_value=5, value=3
        )

    with st.popover("Sobre a Base Indexada", use_container_width=False):
        st.caption(
            "Esta aplicação utiliza embeddings do Google (`gemini-embedding-001`), armazenamento vetorial persistente no **ChromaDB** e geração com o **Modelo Gemini**."
        )

    st.markdown("### Perguntas Sugeridas")
    for pergunta in PERGUNTAS_SUGERIDAS:
        if st.button(pergunta, key=f"btn_{pergunta}", use_container_width=True):
            st.session_state.pending_prompt = pergunta
            st.rerun()

    if st.button("Limpar Historico de Chat"):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

# --- AREA PRINCIPAL ---
st.title("AskData: Assistente de Documentação Técnica Tech")
st.caption(
    "Faça perguntas sobre a base de conhecimento. Todas as respostas são fundamentadas com citação direta dos documentos."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou o AskData. Como posso ajudar com base nos documentos técnicos da área da tecnologia?",
            "fontes": [],
        }
    ]
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def render_fontes(fontes):
    """Renderiza a lista de fontes com barra de similaridade visual."""
    with st.expander("Ver Fontes e Chunks Recuperados"):
        for idx, f in enumerate(fontes, 1):
            st.markdown(
                f"**Fonte {idx}:** `{f['arquivo']}` (Pág. {f['pagina']})"
            )
            col1, col2 = st.columns([4, 1])
            with col1:
                st.progress(min(max(f["similaridade"], 0.0), 1.0))
            with col2:
                st.caption(f"{f['similaridade']:.2%}")
            st.info(f["texto"])


# Renderizar historico de mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("fontes"):
            render_fontes(msg["fontes"])

prompt = st.session_state.pending_prompt if st.session_state.pending_prompt else None
if prompt is None:
    prompt = st.chat_input("Digite sua pergunta técnica aqui...")

if prompt:
    if st.session_state.pending_prompt:
        st.session_state.pending_prompt = None

    st.session_state.messages.append({"role": "user", "content": prompt, "fontes": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    tempo_resposta = 0.0

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        try:
            status_placeholder.markdown("🔎 *Buscando nos documentos...*")
            inicio = time.perf_counter()

            status_placeholder.markdown(" *Gerando resposta...*")
            resultado = engine.responder_pergunta(prompt, top_k=top_k)

            tempo_resposta = time.perf_counter() - inicio
            resposta_texto = resultado["resposta"]
            fontes = resultado["fontes"]

            status_placeholder.empty()
            st.markdown(resposta_texto)
            st.caption(f"Tempo de resposta: {tempo_resposta:.2f}s")

            if fontes:
                render_fontes(fontes)

            st.session_state.messages.append(
                {"role": "assistant", "content": resposta_texto, "fontes": fontes}
            )
        except Exception as err:
            status_placeholder.empty()
            st.error(f"Erro ao processar a pergunta: {err}")
            st.caption(f"Tempo de resposta: {tempo_resposta:.2f}s")

        historico_json = json.dumps(st.session_state.messages, indent=2, ensure_ascii=False)
        st.sidebar.download_button(
            label="Exportar Historico (JSON)",
            data=historico_json,
            file_name="historico_chat.json",
            mime="application/json",
        )
# Exemplo de calculo de confianca media das fontes recuperadas
if "messages" in st.session_state and st.session_state.messages:
    ultima_msg = st.session_state.messages[-1]
    fontes = ultima_msg.get("fontes", [])
    if fontes:
        similaridades = [f["similaridade"] for f in fontes]
        media_sim = sum(similaridades) / len(similaridades)

        if media_sim >= 0.75:
            status = "Alta"
            cor = "green"
        elif media_sim >= 0.50:
            status = "Media"
            cor = "orange"
        else:
            status = "Baixa"
            cor = "red"

        with st.sidebar:
            st.markdown(f"**Confianca da Ultima Resposta:** :{cor}[{status} ({media_sim:.1%})]")
# Dica de Engenharia: Se algo nao funcionar de primeira, leia o traceback e debugar faz parte do projeto!