import pandas as pd
import os
import numpy as np
from fileLog import config_log
import logging

config_log('app.log')

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
            logging.info('File successfully pre-Parsed')

    def extractSections(self, strip_chars, start_condition, end_condition, clean_headers=False, team_id=False, clean_stats=False):

        if self.processed_content is None:
            logging.info('ValueError: No Processed content passed to function')
            raise ValueError('File content must be preprocessed first')

        logging.info('contents passed Successfully')

        start_copying = False
        parsed_list = []

        for line in self.processed_content:
            line = line.strip(strip_chars).strip()

            #check for start of section
            if start_condition and start_condition(line):
                start_copying = True
                logging.info(f'Start of Team Info found. Copying = {start_copying}\n')
                logging.info(f'Line proccessed: "{line}"')
                continue

            #check for end of section
            if end_condition and end_condition(line):
                start_copying = False
                logging.info(f'End of Team Info reached. Copying = {start_copying}\n')
                logging.info(f'End of section reached: "{line}"')
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
        if clean_stats:

            parsed_list = self._cleanPlayerStats(parsed_list)
        
        return parsed_list

    def _cleanHeaders(self, parsed_list):
        logging.info('_cleanHeaders function Initialized\n')

        cleaned_headers = []

        for item in parsed_list:
            cleaned_headers.extend([i.strip() for i in item.split(',')])
        
        logging.info('Headers cleaned successfully')
        
        logging.info(cleaned_headers)
        return cleaned_headers
        
    def _cleanTeamIds(self, parsed_list):
        '''
        Parse the stats from each player in the league

        Returns nested list.
        '''
        logging.info('_cleanTeamIds called successfully')

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
                logging.warning(f'Unexpected format in line: {i}')

        return team_dict

    def _cleanPlayerStats(self, parsed_list):
        logging.info('_cleanPlayerStats Initiated\n')

        team_stats = []
        
        for i in parsed_list:
            #logging.info(f'processing entry: {i}')
            if i.strip():
                # split entry for each player
                i = i.split(',')
                
                #fix the extra column created due to the comma in the name of the specific team
                if len(i) > 38:
                    logging.warning('Unexpected length encountered')
                    name = i[-8].strip()
                    
                    if 'Jackson County' in name:
                        del i[-8]
                        logging.info('Extra Entry successfully removed. Length now correct')
                    else:
                        logging.warning('Exception caught successfully')
                        raise ValueError('Extra String Unknown. Check Raw Data Carefully')
                
                cleaned_stats = [np.nan if item =='' else item for item in i]
               
                cleaned_stats = cleaned_stats[:-1]
                
                if len(cleaned_stats) != 37:
                    logging.warning(f'Unexpected length for player stats: {len(cleaned_stats)}')
                    logging.warning(f'cleaned stats content: \n{cleaned_stats}')
                    continue

                team_stats.append(cleaned_stats)
            else:
                logging.warning(f'Empty or malformed entry: {i}')
        
        return team_stats

    def createStatsDf(self, player_stats, column_names):
        '''
        Takes nested list from parsePlayerStats and creates a pandas
        DataFrame using the Headers from parseHeaders

        Returns pandas.DataFrame()
        '''
        player_stats_df = pd.DataFrame(player_stats, columns=column_names)
        logging.info('player Stats created successfully')
        return player_stats_df

    def saveDf(self, df, filename):
        '''
        Saves the df into a specified file location for later retrieval
        '''
        df.to_csv(filename, index=False)
        logging.info(f'{filename} saved Successfully')

if __name__ == '__main__':

    raw_data_path = '../data/raw/player_batting_stats.txt'
    save_path = '../data/cleaned'

    # Create FileParser Object
    data = FileParser(raw_data_path)
    #Pre-process the data
    data.preProcessFile('\n')

    # Extract the headers
    headers = data.extractSections('/', lambda line: line.startswith('FILE FORMAT:'), lambda line: line.startswith('NOTE'), clean_headers=True)
    
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
    player_stats = data.extractSections('/', lambda line: line.startswith('NOTE'), lambda line: line is None, clean_stats=True)
    # Create DataFrame using the headers as the column names
    stats_df = data.createStatsDf(player_stats, headers)
    
    # Select relevant columns to save
    columns_of_interest =['player ID', 'lastname', 'firstname', 'year', 'team ID', 'g', 'gs',
       'pa', 'ab', 'h', '2b', '3b', 'hr', 'rbi', 'r', 'sb', 'cs', 'bb', 'hp',
       'k', 'sh', 'sf', 'gdp', 'ibb', 'ci', 'pitches seen', 'split_id']

    stats_df = stats_df[columns_of_interest]
    # Save to csv
    data.saveDf(stats_df, os.path.join(save_path, 'playerBattingStats.csv'))

    overall = stats_df.loc[stats_df['split_id'] == '1']
    vsL = stats_df.loc[stats_df['split_id'] == '2']
    vsR = stats_df.loc[stats_df['split_id'] == '3']
    print(vsR)