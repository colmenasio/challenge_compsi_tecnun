import os
import pandas as pd

class IdResolver:
    names_path = "../data/nombres_distritos.csv"
    population_path = "../data/poblacion_distritos.csv"

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        if not os.path.exists(self.names_path) or not os.path.exists(self.population_path):
            raise FileNotFoundError(f"{self.names_path} or {self.population_path} not found")
        self.df = pd.concat([
            pd.read_csv(self.names_path, sep="|", index_col="ID"),
            pd.read_csv(self.population_path, sep="|", index_col=0, names=["population"])],
            axis=1
        )

        self._initialized = True

    def resolve_name(self, id: str):
        return self.df.loc[id, "name"]

    def resolve_population(self, id: str):
        return self.df.loc[id, "population"]


    def __repr__(self):
        return super().__repr__() + f"\nNames and population dataframe: \n{self.df}\n\n"
