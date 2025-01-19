'''
This function was created to clean the raw textfiles acquired directly from OOTP25 and parsed to created
useful pandas dataframes for processing later on.
One file was used titled abl_roster.txt and from this file 3 dataframes where created.
One titled team_data which was used to create the master_roster.csv and the other one created the teamid_master.csv.
The master roster contains the names, ID, team and team ID for each player in the league. the teamid_master.csv contains
the list of each team and their corresponding ID.

These files can then be used to cross-reference performance statistics to match an id to a specific player,
as those files do not contain team names or player names.
'''

import pandas as pd
import os
import re
import numpy as np

DATA ='../data/raw/2025_stats/league_stats/abl_rosters.txt'
SAVE_PATH = '../data/cleaned'

def parse_file(filename):
    team_section = False
    player_section = False
    header_section = False
    team_data = []
    player_data = []
    headers = []

    with open(filename, 'r') as file:
        file = file.read()
        content = file.strip().replace('eol', '').split('\n')
        for line in content:

            if line.startswith('// List'):
                team_section = True
                continue

            elif line.startswith('//id'):
                header_section = True
                team_section = False

            elif line[0].isdigit():
                player_section = True
                team_section = False
                header_section = False

            if team_section:
                line = line.strip('/').replace(' => ID of ', ':')
                line = line.replace('\n', '')
                team_data.append(line)

            if header_section:
                if line.startswith('//id'):
                    line = line.strip('/').replace(' ', '').split(',')
                    headers.append(line)


            if player_section:
                line = line.replace('eol\n', '').split(',')
                player_data.append(line)

        cleaned_player_data = []
        for player in player_data:
            cleaned_player = [np.nan if item == '' else item for item in player]
            cleaned_player = cleaned_player[:-1]
            cleaned_player_data.append(cleaned_player)




    return team_data, cleaned_player_data, headers


team_data, player_data, headers = parse_file(DATA)

#create df out of list using headers as column titles
df = pd.DataFrame(player_data, columns=headers)

#create a master roster of each player and their corresponding id
player_roster = df[['id', 'LastName', 'FirstName', 'TeamName', 'team_id']]
player_roster.set_index('id')
print(player_roster)
player_roster.to_csv(os.path.join(SAVE_PATH, 'master_roster.csv'))


#remove last two entries, since they are empty and create a dict
team_dict = dict(item.split(':') for item in team_data[:-2])
team_dict = pd.DataFrame([team_dict])
team_dict.to_csv(os.path.join(SAVE_PATH, 'teamid_master.csv'), index=False)
