import streamlit as st
from utils.estilo import aplicar_estilo

st.set_page_config(page_title="Início - PNAD", layout="wide")

aplicar_estilo()

st.title("Sobre o Projeto")

st.markdown(
    """
    Este projeto utiliza os microdados trimestrais da **PNAD Contínua** do IBGE
    entre 2019 e 2025 para analisar características do mercado de trabalho e da
    renda da população brasileira.

    Os dados foram processados em Python e transformados em estatísticas
    trimestrais, permitindo a construção de series históricas e comparações
    entre diferentes grupos ocupacionais.
    """
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("O que e a PNAD Contínua")
    st.markdown(
        """
        A Pesquisa Nacional por Amostra de Domicilios Contínua é uma pesquisa
        do IBGE que acompanha de forma contínua as flutuações trimestrais e a
        evolução de curto, médio e longo prazo da força de trabalho, além de
        outras informações necessárias ao estudo socioeconomico do país.

        A coleta é feita por amostragem de domicílios, gerando indicadores
        representativos da população por meio de pesos amostrais
        (população ponderada).
        """
    )

with col2:
    st.subheader("Período analisado (2019 - 2025)")
    st.markdown(
        """
        O recorte de 2019 a 2025 permite observar o mercado de trabalho antes,
        durante e após o período de impacto da pandemia, capturando mudanças
        relevantes em:

        - taxa de ocupação;
        - formalização do emprego (carteira assinada);
        - rendimentos medios e medianos;
        - distribuição por escolaridade e horas trabalhadas.
        """
    )

st.divider()

st.subheader("Variaveis Utilizadas")

variaveis = {
    "V1028": ["Peso do domicílio das pessoas com calibração", "Valor numérico"],
    "V2007": ["Sexo","1 = Homem | 2 = Mulher",], #Não utilizado ainda
    "V2009": ["Idade","Valor numérico entre 0 e 130",], #Não utilizado ainda
    "V2010": ["Cor/Raça","1 = Branco | 2 = Preto | 3 = Amarelo | 4 = Pardo | 5 = Indígena | 9 = Ignorado",], #Não utilizado ainda
    "V3014": ["Conclusão de curso frequentado","1 = Sim | 2 = Não",], #Não utilizado ainda
    "V4001": ["Indicador de ocupação","1 = Trabalhou | 2 = Não trabalhou"],
    "V4028": ["Servidor público", "1 = Sim | 2 = Não"],
    "V4029": ["Carteira assinada", "1 = Sim | 2 = Não"],
    "V4012": ["Posição na ocupação","5 = Empregador | 6 = Conta própria",],
    "V403312": ["Rendimento mensal", "Valor monetário"],
    "V4039": ["Horas trabalhadas por semana", "Horas habituais"],
    "V4040": ["Tempo de trabalho", "1 = Menos de 1 mês | 2 = 1 mês a menos de 1 ano | 3 = 1 ano a menos de 2 anos | 4 = 2 anos ou mais",], #Não utilizado ainda
    "V4071": ["Providência para conseguir trabalho", "1 = Sim | 2 = Não",], #Não utilizado ainda
    "V3009A": ["Nível de escolaridade", "Categorias de escolaridade"],
}

for codigo, info in variaveis.items():
    with st.expander(f"{codigo} - {info[0]}"):
        st.markdown(f"**Descrição:** {info[0]}")
        st.markdown(f"**Categorias:** {info[1]}")

st.divider()

st.subheader("Arquivos de Dados")
st.markdown(
    """
    - **estatísticas_empilhadas.csv**: estatísticas trimestrais consolidadas
      (ocupação, renda, percentuais e horas).
    - **renda_escolaridade_empilhada.csv**: renda total por nivel de
      escolaridade em cada trimestre.
    - **renda_horas_semanais_empilhada.csv**: renda total por faixa de horas
      semanais trabalhadas.
    """
)