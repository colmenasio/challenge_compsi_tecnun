from typing import Tuple

import pandas
import pandas as pd

import filter
import consts

def summary(df: pd.DataFrame) -> None:
    pd.set_option("display.max_columns", None)
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

def expand(i_df: pd.DataFrame,
           in_place : bool = True,
           parse_date: bool = True,
           average_age: bool = True,
           average_recurrence: bool = True,
           get_number_of_displacements: bool = True,
           ) -> pd.DataFrame:
    """For average_age age must not be a NAN value"""
    if not in_place:
        df = i_df.copy()
    else:
        df = i_df

    if parse_date:
        df["years"] = df["mes"].apply(lambda x : 0 if not isinstance(x, int) or len(str(x)) != 6 else int(str(x)[0:4]))
        df["month"] = df["mes"].apply(lambda x : 0 if not isinstance(x, int) or len(str(x)) != 6 else int(str(x)[4:6]))

    if average_age:
        df["avrg_age"] = df["edad"].apply(lambda x: (max(x.left, 18) + max(x.right, 18))/2 if isinstance(x, pd.Interval) else -1)

    if average_recurrence:
        df["avrg_recurrence"] = df["recurrencia"].apply(lambda x: (x.right + x.left)/2 if isinstance(x, pd.Interval) else 1)

    if get_number_of_displacements and average_recurrence:
        df["avrg_displacements"] = df["personas"] * df["avrg_recurrence"]

    return  df

def get_cols_from_to(df: pandas.DataFrame, origen_idx: str | list[str], destino_idx: str | list[str]):
    if isinstance(origen_idx, str): origen_idx = [origen_idx]
    if isinstance(destino_idx, str): destino_idx = [destino_idx]
    relevant_cols = df[(df["origen"].isin(origen_idx)) & (df["destino"].isin(destino_idx))].copy()
    return relevant_cols