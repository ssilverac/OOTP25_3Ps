import pandas as pd
import os
import numpy as np
from fileLog import get_logger
import logging

fileParser_logger = get_logger('FileParserLogger', 'fileparser.log')

class FileParser:
    '''
    A class for parsing raw data from a file. Only accepts .csv or .xlsx

    Attributes:
    ----------
    raw_data: str
        Pat to the raw data file to be loaded and processed

    Methods:
    --------
    preProcessFile(sep_char: str):
        Opens and parse the raw file and cleans its contents, making it easier to process
        further. Removes leading and trailing whitespace.
        Takes argument sep_char, which is the character will be used
        to split the file contents.

    extractSections(strip_char: str
                    start_condition: lambda function
                    end_condition: lambda function
                    clean_headers=False
                    team_id=False
                    clean_stats=False)
        Parses and extract the sections of the provided file of interest.
        Currently this function is set up to handle the 3 most relevant sections;
        Headers, team names and corresponding ID, and player statistics.
        strip_chars should be a string, which is a character that will be stripped from
        the file, such as unwanted characters, extra commas or parenthesis etc.
        start_conditon and end_condition should be provided as a lambda function. This 
        will be used to check whether the content of interest is being copied.
        clean_headers defaults to False. This should be changed to True if the goal is
        to extract the header names from the file. Same thing with team_id and clean_stats.
        Note only one of these 3 options should be set to True at a time.

        Returns parsed_list

    _cleanHeaders(parsed_list: list)
        Internal function automatically called when clean_headers=True in extractSections
        Returns a cleaned list of headers

    _cleanTeamIds(parsed_list: list)
        Internal function automatically called when team_id=True. in extractSections
        Returns dictionary, with keys as the team id and values as team name
    
    _cleanPlayerStats(parsed_list: list)
        Internal function automatically called when clean_stats=True in extractSections.
        Return cleaned nested list of player statistics.

    createStatsDf(player_stats: list
                  column_names: list)
        Takes the list containing the player statistics and creates
        a pandas DataFrame, using the list of headers as the column names.
        Returns Pandas DataFrame
    
    saveDf(df: DataFrame
           filename: str)
        takes the dataframe and saves it as a csv file at the specified filepath/filename

    '''
    def __init__(self, raw_data):
        self.processed_content = None
        self.raw_data = raw_data
    '''
    raw_data: str;
        The raw data which you wish to load and parse.
        Can be the relative path to the file.
        This class takes text file downloaded from Out of the Park Baseball 25. All these files are typically
        in the same format.
    '''

    def preProcessFile(self, sep_char):
        '''
        Parse the full file and clean up eol, and leading/trailing whitespace.
        Uses sep_char to seperate the content into iterable objects
        '''
        with open(self.raw_data, 'r') as file:

            self.processed_content = file.read().strip()
            self.processed_content = self.processed_content.replace('eol', '').split(sep_char)
            fileParser_logger.info('File successfully pre-Parsed')

    def extractSections(self, strip_chars, start_condition, end_condition, clean_headers=False, team_id=False, clean_batter_stats=False, clean_pitcher_stats=False):

        if self.processed_content is None:
            fileParser_logger.info('ValueError: No Processed content passed to function')
            raise ValueError('File content must be preprocessed first')

        fileParser_logger.info('contents passed Successfully')

        start_copying = False
        parsed_list = []

        for line in self.processed_content:
            line = line.strip(strip_chars).strip()

            #check for start of section
            if start_condition and start_condition(line):
                start_copying = True
                fileParser_logger.info(f'Start of Team Info found. Copying = {start_copying}\n')
                fileParser_logger.info(f'Line proccessed: "{line}"')
                continue

            #check for end of section
            if end_condition and end_condition(line):
                start_copying = False
                fileParser_logger.info(f'End of Team Info reached. Copying = {start_copying}\n')
                fileParser_logger.info(f'End of section reached: "{line}"')
                break

            #make sure copying only occurs within the start and end conditions
            if start_copying:
                parsed_list.append(line.strip())
                

        # clean the headers if selected
        if clean_headers:
            parsed_list = self._cleanHeaders(parsed_list)

        # clean Team IDs if selected
        if team_id:
            parsed_list = self._cleanTeamIds(parsed_list)

        #clean Player stats
        if clean_batter_stats:

            parsed_list = self._cleanBatterStats(parsed_list)
        
        if clean_pitcher_stats:
            parsed_list = self._cleanPitcherStats(parsed_list)
        
        return parsed_list

    def _cleanHeaders(self, parsed_list):
        fileParser_logger.info('_cleanHeaders function Initialized\n')
        
        cleaned_headers = []

        for item in parsed_list:
            #fileParser_logger.info(f'Length of headers prior to cleaning: {len(item)}')
            cleaned_headers.extend([i.strip() for i in item.split(',')])
        fileParser_logger.info(f'Length of Cleaned Headers: {len(cleaned_headers)}')
        
        fileParser_logger.info('Headers cleaned successfully')
        
        fileParser_logger.info(cleaned_headers)
        return cleaned_headers
        
    def _cleanTeamIds(self, parsed_list):
        '''
        Parse the stats from each player in the league

        Returns nested list.
        '''
        fileParser_logger.info('_cleanTeamIds called successfully')

        team_dict = {}
        for i in parsed_list:
            # Split and strip each part, then keep only the ID and team name
            parts = [part.strip() for part in i.split('=>')]

            # Only take the ID and team name
            if len(parts) >= 2:
                team_name = parts[1].split('(')[0].strip()
                team_id = parts[0]
                team_dict[team_id] = team_name

            else:
                fileParser_logger.warning(f'Unexpected format in line: {i}')

        return team_dict

    def _cleanBatterStats(self, parsed_list):
        fileParser_logger.info('_cleanBatterStats Initiated\n')

        team_stats = []
        
        for i in parsed_list:
            if i.strip():
                # split entry for each player
                i = i.split(',')
                
                #fix the extra column created due to the comma in the name of the specific team
                if len(i) > 38:
                    fileParser_logger.warning('Unexpected length encountered')
                    fileParser_logger.info(f'Line Prior to cleaning: {i}')
                    fileParser_logger.warning(f'Length of line prior to cleaning: {len(i)}')
                    name = i[-8].strip()
                    
                    if 'Jackson County' in name:
                        del i[-8]
                        fileParser_logger.info('Extra Entry successfully removed. Length now correct')
                        fileParser_logger.info(f'Line after cleaning: {i}')
                        fileParser_logger.info(f'Length of line after cleaning: {len(i)}')
                    else:
                        fileParser_logger.warning('Exception caught successfully')
                        fileParser_logger.warning(f'Line causing issue: {i}')
                        fileParser_logger.warning(f'Length of line causing probelm: {len(i)}')
                        raise ValueError('Extra String Unknown. Check Raw Data Carefully')
                
                cleaned_stats = [np.nan if item =='' else item for item in i]
               
                cleaned_stats = cleaned_stats[:-1]
                
                if len(cleaned_stats) != 37:
                    fileParser_logger.warning(f'Unexpected length for player stats: {len(cleaned_stats)}')
                    fileParser_logger.warning(f'cleaned stats content: \n{cleaned_stats}')
                    continue

                team_stats.append(cleaned_stats)
            else:
                fileParser_logger.warning(f'Empty or malformed entry: {i}')
        
        return team_stats

    def _cleanPitcherStats(self, parsed_list):
        fileParser_logger.info('Cleaning Pitcher Statistics')
        pitching_stats = []
        for i in parsed_list:
            if i.strip():
                
                i = i.split(',')

                if len(i) > 56:
                    name = i[-8].strip()
                    if 'Jackson County' in name:
                        fileParser_logger.info('Deleting Extra String')
                        del i[-8]
                        fileParser_logger.info(f'New Line Length: {len(i)}')
                    else:
                        fileParser_logger.warning('Exception caught successfully')
                        fileParser_logger.warning(f'Line causing issue: {i}')
                        fileParser_logger.warning(f'Length of line causing probelm: {len(i)}')
                        raise ValueError('Extra String Unknown. Check Raw Data Carefully')
                
                cleaned_stats = [np.nan if item == '' else item for item in i]
                cleaned_stats = cleaned_stats[:-1]

                if len(cleaned_stats) != 55:
                    fileParser_logger.warning('Incorrect Length in stats detected')
                    fileParser_logger.info(f'Length is: {len(cleaned_stats)}')
                    continue

                pitching_stats.append(cleaned_stats)
        return pitching_stats

    def createStatsDf(self, player_stats, column_names):
        '''
        Takes nested list from parsePlayerStats and creates a pandas
        DataFrame using the Headers from parseHeaders

        Returns pandas.DataFrame()
        '''
        player_stats_df = pd.DataFrame(player_stats, columns=column_names)
        fileParser_logger.info('player Stats created successfully')
        return player_stats_df

    def saveDf(self, df, filename):
        '''
        Saves the df into a specified file location for later retrieval
        '''
        df.to_csv(filename, index=False)
        fileParser_logger.info(f'{filename} saved Successfully')

