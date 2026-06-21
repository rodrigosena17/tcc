# Dashboard PNAD Contínua: Mercado de Trabalho e Renda

Este projeto desenvolve um dashboard interativo em **Python** utilizando **Streamlit** e **Plotly** para visualização de estatísticas trimestrais derivadas dos microdados da **PNAD Contínua (IBGE)**.

O objetivo é permitir a exploração de séries históricas relacionadas ao mercado de trabalho, rendimento, escolaridade, ocupação, carteira assinada, servidores públicos, conta própria, empregadores e outras relações socioeconômicas relevantes.

---

## 1. Visão Geral

A aplicação utiliza microdados trimestrais da PNAD Contínua do IBGE, processados previamente em Python, para gerar estatísticas agregadas por ano e trimestre.

A partir desses dados, o dashboard permite analisar:

- Panorama geral da população e ocupação;
- Indicadores de renda;
- Trabalhadores ocupados;
- Trabalhadores com carteira assinada;
- Servidores públicos;
- Trabalhadores por conta própria;
- Empregadores;
- Renda por escolaridade;
- Renda por horas trabalhadas;
- Idade × renda;
- Tempo de trabalho × renda;
- Escolaridade × ocupação;
- Escolaridade × carteira assinada;
- Sexo × renda × escolaridade;
- Cor ou raça × escolaridade × renda.

---

## 2. Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- PNAD Contínua / IBGE

---

## 3. Estrutura do Projeto

A estrutura principal do projeto é organizada da seguinte forma:

```text
pnad_dashboard/
│
├── app.py
│
├── pages/
│   ├── 01_Inicio.py
│   └── 02_estatisticas.py
│
├── utils/
│   ├── carregamento.py
│   ├── estilo.py
│   ├── filtros.py
│   └── graficos.py
│
├── data/
│   ├── estatisticas_empilhadas.csv
│   ├── renda_escolaridade_empilhada.csv
│   ├── renda_horas_semanais_empilhada.csv
│   ├── idade_renda_empilhada.csv
│   ├── tempo_trabalho_renda_empilhada.csv
│   ├── escolaridade_ocupacao_empilhada.csv
│   ├── escolaridade_carteira_empilhada.csv
│   ├── sexo_renda_escolaridade_empilhada.csv
│   ├── cor_raca_renda_escolaridade_empilhada.csv
│   │
│   └── microdados_pnad/
│       └── estatisticas_trimestrais/
│           ├── 2019/
│           ├── 2020/
│           ├── 2021/
│           ├── 2022/
│           ├── 2023/
│           ├── 2024/
│           └── 2025/
│
└── README.md
```

## 4. Organização dos Arquivos

### `app.py`

Arquivo principal da aplicação Streamlit.

Responsável por:

- Configurar a aplicação;
- Definir o layout geral;
- Controlar a navegação entre páginas.
- Apresentação do projeto;
- Descrição da PNAD Contínua;
- Explicação do período analisado;
- Descrição das principais variáveis utilizadas.

### `pages/02_estatisticas.py`

Página principal de análise estatística.

Contém:

- Módulos interativos do dashboard;
- Filtros por ano e trimestre;
- Métricas resumidas;
- Gráficos interativos para diferentes dimensões analisadas.

### `utils/carregamento.py`

Responsável pela leitura e preparação dos arquivos CSV utilizados pelo dashboard.

Principais funções:

- Leitura dos arquivos empilhados;
- Conversão de colunas numéricas;
- Criação da coluna `Periodo`;
- Mapeamento de categorias como escolaridade, sexo e cor/raça.

### `utils/filtros.py`

Contém funções auxiliares para criação e aplicação de filtros no Streamlit.

Exemplos:

- Filtro por intervalo de anos;
- Filtro por trimestre;
- Filtro por ano único;
- Filtro por série temporal.

### `utils/graficos.py`

Contém funções reutilizáveis para construção de gráficos com Plotly.

Principais tipos de gráficos:

- Gráficos de linha;
- Gráficos de barras;
- Gráficos de dispersão.

### `utils/estilo.py`

Arquivo responsável pela aplicação de estilos visuais da interface Streamlit.

Inclui customizações de:

- Cores;
- Cards;
- Métricas;
- Layout;
- Fontes.

---

## 5. Dados Utilizados

A aplicação utiliza arquivos CSV já processados e agregados.

Os principais arquivos empilhados esperados na pasta `data/` são:

### Estatísticas gerais

Arquivo:

`estatisticas_empilhadas.csv`

Contém indicadores gerais por ano e trimestre, como:

- `Ano`
- `Trimestre`
- `Total_Pessoas`
- `Populacao_Ponderada`
- `Ocupados_total`
- `Ocupados_Ponderado`
- `Taxa_Ocupacao`
- `Ocupados_Renda_Total`
- `Ocupados_Renda_Media`
- `Carteira_Assinada_Total`
- `Carteira_Assinada_Ponderado`
- `Servidor_Publico_Total`
- `Servidor_Publico_Ponderado`
- `Conta_Propria_Total`
- `Conta_Propria_Ponderado`
- `Empregador_Total`
- `Empregador_Ponderado`
- `Renda_Media`
- `Renda_Mediana`
- `Renda_Media_Ponderada`
- `Horas_Media_Semanal`

