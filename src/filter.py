import pandas as pd
from io import StringIO

def get_converters():
    def to_range(i_input: str):
        if not isinstance(i_input, str):
            return pd.Interval(left=-1, right=-1)
        elif len(i_input) == 0 or i_input == "NA":
            return pd.Interval(left=-1, right=-1)
        elif "-" in i_input:
            return pd.Interval(left=int(i_input.split("-")[0]), right=int(i_input.split("-")[1]))
        else:
            return pd.Interval(left=int(i_input), right=int(i_input))
    return {
        "edad": lambda x:  to_range(x),
        "recurrencia": lambda x: to_range(x)
    }

def get_dtype_dict():
    return {
        "origen": "string",
        "destino": "string",
        "sexo": "string"
    }

def filter_read_csv(path:str, relevant_ids: list[str]) -> pd.DataFrame:
    # Read csv in chunks
    chunks = pd.read_csv(path,
                         chunksize=1000,
                         sep="|",
                         converters=get_converters(),
                         dtype=get_dtype_dict()
                         )

    # Filter dataframe to have only relevant rows
    filtered_data = pd.concat(
        [chunk[chunk.apply(
            lambda row: (row["origen"] in relevant_ids or row["destino"] in relevant_ids),
            axis=1
        )] for chunk in chunks]
    )
    return filtered_data


def import_csv(sources : str | list[str], relevant_ids: list[str]) -> pd.DataFrame:
    # Sanitize input
    if isinstance(sources, str):
        sources =  [sources]

    # Read files
    dfs = []
    for source in sources:
        print(f"[INFO] Reading {source}")
        dfs.append(filter_read_csv(source, relevant_ids))

    # Return the concatenated input
    df = pd.concat(dfs)
    #df.reset_index()
    return df