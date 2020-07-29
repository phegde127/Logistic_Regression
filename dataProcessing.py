import pandas as pd
import numpy as np

class Processing:
    def __init__(self, df, variable):
        self.df = df
        self.variable = variable

    def impute_random(self):
        self.random_sample = self.df[self.df[self.variable] != 0].sample((self.df[self.variable] == 0).sum(), random_state=0)[self.variable]
        # Indexing the sample data to merge with the dataset
        self.random_sample.index = self.df[self.df[self.variable] == 0].index
        self.df.loc[self.df[self.variable] == 0, self.variable] = self.random_sample
