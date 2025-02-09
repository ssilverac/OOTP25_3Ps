import pandas as pd
from FileParser import FileParser
from fileLog import config_log
from utils import create_df
import logging
import re

config_log('app.log')

with open('../data/raw/abl_rosters.txt', 'r') as file:
    content = file.readlines()

    player_stats = []

    for i in content:

        if i.startswith('//id'):
           headers = i.strip('/').strip()
           logging.info(f'Raw Headers: {repr(headers)}')
        
           headers_list = [col.strip() for col in headers.split(',')]
           logging.info(f'Cleaned headers list {repr(headers_list)}')
        
        pattern = r'^\d+'
        if re.match(pattern, i):
            i = i.replace('eol', '').strip()
            i = i.split(',')
            i = i[:-1]
            

            player_stats.append(i)
            
    
    headers_list = headers.split(',')


    player_stats = [row[:len(headers_list)] for row in player_stats]


    df = create_df(player_stats, headers_list)
    df.columns = df.columns.str.strip()

    df = df[['id', 'team_id', 'Team Name', 'League Name', 'LastName', 'FirstName', 'Bats', 'Throws', 'Position']]
    logging.info(df.head())
    
    df.rename(columns={'id':'Player ID', 'team_id': 'Team ID', 'LastName': 'Last Name', 'FirstName': 'First Name'}, inplace=True)
    logging.info(df.head())

    df.to_csv('../data/cleaned/master_roster.csv', index=False)
    



  