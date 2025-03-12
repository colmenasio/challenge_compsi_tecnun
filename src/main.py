import pandas as pd

from consts import data_paths
from filter import import_csv

def load_raw_data(from_pkl: bool, verbose: bool = False) -> pd.DataFrame:
    pkl_path = "../data/filtered_raw.pkl"
    if from_pkl:
        df = pd.read_pickle(pkl_path)
    else:
        df = import_csv(data_paths, [str(x) for x in range(2006901, 2006908)])

    if verbose:
        print(df.head())
        print(df.shape)
        print(df.dtypes)

    if not from_pkl :
        df.to_pickle(pkl_path)

    return df



if __name__ == '__main__':
    # Import & filter the csv files
    df = load_raw_data(False, True)




