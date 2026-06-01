import pandas as pd
import os


def organizar_pnad(caminho_txt, saida_csv_dir):
    """
    Lê o arquivo TXT da PNAD Contínua,
    extrai apenas as variáveis da base definitiva,
    normaliza os pesos amostrais
    e salva a base organizada em CSV.
    """

    print(f"Lendo arquivo bruto: {caminho_txt}")

    layout_definitivo = {
        "variavel": [
            "Ano",
            "Trimestre",
            "UF",
            "V1028",
            "V2007",
            "V2009",
            "V2010",
            "V3009A",
            "V3014",
            "V4001",
            "V4010",
            "V4012",
            "V4013",
            "V4028",
            "V4029",
            "V403312",
            "V4039",
            "V4040",
            "V4071"
        ],

        "start": [
            1,    # Ano
            5,    # Trimestre
            17,   # UF
            44,   # V1028
            89,   # V2007
            98,   # V2009
            101,  # V2010
            119,  # V3009A
            129,  # V3014
            130,  # V4001
            146,  # V4010
            150,  # V4012
            152,  # V4013
            188,  # V4028
            189,  # V4029
            194,  # V403312
            235,  # V4039
            241,  # V4040
            370   # V4071
        ],

        "width": [
            4,   # Ano
            1,   # Trimestre
            2,   # UF
            15,  # V1028
            1,   # V2007
            3,   # V2009
            1,   # V2010
            2,   # V3009A
            1,   # V3014
            1,   # V4001
            4,   # V4010
            1,   # V4012
            5,   # V4013
            1,   # V4028
            1,   # V4029
            8,   # V403312
            3,   # V4039
            1,   # V4040
            1    # V4071
        ]
    }

    layout = pd.DataFrame(layout_definitivo)

    fwf_cols = list(
        zip(
            layout["start"] - 1,
            layout["start"] - 1 + layout["width"]
        )
    )

    df = pd.read_fwf(
        caminho_txt,
        colspecs=fwf_cols,
        names=layout["variavel"],
        dtype=str,
        encoding="latin1"
    )

    print(
        f"Arquivo carregado: "
        f"{df.shape[0]} linhas, "
        f"{df.shape[1]} colunas"
    )

    # Remover espaços residuais
    for col in df.columns:
        df[col] = df[col].str.strip()

    # Converter para numérico
    for col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Normalização do peso amostral
    if "V1028" in df.columns:

        max_peso = df["V1028"].max(skipna=True)

        if pd.notna(max_peso) and max_peso > 1_000_000:
            df["V1028"] = df["V1028"] / 100_000_000

    # Filtro Pernambuco
    if "UF" in df.columns:

        df = df[df["UF"] == 26]

        print(
            f"Filtrado para Pernambuco: "
            f"{df.shape[0]} linhas restantes."
        )

    nome_base = os.path.splitext(
        os.path.basename(caminho_txt)
    )[0]

    caminho_saida_csv = os.path.join(
        saida_csv_dir,
        f"{nome_base}_organizado.csv"
    )

    # Mantém ';' para compatibilidade com Excel/LibreOffice
    df.to_csv(
        caminho_saida_csv,
        sep=";",
        index=False,
        encoding="utf-8"
    )

    print(
        f"Arquivo CSV salvo em: "
        f"{caminho_saida_csv}"
    )

    return caminho_saida_csv