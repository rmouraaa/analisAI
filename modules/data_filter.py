import pandas as pd


def dispersao_baixo_custo(df: pd.DataFrame) -> pd.DataFrame:
    # Filtros básicos de qualidade
    df = df[
        (df["Search Volume"] > 1000) &
        (df["CPC"] > 0.01) &
        (df["Number of Results"] > 100) &
        (df["CPC"] < 0.2) &
        (df["Number of Results"] < 5000000)
    ]

    # Inverter a ordem para manter o último índice de cada keyword
    df = df[::-1]

    # Remove duplicatas mantendo a última ocorrência (maior índice)
    df = df.drop_duplicates(subset=["Keyword"], keep='first')

    # Reordenar para exibir o top 10 mais estratégico
    df = df.sort_values(
        by=["Number of Results", "Search Volume", "CPC"], ascending=[True, False, True])

    return df.head(10)


def dominio_de_marca(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Position"] <= 3) &
        (df["Keyword Intents"].str.lower().str.contains("navigational")) &
        (df["Search Volume"] > 300)
    ]

    # Inverter a ordem para manter a última ocorrência
    df = df[::-1]

    # Remove duplicatas mantendo a última
    df = df.drop_duplicates(subset=["Keyword"], keep='first')

    # Ordenar pela relevância
    df = df.sort_values(by=["Traffic", "Search Volume"],
                        ascending=[False, False])

    return df.head(10)


def oportunidade_crescimento(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Position"] >= 5) &
        (df["Position"] <= 20) &
        (df["Search Volume"] > 2000) &
        (df["CPC"] > 0.01) &
        (df["Number of Results"] > 100)
    ]

    # Inverter para manter o último índice em caso de duplicata
    df = df[::-1]

    # Remove duplicatas mantendo a última
    df = df.drop_duplicates(subset=["Keyword"], keep="first")

    # Ordena por oportunidade: mais próximo do topo, maior volume e menor CPC
    df = df.sort_values(by=["Position", "Search Volume",
                        "CPC"], ascending=[True, False, True])

    return df.head(10)


def demanda_qualificada(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Keyword Intents"].str.lower().str.contains("informational")) &
        (df["Search Volume"] > 2000) &
        (df["CPC"] > 0.01) &
        (df["Number of Results"] > 100) &
        (df["SERP Features by Keyword"].str.contains(
            "Video|People also ask", case=False, na=False))
    ]

    # Inverter para manter o último índice
    df = df[::-1]

    # Remover duplicatas mantendo o último
    df = df.drop_duplicates(subset=["Keyword"], keep='first')

    # Ordenar por interesse e viabilidade
    df = df.sort_values(by=["Search Volume", "CPC"], ascending=[False, True])

    return df.head(10)


def aposta_nicho(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Search Volume"] >= 500) &
        (df["Search Volume"] <= 3000) &
        (df["CPC"] >= 0.01) &
        (df["CPC"] <= 0.20) &
        (df["Keyword Difficulty"] < 35) &
        (df["Number of Results"] < 1_000_000)
    ]

    # Inverter para manter última ocorrência em caso de duplicata
    df = df[::-1]
    df = df.drop_duplicates(subset=["Keyword"], keep="first")

    df = df.sort_values(
        by=["Keyword Difficulty", "Search Volume", "CPC"],
        ascending=[True, False, True]
    )

    return df.head(10)


def apoio_conversao(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Keyword Intents"].str.lower().str.contains("commercial")) &
        (df["Position"] <= 10) &
        (df["Search Volume"] > 2000) &
        (df["CPC"] > 0.01) &
        (df["Number of Results"] > 100) &
        (df["SERP Features by Keyword"].str.contains(
            "Video|Reviews", case=False, na=False))
    ]

    # Manter últimas ocorrências únicas
    df = df[::-1]
    df = df.drop_duplicates(subset=["Keyword"], keep="first")

    # Ordenar por conversão potencial
    df = df.sort_values(by=["Position", "Search Volume",
                        "CPC"], ascending=[True, False, True])

    return df.head(10)


def reconhecimento_com_midia(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Keyword Intents"].str.lower().str.contains("informational")) &
        (df["Search Volume"] > 2000) &
        (df["CPC"] > 0.01) &
        (df["Number of Results"] > 100) &
        (df["SERP Features by Keyword"].str.contains(
            "Image|Video|Knowledge panel", case=False, na=False))
    ]

    df = df[::-1]
    df = df.drop_duplicates(subset=["Keyword"], keep="first")

    df = df.sort_values(by=["Search Volume", "CPC"], ascending=[False, True])

    return df.head(10)
