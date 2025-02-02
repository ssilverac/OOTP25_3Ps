import os
import pandas as pd

class csvLoader:
    def __init__(self, filename):
        self.filename = filename
        

    def csv_to_df(self):
        df = pd.read_csv(self.filename)
        print(f'\nLoading "{self.filename}" and converting to DataFrame\n')
        
        return df


def create_df(data, column_names):
    df = pd.DataFrame(data, columns=column_names)
    return df