if __name__ == '__main__':

    raw_data_path = '../data/raw/'
    save_path = '../data/cleaned'

    # Create FileParser Object
    data = FileParser(os.path.join(raw_data_path, 'player_batting_stats.txt'))
    pitch_data = FileParser(os.path.join(raw_data_path, 'player_pitching_stats.txt'))
    #Pre-process the data
    data.preProcessFile('\n')
    pitch_data.preProcessFile('\n')

    # Extract the headers
    fileParser_logger.info('clean headers called for batters stats headers\n')
    headers = data.extractSections('/', lambda line: line.startswith('FILE FORMAT:'), lambda line: line.startswith('NOTE'), clean_headers=True)
    fileParser_logger.info(len(headers))
    fileParser_logger.info('Clean headers called for pitching stats headers\n')
    pitching_headers = pitch_data.extractSections('/', lambda line: line.startswith('FILE FORMAT:'), lambda line: line.startswith('NOTE'), clean_headers=True)
    fileParser_logger.info(f'length of pitching headers: {len(pitching_headers)}')
    # Extract Team ID information
    team_id = data.extractSections('/', lambda line: line.startswith('List'), lambda line: line == '', team_id=True)
    # Convert extracted team ID (dict) to DataFrame
    team_id_df = pd.DataFrame.from_dict(team_id, orient='index', columns=['Team Name'])
    
    #reset index to make keys a column
    team_id_df.reset_index(inplace=True)
    team_id_df.rename(columns={'index': 'ID'}, inplace=True)
    # Save to CSV using saveDf
    data.saveDf(team_id_df, os.path.join(save_path, 'masterTeamID.csv'))

    # Extract the player stat section
    player_stats = data.extractSections('/', lambda line: line.startswith('NOTE'), lambda line: line is None, clean_batter_stats=True)
    pitching_stats = pitch_data.extractSections('/', lambda line: line.startswith('NOTE'), lambda line: line is None, clean_pitcher_stats=True)
    
    # Create DataFrame using the headers as the column names
    stats_df = data.createStatsDf(player_stats, headers)
    pitch_stats_df = pitch_data.createStatsDf(pitching_stats, pitching_headers)
    
    # Select relevant columns to save for batters
    columns_batters =['player ID', 'lastname', 'firstname', 'year', 'team ID', 'g', 'gs',
       'pa', 'ab', 'h', '2b', '3b', 'hr', 'rbi', 'r', 'sb', 'cs', 'bb', 'hp',
       'k', 'sh', 'sf', 'gdp', 'ibb', 'ci', 'pitches seen', 'split_id']
    
    columns_pitchers = ['player ID', 'lastname',
                        'firstname', 'year', 'team id',
                        'g', 'w', 'l', 's', 'ip', 'ha',
                        'r', 'er', 'bb', 'hp', 'k', 'bf', 'ab',
                        '1b', '2b', '3b', 'hr', 'tb', 'sh', 'sf',
                        'ci', 'iw', 'bk', 'wp', 'dp', 'qs', 'svopp',
                        'blownsv', 'holds', 'sb', 'cs', 'gb', 'fb', 'pitches',
                        'runsupport', 'split_id'
                        ]

    stats_df = stats_df[columns_batters]
    pitch_stats_df = pitch_stats_df[columns_pitchers]
    # Save to csv
    data.saveDf(stats_df, os.path.join(save_path, 'playerBattingStats.csv'))
    pitch_data.saveDf(pitch_stats_df, os.path.join(save_path, 'playerPitchingStats.csv'))

    overall = stats_df.loc[stats_df['split_id'] == '1']
    vsL = stats_df.loc[stats_df['split_id'] == '2']
    vsR = stats_df.loc[stats_df['split_id'] == '3']
    #print(vsR)