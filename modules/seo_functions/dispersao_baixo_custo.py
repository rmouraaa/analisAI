import pandas as pd


def dispersao_baixo_custo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona keywords para dispersão com baixo custo:
      1. Mantém última ocorrência de cada keyword.
      2. Filtra por Search Volume >= 15% da média do top 100.
      3. CPC > 0.01 e Number of Results entre [100, 5M].
      4. Calcula Score Estratégico vetorizado e retorna top 10.
    """
    # 1. Última ocorrência e cópia (pra evitar warnings)
    df_clean = df.iloc[::-1] \
                 .drop_duplicates(subset="Keyword", keep="first") \
                 .copy()

    # 2. Threshold de volume (>=15% da média do top 100)
    top100_vol = df_clean.nlargest(100, "Search Volume")["Search Volume"]
    media_top100 = top100_vol.mean() if not top100_vol.empty else 0
    limite_vol = media_top100 * 0.15
    filtro_vol = df_clean["Search Volume"] >= limite_vol

    # 3. Filtra CPC e Number of Results
    filtro_ruido = (
        (df_clean["CPC"] > 0.01) &
        df_clean["Number of Results"].between(100, 5_000_000)
    )

    df_filt = df_clean[filtro_vol & filtro_ruido].copy()
    if df_filt.empty:
        return df_filt

    # 4. CPC máximo do top 100 para normalização
    top100_cpc = df_filt.nlargest(100, "CPC")["CPC"]
    max_cpc = top100_cpc.max() if not top100_cpc.empty else 0

    # 5. Cálculo vetorizado do Score Estratégico
    pct_cpc = df_filt["CPC"].div(max_cpc).fillna(0)
    # pontuação da parte CPC entre 0.05 e 2.0
    peso_cpc = (2.1 - 2 * pct_cpc).clip(lower=0.05, upper=2.0)
    df_filt["Score Estratégico"] = df_filt["Search Volume"] * 3 * peso_cpc

    # 6. Ordena e pega top 10
    return df_filt.nlargest(10, "Score Estratégico")
