import pandas as pd


def demanda_qualificada(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Keyword Intents"].str.lower().str.contains("informational")) &
        (df["Search Volume"] > 2000) &
        (df["CPC"] > 0.01) &
        (df["Number of Results"] > 100) &
        (df["SERP Features by Keyword"]
         .str.contains("Video|People also ask", case=False, na=False))
    ]
    df = df[::-1]
    df = df.drop_duplicates(subset=["Keyword"], keep='first')
    df = df.sort_values(by=["Search Volume", "CPC"], ascending=[False, True])
    return df.head(10)
