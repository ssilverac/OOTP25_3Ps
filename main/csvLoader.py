import os
import pandas as pd

class csvLoader:
    def __init__(self, filename):
        self.filename = filename

    def csv_to_df(self):
        df = pd.read_csv(self.filename)
        print(f'Loading {self.filename} and converting to DataFrame')
        print(df)
        return df

roster = csvLoader('../data/cleaned/2025/masterRoster.csv')

master_roster = roster.csv_to_df()
print(master_roster)
