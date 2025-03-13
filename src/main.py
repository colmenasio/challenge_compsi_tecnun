import utils
import pre_processing

if __name__ == '__main__':
    # Import & filter the csv files
    df = utils.load_raw_data(True, True)

    # Remove missing values
    df_sanitized = pre_processing.remove_age_na(df)
    df_sanitized = pre_processing.remove_invalid_ages(df_sanitized)

    #

    utils.summary(df)
