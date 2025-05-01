import pandas as pd


def apoio_conversao(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Keyword Intents"].str.lower().str.contains("commercial")) &
        (df["Position"] <= 10) &
        (df["Search Volume"] > 2000) &
        (df["CPC"] > 0.01) &
        (df["Number of Results"] > 100) &
        (df["SERP Features by Keyword"]
         .str.contains("Video|Reviews", case=False, na=False))
    ]
    df = df[::-1]
    df = df.drop_duplicates(subset=["Keyword"], keep="first")
    df = df.sort_values(by=["Position", "Search Volume",
                        "CPC"], ascending=[True, False, True])
    return df.head(10)
