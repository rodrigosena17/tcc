import streamlit as st
from utils.estilo import aplicar_estilo

st.set_page_config(
    page_title="PNAD Continua - Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilo()

st.title("Sobre o Projeto")

st.markdown(
    """
    Dashboard interativo para exploracao de dados da Pesquisa Nacional por Amostra de Domicilios Contínua (PNAD Continua) do IBGE, 
    com foco em mercado de trabalho e renda da população brasileira. 
    Elaborado como parte da entrega final do Trabalho de Conclusão de Curso do curso de Análise e Desenvolvimento de Sistemas do IFPE.

    Título do trabalho: "Integração e Mineração de Dados: uma abordagem em Ciência de Dados aplicada à análise da mobilidade social e inserção no mercado de trabalho"

    Discentes: Karen Evellyn Vieira Ribeiro e Rodrigo Sena Rodrigues
    
    Orientador: Prof. Dr. Lutemberg Francisco de Andrade Santana

    
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
    st.subheader("O que é a PNAD Contínua")
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

        - Taxa de ocupação;
        - Formalização do emprego (carteira assinada);
        - Rendimentos medios e medianos;
        - Distribuição por:
            - Cor/Raça;
            - Escolaridade;
            - Horas trabalhadas;
            - Sexo;
            - Tempo de trabalho.
        """
    )

st.divider()

st.subheader("Variáveis Utilizadas")

variaveis = {
    "V1028": ["Peso do domicílio das pessoas com calibração", "Valor numérico"],
    "V2007": ["Sexo","1 = Homem | 2 = Mulher",], 
    "V2009": ["Idade","Valor numérico entre 0 e 130",],
    "V2010": ["Cor/Raça","1 = Branco | 2 = Preto | 3 = Amarelo | 4 = Pardo | 5 = Indígena | 9 = Ignorado",], 
    "V3014": ["Conclusão de curso frequentado","1 = Sim | 2 = Não",], 
    "V4001": ["Indicador de ocupação","1 = Trabalhou | 2 = Não trabalhou"],
    "V4028": ["Servidor público", "1 = Sim | 2 = Não"],
    "V4029": ["Carteira assinada", "1 = Sim | 2 = Não"],
    "V4012": ["Posição na ocupação","5 = Empregador | 6 = Conta própria",],
    "V403312": ["Rendimento mensal", "Valor monetário recebido por mês",],
    "V4039": ["Horas trabalhadas por semana", "Horas habituais de trabalho por semana",],
    "V4040": ["Tempo de trabalho", "1 = Menos de 1 mês | 2 = 1 mês a menos de 1 ano | 3 = 1 ano a menos de 2 anos | 4 = 2 anos ou mais",], 
    "V4071": ["Providência para conseguir trabalho", "1 = Sim | 2 = Não",], 
    "V3009A": ["Nível de escolaridade", "1: Creche | 2: Pré-escola | 3: Classe de alfabetização (CA) | 4: Alfabetização de jovens e adultos "
    "| 5: Antigo primário (elementar) | 6: Antigo ginásio (médio 1º ciclo) | 7: Ensino fundamental regular | 8: EJA ou supletivo do 1º grau "
    "| 9: Antigo científico, clássico etc. (médio 2º ciclo) | 10: Ensino médio regular | 11: EJA ou supletivo do 2º grau | 12: Superior - graduação "
    "| 13: Especialização | 14: Mestrado | 15: Doutorado"]
}

for codigo, info in variaveis.items():
    with st.expander(f"{codigo}"):
        st.markdown(f"**Descrição:** {info[0]}")
        st.markdown(f"**Categorias:** {info[1]}")

st.divider()