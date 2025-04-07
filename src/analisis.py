import utils
from id_resolver import IdResolver

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as sts

def common_preprocessing(df_raw: pd.DataFrame) -> pd.DataFrame:
    # Remove missing values and expand the df
    df = utils.remove_invalid_ages(utils.remove_age_na(df_raw))
    df = utils.expand(df, in_place=False)
    ids_resolver = IdResolver()

    # Encodings
    df["poblacion_origen"] = df["origen"].apply(lambda x: ids_resolver.resolve_population(x))
    df = df[df["poblacion_origen"] != 0]
    df['sexo_encoded'] = df['sexo'].map({'hombre': 0, "H": 0, 'mujer': 1, "M": 1})

    # For debugging
    # # print(df.isna().sum())
    # # print(df[df.isna().any(axis=1)])
    return df

def simple_linear_regression(df_preprocessed: pd.DataFrame, target: str) -> None:
    # Select features and target
    features = df_preprocessed[["poblacion_origen", "avrg_age", "residencia", "sexo_encoded", "month", "years"]]
    features = sm.add_constant(features)
    target = df_preprocessed[target]

    # Solve the Model
    model = sm.OLS(target, features).fit()
    print(model.summary())

    return None

def simple_polynomial_regression(df_preprocessed: pd.DataFrame, target: str):
    features = df_preprocessed[["poblacion_origen", "avrg_age", "residencia", "sexo_encoded", "month", "years"]]
    features = sm.add_constant(features)
    target = df_preprocessed[target]

    # Solve the Model
    model = sm.OLS(target, features).fit()
    print(model.summary())

    return None

if __name__ == '__main__':
    df_raw = utils.load_raw_data(True, True)
    df = common_preprocessing(df_raw)
    print(40*"-"), print("SUMMARY OF THE DF BEFORE REGRESSION\n\n"), utils.summary(df), print(40*"-")

    # # FIRST ATTEMPT AT A REGRESSION
    #simple_linear_regression(df, "avrg_displacements")

    # # RESULTS
    # The kurtosis is OVER THE ROOF (almost 40)
    # Also the data is HIGHLY skewed (almsot 5).
    # # plt.hist(df["avrg_displacements"], density = True, bins = 100)
    # # plt.show()

    # Está claro el problema. Hay que turbonomalizar ya de ya
    # Aplicamos una transformada box-cox
    opt_lambda = sts.boxcox_normmax(df["avrg_displacements"], method="mle")
    df["avrg_displacements_transformed"] = sts.boxcox(df["avrg_displacements"], opt_lambda)
    plt.hist(df["avrg_displacements_transformed"], density = True, bins = 100)
    plt.show()

    # Hay multiple picos, deberiamos clusterer. Hacemos un pequeño analisis tontorrón pa ver que tal
    simple_linear_regression(df, "avrg_displacements_transformed")
    # Es kinda decente, igual en un futuro cunde clusterear, pero por ahora esta dpm
