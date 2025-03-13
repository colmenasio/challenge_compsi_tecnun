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
        df = filter.import_csv(consts.data_paths, [str(x) for x in range(2006901, 2006908)])

    if verbose:
        summary(df)

    if not from_pkl :
        df.to_pickle(pkl_path)

    return df