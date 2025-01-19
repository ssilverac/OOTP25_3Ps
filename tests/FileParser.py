import pandas as pd
import os
import re
import numpy as np

DATA_PATH = '../data/raw/2025_stats/league_stats'
SAVE_PATH = '../data/cleaned/2025'

class FileParser:
    def __init__(self, input_filename):
        '''
        input_filename: str
            This is the path to the file you wish to load and parse.
        These files were all downloaded from OOTP25 so the format of each
        file is very similar

        '''
        self.input_filename = input_filename

    def parse_file(self):
        team_section = False
        player_section = False
        header_section = False

        team_data = []
        player_data = []
        headers = []

        with open(self.input_filename, 'r') as file:
            file = file.read()
            content = file.strip().replace('eol', '').split('\n')

            for line in content:
                if line.startswith('// List'):
                    team_section = True


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
                        headers = line

                if player_section:
                    line = line.replace('eol\n', '').split(',')
                    player_data.append(line)

                #clean player data
            cleaned_player_data = []
            for player in player_data:
                cleaned_player = [np.nan if item =='' else item for item in player]
                # Drop final category since its irrelevant
                # Droping this also makes sure this will match up with the headers
                cleaned_player = cleaned_player[:-1]
                cleaned_player_data.append(cleaned_player)
        print('File successfully Parsed')
        return team_data, cleaned_player_data, headers

    def create_df(self, team_data, cleaned_player_data, headers):
        #create df out of headers list
        player_df = pd.DataFrame(cleaned_player_data, columns=headers)

        #create master roster for each player and corresponding id
        player_roster = player_df[['id', 'LastName', 'FirstName', 'TeamName', 'team_id']].set_index('id')

        #convert list to dict and drop last 2 entries
        team_dict = dict(item.split(':') for item in team_data[:-2])
        team_dict = pd.DataFrame([team_dict])

        return player_df, player_roster, team_dict

    def save_df(self, data, output_path):
        data.to_csv(output_path, index=False)
        print(f'DataFrame Saved to {output_path}')


file_name = 'abl_rosters.txt'

#Initiate class
parser = FileParser(os.path.join(DATA_PATH, file_name))

#Parse the file
team_data, cleaned_player_data, headers = parser.parse_file()

#Create DataFrame
player_stats, player_roster, team_dict = parser.create_df(team_data, cleaned_player_data, headers)

#Save DataFrame
output_master_roster_path = os.path.join(SAVE_PATH, 'masterRoster.csv')
parser.save_df(player_roster, output_master_roster_path)

output_master_teamID_path = os.path.join(SAVE_PATH, 'output_master_teamID.csv')
parser.save_df(team_dict, output_master_teamID_path)

player_statistics_path = os.path.join(SAVE_PATH, 'player_stats.csv')
parser.save_df(player_stats, player_statistics_path)

print(player_roster.head(50))
