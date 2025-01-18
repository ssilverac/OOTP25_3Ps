import pandas as pd
import re
import os

DATA ='../data/raw/2025_stats/league_stats/abl_rosters.txt'

def preprocess_data(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
        cleaned_content = content.strip().replace('eol', '').split('\n')
        for line in cleaned_content:
            if line.startswith('/'):
                print (line)


preprocess_data(DATA)
