import consts
import utils

if __name__ == '__main__':
    # Import & filter the csv files
    df_raw = utils.load_raw_data(True, True)

    # Remove missing values
    df_sanitized = utils.remove_invalid_ages(utils.remove_age_na(df_raw))

    # Further develop the dataframe
    utils.expand(df_sanitized, in_place=True)
    utils.summary(df_sanitized)

    # Partition df according to direction of traffic
    outbound_df, inbound_df, inner_df = utils.traffic_based_partition(df_sanitized)
    del df_raw, df_sanitized

    print(f"Outbound total: {outbound_df["avrg_displacements"].sum()}")
    print(f"Inbound total: {inbound_df["avrg_displacements"].sum()}")
    print(f"Inner total: {inner_df["avrg_displacements"].sum()}")
