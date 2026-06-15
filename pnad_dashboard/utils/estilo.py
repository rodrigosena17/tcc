import streamlit as st

CSS = """
<style>
    /* Fundo geral creme */
    .stApp {
        background-color: #faf8ef;
    }

    /* Texto padrao da area principal em tom escuro */
    .main, .block-container {
        color: #2b2b2b;
    }
    .main p, .main li, .main span, .main label,
    .block-container p, .block-container li,
    .block-container span, .block-container label {
        color: #2b2b2b;
    }

    /* Titulos da area principal em verde escuro */
    .main h1, .main h2, .main h3, .main h4 {
        color: #1d5631 !important;
    }

    /* Sidebar verde escuro com texto branco */
    section[data-testid="stSidebar"] {
        background-color: #1d5631;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* Cards de metrica com fundo bege e texto escuro */
    div[data-testid="stMetric"] {
        background-color: #f5f2e3;
        border: 1px solid #e3ddc4;
        border-radius: 8px;
        padding: 16px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
        color: #a52828 !important;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #1d5631 !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #5a8a3c !important;
    }

    /* Abas */
    button[data-baseweb="tab"] {
        color: #1d5631;
    }

    .block-container {
        padding-top: 2rem;
    }

    /* ===== Inputs de filtro na sidebar com fundo claro ===== */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #e3ddc4 !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #1d5631 !important;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #7ba05b !important;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"] * {
        color: #ffffff !important;
    }
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    div[data-baseweb="popover"] li {
        color: #1d5631 !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #f5f2e3 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSlider"] {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] input {
        background-color: #ffffff !important;
        color: #1d5631 !important;
    }
</style>
"""


def aplicar_estilo():
    st.markdown(CSS, unsafe_allow_html=True)