### Renda por escolaridade

Arquivo:

`renda_escolaridade_empilhada.csv`

Contém:

- `Ano`
- `Trimestre`
- `Escolaridade`
- `Renda_Total`

### Renda por horas semanais

Arquivo:

`renda_horas_semanais_empilhada.csv`

Contém:

- `Ano`
- `Trimestre`
- `Horas_Semanais`
- `Renda_Total`

### Idade × renda

Arquivo:

`idade_renda_empilhada.csv`

Contém:

- `Ano`
- `Trimestre`
- `Idade`
- `Renda_Media`

### Tempo de trabalho × renda

Arquivo:

`tempo_trabalho_renda_empilhada.csv`

Contém:

- `Ano`
- `Trimestre`
- `Tempo_Trabalho`
- `Renda_Media`

### Escolaridade × ocupação

Arquivo:

`escolaridade_ocupacao_empilhada.csv`

Contém:

- `Ano`
- `Trimestre`
- `Escolaridade`
- `Percentual_Ocupados`

### Escolaridade × carteira assinada

Arquivo:

`escolaridade_carteira_empilhada.csv`

Contém:

- `Ano`
- `Trimestre`
- `Escolaridade`
- `Percentual_Carteira`

### Sexo × renda × escolaridade

Arquivo:

`sexo_renda_escolaridade_empilhada.csv`

Contém:

- `Ano`
- `Trimestre`
- `Sexo`
- `Escolaridade`
- `Renda_Media`

### Cor/raça × escolaridade × renda

Arquivo:

`cor_raca_renda_escolaridade_empilhada.csv`

Contém:

- `Ano`
- `Trimestre`
- `Cor_Raca`
- `Escolaridade`
- `Renda_Media`

---

## 6. Geração das Estatísticas

As estatísticas são geradas a partir dos arquivos organizados da PNAD Contínua por meio do script de processamento.

O script percorre os arquivos organizados, calcula estatísticas por ano e trimestre e salva dois tipos de saída:

1. Arquivos empilhados na pasta `data/`;
2. Arquivos separados por ano na pasta `data/microdados_pnad/estatisticas_trimestrais/`.

Estrutura esperada:

`data/`

- `estatisticas_empilhadas.csv`
- `renda_escolaridade_empilhada.csv`
- `renda_horas_semanais_empilhada.csv`
- `idade_renda_empilhada.csv`
- `tempo_trabalho_renda_empilhada.csv`
- `escolaridade_ocupacao_empilhada.csv`
- `escolaridade_carteira_empilhada.csv`
- `sexo_renda_escolaridade_empilhada.csv`
- `cor_raca_renda_escolaridade_empilhada.csv`

`data/microdados_pnad/estatisticas_trimestrais/`

- `2019/`
- `2020/`
- `2021/`
- `2022/`
- `2023/`
- `2024/`
- `2025/`

Cada pasta anual contém arquivos específicos daquele ano, como:

- `2019_estatisticas.csv`
- `2019_renda_escolaridade.csv`
- `2019_renda_horas_semanais.csv`
- `2019_idade_renda.csv`
- `2019_tempo_trabalho_renda.csv`
- `2019_escolaridade_ocupacao.csv`
- `2019_escolaridade_carteira.csv`
- `2019_sexo_renda_escolaridade.csv`
- `2019_cor_raca_renda_escolaridade.csv`

---

## 7. Principais Variáveis da PNAD Utilizadas

### `V4001`

Indicador de ocupação.

- `1` = Trabalhou
- `2` = Não trabalhou

### `V4029`

Carteira assinada.

- `1` = Sim
- `2` = Não

### `V4028`

Servidor público.

- `1` = Sim
- `2` = Não

### `V4012`

Posição na ocupação.

- `5` = Empregador
- `6` = Conta própria

### `V403312`

Rendimento mensal em reais.

### `V4039`

Horas habitualmente trabalhadas por semana.

### `V3009A`

Nível de escolaridade.

-  `1` = Creche,
-  `2` = Pré-escola,
-  `3` = Classe de alfabetização (CA),
-  `4` = Alfabetização de jovens e adultos,
-  `5` = Antigo primário (elementar),
-  `6` = Antigo ginásio (médio 1º ciclo),
-  `7` = Ensino fundamental regular,
-  `8` = EJA ou supletivo do 1º grau,
-  `9` = Antigo científico, clássico etc. (médio 2º ciclo),
-  `10` = Ensino médio regular,
-  `11` = EJA ou supletivo do 2º grau,
-  `12` = Superior - graduação,
-  `13` = Especialização,
-  `14` = Mestrado,
-  `15` = Doutorado

### `V2007`

Sexo.

-  `1` = Homem,
-  `2` = Mulher,

### `V2010`

