import streamlit as st

st.set_page_config(
    page_title="PNAD Continua - Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
    .main {
        background-color: #faf8ef;
    }
    .stApp {
        background-color: #faf8ef;
    }

    section[data-testid="stSidebar"] {
        background-color: #1d5631;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    div[data-testid="stMetric"] {
        background-color: #f5f2e3;
        border: 1px solid #e3ddc4;
        border-radius: 8px;
        padding: 16px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
        color: #a52828;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #1d5631;
    }
    div[data-testid="stMetricDelta"] {
        color: #5a8a3c;
    }

    .main h1, .main h2, .main h3 {
        color: #1d5631;
    }

    button[data-baseweb="tab"] {
        color: #1d5631;
    }

    .block-container {
        padding-top: 2rem;
    }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

st.title("Painel de Analise da PNAD Continua")
st.subheader("Mercado de Trabalho e Renda no Brasil (2019 - 2025)")

st.markdown(
    """
    Bem-vindo ao painel interativo de analise da Pesquisa Nacional por Amostra
    de Domicilios Continua (PNAD Continua), conduzida pelo IBGE.

    Utilize o menu lateral para navegar entre as paginas:

    - **Inicio**: descricao do projeto, variaveis e contexto da pesquisa.
    - **Estatisticas**: modulos interativos com series temporais e analises.
    """
)

st.info(
    "Selecione uma pagina no menu lateral para comecar a explorar os dados.",
    icon=None,
)