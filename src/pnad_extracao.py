import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from zipfile import ZipFile
from pnad_organizacao import organizar_pnad
from pnad_estatisticas import calcular_estatisticas

# Configuracoes basicas (raiz)
base_url = "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/"

# Pasta raiz onde tudo sera guardado
diretorio_raiz = os.path.join("data", "microdados_pnad")
os.makedirs(diretorio_raiz, exist_ok=True)

# Pastas estruturadas
pasta_zips = os.path.join(diretorio_raiz, "arquivos_zip")
pasta_descompactados = os.path.join(diretorio_raiz, "dados_descompactados")
pasta_organizados_txt = os.path.join(diretorio_raiz, "dados_organizados_txt")
pasta_organizados_csv = os.path.join(diretorio_raiz, "dados_organizados_csv")
pasta_empilhados = os.path.join(diretorio_raiz, "dados_empilhados")

for p in [pasta_zips, pasta_descompactados, pasta_organizados_txt, pasta_organizados_csv, pasta_empilhados]:
    os.makedirs(p, exist_ok=True)

# Lista de anos a serem baixados
anos_teste = ["2019/", "2020/", "2021/", "2022/", "2023/", "2024/", "2025/"]

# Auxiliar: normalizar ano (ex: "2024/" -> "2024")
def ano_para_pasta(ano_str):
    return ano_str.strip().strip("/")

# Funcao: baixar todos os arquivos de um determinado ano
def baixar_ano(ano):
    """Baixa e descompacta os microdados de um ano (ex: '2024/')."""
    ano_folder = ano_para_pasta(ano)
    ano_url = base_url + ano
    print(f"\nBuscando arquivos em: {ano_url}")

    resp = requests.get(ano_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Localiza todos os arquivos ZIP disponiveis na pagina
    zips = [a['href'] for a in soup.find_all('a') if a.get('href', '').endswith('.zip')]

    # Pastas por ano
    pasta_zip_ano = os.path.join(pasta_zips, ano_folder)
    pasta_txt_ano = os.path.join(pasta_descompactados, ano_folder)
    os.makedirs(pasta_zip_ano, exist_ok=True)
    os.makedirs(pasta_txt_ano, exist_ok=True)

    for z in zips:
        caminho_zip = os.path.join(pasta_zip_ano, z)

        # Baixa o arquivo ZIP se ainda nao existir
        if not os.path.exists(caminho_zip):
            print(f"Baixando {z} para {pasta_zip_ano} ...")
            with open(caminho_zip, 'wb') as f:
                f.write(requests.get(ano_url + z).content)
            print(f"{z} salvo com sucesso em {caminho_zip}.")

            # Descompacta o arquivo dentro da pasta txt do ano
            with ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(pasta_txt_ano)

            print(f"{z} descompactado em {pasta_txt_ano}.\n")
        else:
            print(f"{z} ja existe em {pasta_zip_ano}, pulando download.")

# Funcao: processar um arquivo .txt extraido
def tratar_dados(caminho_txt, ano):
    #Chama o modulo de organizacao para processar o arquivo bruto .txt
    print(f"Processando arquivo: {caminho_txt}")
    try:
        ano_folder = ano_para_pasta(ano)
        # pastas de destino por ano
        saida_txt_dir = os.path.join(pasta_organizados_txt, ano_folder)
        saida_csv_dir = os.path.join(pasta_organizados_csv, ano_folder)
        os.makedirs(saida_txt_dir, exist_ok=True)
        os.makedirs(saida_csv_dir, exist_ok=True)

        # organizar_pnad agora recebe caminhos de saida
        organizar_pnad(caminho_txt, saida_csv_dir)
        print(f"Arquivo organizado gerado para o ano {ano_folder}.\n")
    except Exception as e:
        print(f"Erro ao processar {caminho_txt}: {e}\n")

# Função: empilhar todos os arquivos organizados
def empilhar_dados(base_dir_organizados_csv):
    """
    Procura recursivamente por todos os arquivos *_organizado.csv dentro de base_dir_organizados_csv,
    concatena e salva em dados_empilhados/PNAD_empilhada.csv
    """
    arquivos_csv = []
    for root, dirs, files in os.walk(base_dir_organizados_csv):
        for f in files:
            if f.endswith("_organizado.csv"):
                arquivos_csv.append(os.path.join(root, f))

    dfs = []
    for caminho in arquivos_csv:
        print(f"Lendo {caminho}...")
        df = pd.read_csv(caminho, low_memory=False)
        dfs.append(df)

    if not dfs:
        print("Nenhum arquivo organizado encontrado para empilhar.")
        return None

    dados_empilhados = pd.concat(dfs, ignore_index=True)
    os.makedirs(pasta_empilhados, exist_ok=True)
    caminho_saida = os.path.join(pasta_empilhados, "PNAD_empilhada.csv")
    dados_empilhados.to_csv(caminho_saida, index=False)
    print(f"\nDados empilhados salvos em: {caminho_saida}")
    print(f"Total de linhas: {dados_empilhados.shape[0]}")
    return caminho_saida

# Execucao principal
if __name__ == "__main__":
    # 1) Baixar e descompactar por ano
    for ano in anos_teste:
        baixar_ano(ano)

    # 2) Processar (tratar) todos os .txt encontrados em dados_descompactados
    for root, dirs, files in os.walk(pasta_descompactados):
        for f in files:
            if f.endswith(".txt"):
                caminho_txt = os.path.join(root, f)
                ano_folder = os.path.basename(root)
                tratar_dados(caminho_txt, ano_folder)

    # 3) Empilhar organizados
    caminho_empilhado = empilhar_dados(pasta_organizados_csv)

    # 4) Calcular estatísticas trimestrais
    from pnad_estatisticas import calcular_estatisticas
    pasta_resultados_est = os.path.join(diretorio_raiz, "estatisticas_trimestrais")
    os.makedirs(pasta_resultados_est, exist_ok=True)

    resumo_por_ano = {}

    # Separar estatisticas por ano
    for ano in anos_teste:

        ano_folder = ano_para_pasta(ano)

        # Pasta especifica do ano
        pasta_ano_est = os.path.join(
            pasta_resultados_est,
            ano_folder
        )

        os.makedirs(
            pasta_ano_est,
            exist_ok=True
        )

        # CSVs organizados daquele ano
        pasta_csv_ano = os.path.join(
            pasta_organizados_csv,
            ano_folder
        )

        print(f"\nCalculando estatisticas para {ano_folder}...")

        resumo = calcular_estatisticas(
            pasta_csv_ano,
            pasta_ano_est
        )

        resumo_por_ano[ano_folder] = resumo

    # Exibir resultados
    print("\nArquivos de estatisticas gerados:")

    for ano_key, resumo in resumo_por_ano.items():

        if resumo.get('combinado'):

            print(
                f" - {ano_key} combinado: "
                f"{resumo['combinado']}"
            )

        for chave, caminho in resumo.get('por_ano', {}).items():

            print(f" - {ano_key}: {caminho}")

    print("\nProcesso completo!")