Cor ou raça.

-  `1` = Branco,
-  `2` = Preto,
-  `3` = Amarelo,
-  `4` = Pardo,
-  `5` = Indígena,
-  `9` = Ignorado,

### `V2009`

Idade total em anos.

### `V4040`

Tempo de trabalho no trabalho em questão.

-  `1` = Até 1 mês,
-  `2` = De 1 mês a menos que 1 ano,
-  `3` = de 1 ano a menos que 2 anos,
-  `4` = 2 anos ou mais,

---

## 8. Módulos do Dashboard

A página de estatísticas contém os seguintes módulos:

### 1. Panorama Geral

Exibe:

- População total;
- População ponderada;
- Ocupados;
- Ocupados ponderados;
- Taxa de ocupação;
- Renda média;
- Renda mediana;
- Renda média ponderada;
- Média de horas trabalhadas.

### 2. Ocupados

Exibe:

- Total de ocupados;
- Ocupados ponderados;
- Renda total dos ocupados;
- Renda média dos ocupados.

### 3. Carteira Assinada

Exibe:

- Total de trabalhadores com carteira assinada;
- Total ponderado;
- Renda total;
- Renda média;
- Percentual de carteira assinada.

### 4. Servidor Público

Exibe:

- Total de servidores públicos;
- Total ponderado;
- Renda total;
- Renda média;
- Percentual de servidores públicos.

### 5. Conta Própria

Exibe:

- Total de trabalhadores por conta própria;
- Total ponderado;
- Renda total;
- Renda média;
- Percentual de conta própria.

### 6. Empregadores

Exibe:

- Total de empregadores;
- Total ponderado;
- Renda total;
- Renda média;
- Percentual de empregadores.

### 7. Escolaridade × Renda

Analisa:

- Renda total por nível de escolaridade;
- Comparações entre trimestres;
- Ordenação das categorias por renda.

### 8. Horas Trabalhadas × Renda

Analisa:

- Relação entre horas habitualmente trabalhadas por semana e renda total;
- Gráfico de dispersão;
- Gráfico de linha;
- Gráfico de barras.

### 9. Idade × Renda

Analisa:

- Renda média por idade;
- Distribuição da renda ao longo das idades;
- Possibilidade de limitar a faixa etária analisada.

### 10. Tempo de Trabalho × Renda

Analisa:

- Renda média por tempo de trabalho;
- Relação entre permanência no trabalho e rendimento.

### 11. Escolaridade × Ocupação

Analisa:

- Percentual de ocupados por nível de escolaridade;
- Comparação entre níveis educacionais.

### 12. Escolaridade × Carteira Assinada

Analisa:

- Percentual de trabalhadores com carteira assinada por nível de escolaridade.

### 13. Sexo × Renda × Escolaridade

Analisa:

- Renda média por sexo;
- Renda média por escolaridade;
- Comparações simultâneas entre sexo e escolaridade.

### 14. Cor/Raça × Escolaridade × Renda

Analisa:

- Renda média por cor/raça;
- Renda média por escolaridade;
- Comparações simultâneas entre cor/raça e escolaridade.

---

## 9. Como Executar o Projeto

### 1. Criar ambiente virtual

No terminal, execute:

`python -m venv venv`

### 2. Ativar ambiente virtual

No Windows:

`venv\Scripts\activate`

No Linux/Mac:

`source venv/bin/activate`

### 3. Instalar dependências

`pip install -r requirements.txt`

### 4. Executar a aplicação

`streamlit run app.py`

---

## 10. Observações Importantes

- O deploy do app foi feito na plataforma do streamlit, e pode ser acessado no link abaixo:

`[PNAD Dashboard - App](https://pnad-dashboard.streamlit.app/)`

---

## 11. Observações Importantes

- Os dados originais da PNAD Contínua não são carregados diretamente no dashboard.
- O dashboard utiliza arquivos CSV já processados e agregados.
- Caso novos anos sejam adicionados, os arquivos empilhados devem ser regenerados.
- As categorias de escolaridade, sexo e cor/raça são tratadas no arquivo `utils/carregamento.py`.
- O dashboard foi estruturado para permitir expansão futura com novos módulos e novas variáveis.

---

## 12. Próximos Passos

Melhorias futuras a serem implementdas:

- Automatizar a atualização dos arquivos empilhados para os próximos anos;
- Adicionar filtros geográficos;
- Incluir análises por UF, região e setor de atividade;
- Incorporar novos indicadores de rendimento;
- Adicionar opção de download das tabelas filtradas;

---

## 13. Fonte dos Dados

Os dados utilizados têm origem nos microdados da:

**PNAD Contínua: Pesquisa Nacional por Amostra de Domicílios Contínua**

Instituto Brasileiro de Geografia e Estatística — **IBGE**

Site oficial:

`https://www.ibge.gov.br/`

---

## 14. Licença

Este projeto foi desenvolvido para fins acadêmicos e analíticos.

O uso dos dados deve respeitar as condições de uso e divulgação estabelecidas pelo IBGE.
