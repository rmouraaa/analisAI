import pandas as pd


def oportunidade_crescimento(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Position"] >= 5) &
        (df["Position"] <= 20) &
        (df["Search Volume"] > 2000) &
        (df["CPC"] > 0.01) &
        (df["Number of Results"] > 100)
    ]
    df = df[::-1]
    df = df.drop_duplicates(subset=["Keyword"], keep="first")
    df = df.sort_values(
        by=["Position", "Search Volume", "CPC"],
        ascending=[True, False, True]
    )
    return df.head(10)
