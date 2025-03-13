import pandas as pd

def remove_invalid_ages(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(
        df[df["edad"] == pd.Interval(-1, -1)].index,
        inplace=False
    )

def remove_age_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(
        axis="rows",
        inplace=False
    )