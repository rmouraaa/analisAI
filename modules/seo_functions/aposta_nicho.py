import pandas as pd


def aposta_nicho(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Seleciona keywords estratégicas para nichos com critérios totalmente dinâmicos 
    baseados em estatísticas internas do DataFrame fornecido.

    Parâmetros:
    -----------
    df : pd.DataFrame
        DataFrame contendo as colunas:
        - 'Keyword'
        - 'Search Volume'
        - 'CPC'
        - 'Keyword Difficulty'
        - 'Number of Results'

    top_n : int
        Número de resultados a retornar (default=10).

    Retorna:
    --------
    pd.DataFrame
        Top N keywords estratégicas filtradas dinamicamente.
    """

    # Cálculo dinâmico dos limites com percentis e medianas
    vol_min, vol_max = df["Search Volume"].quantile([0.25, 0.75])
    cpc_med, cpc_max = df["CPC"].quantile([0.5, 0.75])
    kd_max = df["Keyword Difficulty"].quantile(0.5)
    results_max = df["Number of Results"].quantile(0.5)

    # Filtros dinâmicos aplicados diretamente
    df_filtered = df[
        (df["Search Volume"].between(vol_min, vol_max)) &
        (df["CPC"].between(cpc_med, cpc_max)) &
        (df["Keyword Difficulty"] <= kd_max) &
        (df["Number of Results"] <= results_max)
    ]

    # Remove duplicatas mantendo o último registro
    df_unique = df_filtered.drop_duplicates(subset=["Keyword"], keep="last")

    # Ordenação estratégica
    df_sorted = df_unique.sort_values(
        by=["Keyword Difficulty", "Search Volume", "CPC"],
        ascending=[True, False, True]
    )

    return df_sorted.head(top_n)
