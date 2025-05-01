import pandas as pd
import numpy as np


def oportunidade_crescimento(df: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona keywords com maior oportunidade de crescimento, 
    priorizando quem está perto do top mas perdeu terreno:
      - Position entre 5 e 20.
      - Search Volume ≥15% da média do top100.
      - CPC > 0.01.
      - Peso de CPC: exp(-β·(CPC/max_CPC_top100)).
      - Peso de posição: linear de 1 em pos=5 até 0 em pos=20.
      - Peso delta (perda de terreno): 1 + α·(delta_pos/max_delta).
      - Penalidade de competição: log10(Nº de resultados) normalizado.
      - Score = vol_norm * peso_cpc * peso_pos * peso_delta - penalidade.
    """
    # 1. Filtra Position e Volume > 0, mantém última ocorrência
    df0 = (
        df[df["Position"].between(5, 20) & (df["Search Volume"] > 0)]
        .iloc[::-1]
        .drop_duplicates("Keyword", keep="first")
        .copy()
    )
    if df0.empty:
        return df0

    # 2. Threshold dinâmico de Search Volume
    top100 = df0.nlargest(100, "Search Volume")["Search Volume"]
    limiar = (top100.mean() * 0.15) if not top100.empty else 0
    df1 = df0[df0["Search Volume"] >= limiar].copy()
    if df1.empty:
        return df1

    # 3. Filtra CPC mínimo
    df1 = df1[df1["CPC"] > 0.01].copy()
    if df1.empty:
        return df1

    # 4. Normaliza Search Volume para [0,1]
    vmin, vmax = df1["Search Volume"].min(), df1["Search Volume"].max()
    df1["vol_norm"] = (
        (df1["Search Volume"] - vmin) / (vmax - vmin)
        if vmax > vmin else 1
    )

    # 5. Peso de CPC (decaimento exponencial)
    max_cpc = df1["CPC"].nlargest(100).max()
    pct_cpc = df1["CPC"].div(max_cpc).fillna(0)
    beta = 2.0
    df1["peso_cpc"] = np.exp(-beta * pct_cpc)

    # 6. Peso de posição (1 em pos=5 → 0 em pos=20)
    df1["peso_pos"] = 1 - ((df1["Position"] - 5) / 15)
    df1["peso_pos"] = df1["peso_pos"].clip(0, 1)

    # 7. Bônus de delta_pos (quem perdeu terreno ganha mais atenção)
    delta = (df1["Position"] - df1.get("Previous Position",
             df1["Position"])).clip(lower=0)
    max_delta = delta.max() if delta.max() > 0 else 1
    alpha = 0.5
    df1["peso_delta"] = 1 + alpha * (delta / max_delta)

    # 8. Penalidade de competição normalizada
    log_nr = np.log10(df1["Number of Results"].clip(lower=1))
    max_log = log_nr.max() if not log_nr.empty else 1
    df1["penalidade"] = log_nr.div(max_log)

    # 9. Score final
    df1["Score Estratégico"] = (
        df1["vol_norm"]
        * df1["peso_cpc"]
        * df1["peso_pos"]
        * df1["peso_delta"]
        - df1["penalidade"]
    )

    # 10. Retorna top 10 por Score
    return df1.nlargest(10, "Score Estratégico")
