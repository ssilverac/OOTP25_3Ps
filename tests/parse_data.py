
import pandas as pd
import os
import re

DATA ='../data/raw/2025_stats/league_stats/abl_rosters.txt'

def parse_file(filename):
    with open (filename, 'r') as file:
        team_section = False
        player_section = False
        header_section = False
        team_data = {}
        player_data = []
        headers = []

        for line in file:

            if line.startswith('//id'):

                headers.append(line.strip('//')) #clean header line

                header_section= True

                print(headers)
                continue
            if line.startswith('// List of Teams'):
                print('Team section started')
                team_section = True
                continue
            if team_section and line.startswith('//'):
                print(line)
                print(f'Team line found: {line}')
                line = line.strip('//').split(',') #split team info
                print(f'Split line: {line}')
                if len(line) == 2: #ensure t he line has valid data
                    team_name = line[0].strip()
                    print(f'Team Name: {team_name}')
                    team_id_match = line[1].strip()
                    print(f'Team ID Match: {team_id_match}')
                    if team_id_match:
                        team_id = int(team_id_match.group(1))
                        print(f'Team ID: {team_id}')
                        team_data[team_id] = team_name
                        print(f'Added to team_data: {team_id} -> {team_name}')
        return team_data, headers


'''
            if line.startswith('//id'):
                line = line.strip('//')
                headers.append(line)

            elif line.startswith('// List of Teams'):
                continue
            elif line.startswith('// '):
                line = line.strip('// ').split(',')
                if len(line) == 2:
                    line[1] = line[1].strip('ID = ')
                    keys = line[1]
                    values = line[0]


                    print('Keys')
                    print(keys)
                    print('\n')
                    print('Values')
                    print(values)
                    print('\n')




        return team_data

'''


team, headers = parse_file(DATA)
print('Team Data:')
for k, v in team.items():
    print(f'ID: {k}, Name: {v}')

'''
print('********************************************************')
print(team)
print('********************************************************')
print(header)
'''
