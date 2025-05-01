import pandas as pd
import numpy as np


def dominio_de_marca(df: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona keywords para reforçar domínio de marca, considerando:
      - Posições <= 3 em buscas navegacionais.
      - Filtragem dinâmica de Search Volume (>=15% da média do top 100).
      - CPC > 0.01.
      - Penalização pelo Number of Results (mais competição = score menor).
      - Bônus pra menor Keyword Difficulty (multiplicada por 0.3).
      - Score final = base_volume * peso_cpc * peso_diff - penalidade_competição.
      - Retorna top 10 por Score.
    """
    # 1. Filtra posição, intent e volume mínimo fixo
    intents = df.get("Keyword Intents", pd.Series(dtype=str)).str.lower()
    mask = (
        (df["Position"] <= 3) &
        intents.str.contains("navigational", na=False) &
        (df["Search Volume"] > 0)  # só pra garantir não ter zero antes de média
    )
    df0 = df[mask].iloc[::-1].drop_duplicates("Keyword", keep="first").copy()
    if df0.empty:
        return df0

    # 2. Threshold dinâmico de volume: >=15% da média do top100 por volume
    top100_vol = df0.nlargest(100, "Search Volume")["Search Volume"]
    vol_mean = top100_vol.mean()
    df1 = df0[df0["Search Volume"] >= vol_mean * 0.15].copy()
    if df1.empty:
        return df1

    # 3. Filtra CPC mínimo
    df1 = df1[df1["CPC"] > 0.01].copy()
    if df1.empty:
        return df1

    # 4. Normalização de CPC e cálculo de peso
    max_cpc = df1["CPC"].nlargest(100).max()
    pct_cpc = df1["CPC"].div(max_cpc).fillna(0)
    peso_cpc = (2.1 - 2 * pct_cpc).clip(lower=0.05, upper=2.0)

    # 5. Peso de Keyword Difficulty (menor = melhor):
    #    dificuldade de 0 a 100 → multiplica 0.3 → menor valor dá peso próximo de 1
    peso_diff = (1 / (1 + df1["Keyword Difficulty"] * 0.3)).clip(lower=0.05)

    # 6. Penalidade pela competição (Number of Results):
    #    usa log10 pra suavizar grandes disparidades
    penalidade = np.log10(df1["Number of Results"]).fillna(0) * 10

    # 7. Score final vetorizado
    base_vol = df1["Search Volume"] * 3
    df1["Score Estratégico"] = base_vol * peso_cpc * peso_diff - penalidade

    # 8. Ordena e retorna top 10
    return df1.nlargest(10, "Score Estratégico")
