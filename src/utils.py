from typing import Tuple

import pandas as pd

import filter
import consts

def summary(df: pd.DataFrame) -> None:
    print(df.head())
    print(df.shape)
    print(df.dtypes)

def load_raw_data(from_pkl: bool, verbose: bool = False) -> pd.DataFrame:
    pkl_path = "../data/filtered_raw.pkl"
    if from_pkl:
        df = pd.read_pickle(pkl_path)
    else:
        df = filter.import_csv(consts.data_paths, [str(x) for x in consts.donostia_ids])

    if verbose:
        summary(df)

    if not from_pkl :
        df.to_pickle(pkl_path)

    return df

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

def traffic_based_partition(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Returns (outbound, inbound, inner)"""
    outbound_df = df[~df['destino'].isin(consts.donostia_ids)]
    inbound_df = df[~df['origen'].isin(consts.donostia_ids)]
    inner_traffic_df = df[df['destino'].isin(consts.donostia_ids) & df['origen'].isin(consts.donostia_ids) ]
    assert df.shape[0] == outbound_df.shape[0] + inbound_df.shape[0] + inner_traffic_df.shape[0]
    return outbound_df, inbound_df, inner_traffic_df