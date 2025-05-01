import pandas as pd


def aposta_nicho(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Search Volume"] >= 500) &
        (df["Search Volume"] <= 3000) &
        (df["CPC"] >= 0.01) &
        (df["CPC"] <= 0.20) &
        (df["Keyword Difficulty"] < 35) &
        (df["Number of Results"] < 1_000_000)
    ]
    df = df[::-1]
    df = df.drop_duplicates(subset=["Keyword"], keep="first")
    df = df.sort_values(
        by=["Keyword Difficulty", "Search Volume", "CPC"],
        ascending=[True, False, True]
    )
    return df.head(10)
