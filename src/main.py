import consts
import utils
from src.id_resolver import IdResolver

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
    del df_raw

    print(f"Outbound total: {outbound_df["avrg_displacements"].sum()}")
    print(f"Inbound total: {inbound_df["avrg_displacements"].sum()}")
    print(f"Inner total: {inner_df["avrg_displacements"].sum()}")

    # Get all instances of travels from 01002 to 2006907
    relevant_columns = utils.get_cols_from_to(df_sanitized,"01002", "2006907")
    print(f"Relevant cols 1: \n{relevant_columns}\n Estimated {relevant_columns["avrg_displacements"].sum()} displacements\n\n")

    # Get all instances of travels from 01002 to Donostia
    relevant_columns = utils.get_cols_from_to(df_sanitized, "01002", consts.donostia_ids)
    print(f"Relevant cols 2: \n{relevant_columns}\n Estimated {relevant_columns["avrg_displacements"].sum()} displacements\n\n")
    del relevant_columns

    ###### IdConverter example use:
    resolver = IdResolver()
    print("\n\nName and population associated with id 01009_AM are:")
    print(resolver.resolve_name("01009_AM"))
    print(resolver.resolve_population("01009_AM"))