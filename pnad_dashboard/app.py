import streamlit as st
from utils.estilo import aplicar_estilo

st.set_page_config(
    page_title="PNAD Continua - Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilo()

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
#Fazer alterações aqui
#Usar como cabeçalho para o TCC com as informações da pesquisa e dos pesquisadores/orientador.


st.info("Selecione uma pagina no menu lateral para comecar a explorar os dados.")