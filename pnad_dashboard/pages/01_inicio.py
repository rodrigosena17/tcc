import streamlit as st
from utils.estilo import aplicar_estilo

st.set_page_config(page_title="Inicio - PNAD", layout="wide")

aplicar_estilo()

st.title("Sobre o Projeto")

st.markdown(
    """
    Este projeto utiliza os microdados trimestrais da **PNAD Continua** do IBGE
    entre 2019 e 2025 para analisar caracteristicas do mercado de trabalho e da
    renda da populacao brasileira.

    Os dados foram processados em Python e transformados em estatisticas
    trimestrais, permitindo a construcao de series historicas e comparacoes
    entre diferentes grupos ocupacionais.
    """
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("O que e a PNAD Continua")
    st.markdown(
        """
        A Pesquisa Nacional por Amostra de Domicilios Continua e uma pesquisa
        do IBGE que acompanha de forma continua as flutuacoes trimestrais e a
        evolucao de curto, medio e longo prazo da forca de trabalho, alem de
        outras informacoes necessarias ao estudo socioeconomico do pais.

        A coleta e feita por amostragem de domicilios, gerando indicadores
        representativos da populacao por meio de pesos amostrais
        (populacao ponderada).
        """
    )

with col2:
    st.subheader("Periodo analisado (2019 - 2025)")
    st.markdown(
        """
        O recorte de 2019 a 2025 permite observar o mercado de trabalho antes,
        durante e apos o periodo de impacto da pandemia, capturando mudancas
        relevantes em:

        - taxa de ocupacao;
        - formalizacao do emprego (carteira assinada);
        - rendimentos medios e medianos;
        - distribuicao por escolaridade e horas trabalhadas.
        """
    )

st.divider()

st.subheader("Variaveis Utilizadas")

variaveis = {
    "V4001": [
        "Indicador de ocupacao",
        "1 = Trabalhou | 2 = Nao trabalhou",
    ],
    "V4029": ["Carteira assinada", "1 = Sim | 2 = Nao"],
    "V4028": ["Servidor publico", "1 = Sim | 2 = Nao"],
    "V4012": [
        "Posicao na ocupacao",
        "5 = Empregador | 6 = Conta propria",
    ],
    "V403312": ["Rendimento mensal", "Valor monetario"],
    "V4039": ["Horas trabalhadas por semana", "Horas habituais"],
    "V3009A": ["Nivel de escolaridade", "Categorias de escolaridade"],
}

for codigo, info in variaveis.items():
    with st.expander(f"{codigo} - {info[0]}"):
        st.markdown(f"**Descricao:** {info[0]}")
        st.markdown(f"**Categorias:** {info[1]}")

st.divider()

st.subheader("Arquivos de Dados")
st.markdown(
    """
    - **estatisticas_empilhadas.csv**: estatisticas trimestrais consolidadas
      (ocupacao, renda, percentuais e horas).
    - **renda_escolaridade_empilhada.csv**: renda total por nivel de
      escolaridade em cada trimestre.
    - **renda_horas_semanais_empilhada.csv**: renda total por faixa de horas
      semanais trabalhadas.
    """
)