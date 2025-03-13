import consts
import utils

if __name__ == '__main__':
    # Import & filter the csv files
    df_raw = utils.load_raw_data(True, True)

    # Remove missing values
    df_sanitized = utils.remove_invalid_ages(utils.remove_age_na(df_raw))

    # Partition df according to direction of traffic
    outbound_df, inbound_df, inner_df = utils.traffic_based_partition(df_raw)

    print(f"Outbound total: {outbound_df["personas"].sum()}")
    print(f"Inbound total: {inbound_df["personas"].sum()}")
    print(f"Inner total: {inner_df["personas"].sum()}")
