import pandas as pd


def demanda_qualificada(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Retorna as top N keywords informacionais com alto volume,
    CPC estratégico baseado na mediana dinâmica (calculada internamente),
    e presença estratégica nas SERPs.

    Parâmetros:
    -----------
    df : pd.DataFrame
        DataFrame contendo as colunas necessárias:
        - 'Keyword'
        - 'Keyword Intents'
        - 'Search Volume'
        - 'CPC'
        - 'SERP Features by Keyword'

    top_n : int
        Número de resultados para retornar (default=10).

    Retorna:
    --------
    pd.DataFrame
        DataFrame filtrado, ordenado e limitado às top N keywords.
    """

    # Calcula internamente o CPC mediano das 100 keywords com maior volume
    cpc_threshold = df.nlargest(100, 'Search Volume')['CPC'].median()

    # Aplica filtros estratégicos diretamente
    df_filtered = df[
        (df["Keyword Intents"].str.lower().str.contains("informational", na=False)) &
        (df["Search Volume"] > 2000) &
        (df["CPC"] <= cpc_threshold) &  # CPC estratégico (mediana)
        (df["CPC"] > 0) &  # exclui keywords com CPC zero (sem valor comercial)
        (df["SERP Features by Keyword"]
            .str.contains("Video|People also ask|Featured Snippet", case=False, na=False))
    ]

    # Remove duplicatas mantendo o último registro
    df_unique = df_filtered.drop_duplicates(subset=["Keyword"], keep='last')

    # Ordenação estratégica (alto volume e CPC equilibrado)
    df_sorted = df_unique.sort_values(
        by=["Search Volume", "CPC"],
        ascending=[False, True]
    )

    # Retorna o top N resultados
    return df_sorted.head(top_n)
