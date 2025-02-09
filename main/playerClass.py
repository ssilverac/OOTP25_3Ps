import pandas as pd
import logging
from utils import csvLoader
from fileLog import config_log

#initiate config log
config_log('app.log')
logging.info('Config log succesfully initialized')

class Roster:
    def __init__(self):
        self.player_roster ={}
    
    def add_player(self, player):
        '''
        Adds a player to the roster. if the player already exists, it adds its stats
        '''
        if player.player_id in self.player_roster:
            logging.info(f'Found duplicate player ID {player.player_id}: Aggregating stats for {player.last_name}')
            self.player_roster[player.player_id].agg_stats(player.stats)
        else:
            self.player_roster[player.player_id] = player
    
    def get_player(self, last_name=None, player_id=None):
        logging.info(f'Getting player: Last Name = {last_name}, player ID = {player_id}')
        
        if player_id and player_id in self.player_roster:
            return self.player_roster[player_id]
        
        for player in self.player_roster.values():
            if last_name and player.last_name.lower() == last_name.lower():
                return player

        logging.warning(f'Player {last_name if last_name else player_id} not found')
        return None

class Player:
    def __init__(self, player_id, last_name, first_name, team_id, stats):
        self.player_id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.team_id = team_id
        self.stats = stats     
        self.advanced_stats = self.calculate_advanced_stats()
        
    @classmethod
    def createPlayer(cls, df):
        logging.info('Creating Player Object')

        records = df.to_dict('records')
        player_list = [] 
        for row in records:
            #create stats dictionary, renaming the columns
            stats = {
                'G': row.get('g', 0),
                'GS': row.get('gs', 0),
                'PA': row.get('pa', 0),
                'AB': row.get('ab', 0),
                'H': row.get('h', 0),
                '2B': row.get('2b', 0),
                '3B': row.get('3b', 0),
                'HR': row.get('hr', 0),
                'RBI': row.get('rbi', 0),
                'R': row.get('r', 0),
                'SB': row.get('sb', 0),
                'CS': row.get('cs', 0),
                'BB': row.get('bb', 0),
                'HBP': row.get('hbp', 0),
                'K': row.get('k'),
                'Sac Hits': row.get('sh', 0),
                'Sac Flys': row.get('sf', 0),
                'GIDP': row.get('gdp', 0),
                'IBB': row.get('ibb', 0),
                'Catch Int': row.get('ci', 0),
                'Pitches Seen': row.get('pitches seen', 0)
            }
            #create list of player objects, using these columns as the keys, and stores the stats for that player
            player = cls(row['player ID'], row['lastname'], row['firstname'], row['team ID'], stats)
            player_list.append(player)
        return player_list

    def agg_stats(self, player_list):

        logging.info(f'Found duplicate Player ID: Aggregating {player.last_name}')
        for key, value in player_list.items():
            self.stats[key] += value
            return
    
    def calculate_advanced_stats(self):
        AB = self.stats.get('AB', 0)
        logging.info(AB)
        H = self.stats.get('H', 0) 
        logging.info(H)
        _2B = self.stats.get('2B', 0)
        logging.info(_2B)
        _3B = self.stats.get('3B', 0)
        logging.info(_3B)
        HR = self.stats.get('HR', 0)
        logging.info(HR)
        BB = self.stats.get('BB', 0)
        logging.info(BB)
        HBP = self.stats.get('HBP', 0)
        logging.info(HBP)
        SF = self.stats.get('SF', 0)
        logging.info(SF)
        K = self.stats.get('K', 0)
        logging.info(K)

        # ensure denominatoris not zero to avoid division errors
        def safe_div(numerator, denominator):
            return round(numerator / denominator, 3) if denominator != 0 else 0.0
        
        AVG = safe_div(H, AB)
        OBP = safe_div((H + BB + HBP), (AB + BB + HBP +SF))
        _1B = H - (_2B + _3B + HR) #calculate singles
        SLG = safe_div((_1B + 2*_2B + 3*_3B + 4*HR), AB)
        OPS = OBP + SLG
        ISO = SLG - AVG
        BABIP = safe_div((H-HR), (AB - K - HR + SF))

        return {
            'AVG': AVG,
            'OBP': OBP,
            'SLG': SLG,
            'OPS': OPS,
            'ISO': ISO,
            'BABIP': BABIP
        }

    def get_info(self):
        print('\nRetriving player info\n')

        return {'ID': self.player_id,
                'Last Name': self.last_name,
                'First Name': self.first_name,
                'Team ID': self.team_id,
                'Stats': self.stats,
                'Advanced Stats': self.advanced_stats
                }

if __name__ == '__main__':
    
    load_csv = csvLoader('../data/cleaned/playerBattingStats.csv')
    #convert to df
    battingStatsDf = load_csv.csv_to_df()

    #get just the stats that correspond to overall stats.
    #the way the data is structure, each player has multiple stats line, overall, vsL, vsR and playoffs
    #where 1= overall, 2=vsL, 3=vsR, 21=playoffs
    player_stats_ovr = battingStatsDf.loc[battingStatsDf['split_id'] == 1]

    #create a player object for each entry and store in list
    player_list = Player.createPlayer(player_stats_ovr)

    #create a player roster
    PlayerRoster = Roster()

    #add each player to the PlayerRoster
    for player in player_list:
        PlayerRoster.add_player(player)

    Abbott = PlayerRoster.get_player('Abbott')
    Ables = PlayerRoster.get_player('Ables')
    Abraham = PlayerRoster.get_player('Abraham')

    print(Abbott.get_info())
    print(Ables.get_info())
    print(Abraham.get_info())
    
