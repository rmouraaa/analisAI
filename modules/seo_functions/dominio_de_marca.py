import pandas as pd


def dominio_de_marca(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        (df["Position"] <= 3) &
        (df["Keyword Intents"].str.lower().str.contains("navigational")) &
        (df["Search Volume"] > 300)
    ]
    df = df[::-1]
    df = df.drop_duplicates(subset=["Keyword"], keep='first')
    df = df.sort_values(by=["Traffic", "Search Volume"],
                        ascending=[False, False])
    return df.head(10)
