import streamlit as st

CSS = """
<style>
    .stApp {
        background-color: #faf8ef;
    }
    .main, .block-container {
        color: #2b2b2b;
    }
    .main p, .main li, .main span, .main label,
    .block-container p, .block-container li,
    .block-container span, .block-container label {
        color: #2b2b2b;
    }
    .main h1, .main h2, .main h3, .main h4 {
        color: #1d5631 !important;
    }
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
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul,
    ul[role="listbox"] {
        background-color: #ffffff !important;
    }

    div[data-baseweb="popover"] li,
    ul[role="listbox"] li,
    li[role="option"] {
        background-color: #ffffff !important;
        color: #1d5631 !important;
    }
    div[data-baseweb="popover"] li:hover,
    ul[role="listbox"] li:hover,
    li[role="option"]:hover {
        background-color: #f5f2e3 !important;
        color: #1d5631 !important;
    }
    li[role="option"][aria-selected="true"] {
        background-color: #7ba05b !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSlider"] {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] input {
        background-color: #ffffff !important;
        color: #1d5631 !important;
    }
    .main div[data-baseweb="select"] > div,
    .block-container div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #e3ddc4 !important;
    }
    .main div[data-baseweb="select"] *,
    .block-container div[data-baseweb="select"] * {
        color: #1d5631 !important;
    }
    .main div[data-testid="stExpander"] summary,
    .block-container div[data-testid="stExpander"] summary {
        background-color: #f5f2e3 !important;
        color: #1d5631 !important;
        border-radius: 6px;
    }
    .main div[data-testid="stExpander"] summary ,
    .block-container div[data-testid="stExpander"] summary {
        color: #1d5631 !important;
    }
    .main div[data-testid="stExpander"] div[data-testid="stExpanderDetails"],
    .block-container div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
        background-color: #ffffff !important;
    }
    .main div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] ,
    .block-container div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
        color: #2b2b2b !important;
    }

    .main div[data-testid="stExpander"],
    .block-container div[data-testid="stExpander"] {
        border: 1px solid #e3ddc4 !important;
        border-radius: 8px;
    }
</style>
"""


def aplicar_estilo():
    st.markdown(CSS, unsafe_allow_html=True)