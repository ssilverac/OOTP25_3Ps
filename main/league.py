import pandas as pd
from fileLog import get_logger
from utils import csvLoader

league_logger = get_logger('LeagueLogger', 'league.log')

class League:
    def __init__(self, league_name):
        self.league_name = league_name
        self.teams = {}
        self.player = {}

        league_logger.info(f'{league_name} Created successfully\n')

    def add_teams(self, df):
        league_logger.info('add_teams successfully initiated')
        self.teams = {row['ID']:row['Team Name'] for row in df.to_dict('records')}
    
    def get_team(self, team_id=None, team_name=None):
        league_logger.info('get team function initiated')
        print('Retrieving Team Info\n')
        if team_id:
            team_id = int(team_id)
            if team_id not in self.teams:
                league_logger.info('Team {team_id} not found in database')
                return {'Error': f' Team ID {team_id} not found.'}
            
            league_logger.info(f'Searching for ID: {team_id} in Database...')
            return {'ID': team_id, 'Team Name': self.teams.get(team_id, 'Team not found')}
        
        if team_name:
            for id_, name in self.teams.items():
                if name.lower() == team_name.lower():
                    league_logger.info('Team Found, retrieving Info...')
                    return {'ID': id_, 'Team Name': name}
        
        return 'Team Not Found'
    
    def list_all_teams(self, team_list=False):
        league_logger.info('Listing all teams in League....\n')

        if not self.teams:
            league_logger.info('No Teams found')
            return 'No Teams in League'
        
        if team_list == True:
            return self.teams
        return '\n'.join([f'ID: {team_id}, Name: {team_name}' for team_id, team_name in self.teams.items()])

class Roster:
    def __init__(self):
        self.team_roster = {} #{team_id: {player_ID, player_ID...}}
        self.players = {} # {player_ID: player_object}
     
    def add_players(self, player_list):
        league_logger.info('Add Player function initiated.\n')
        for player in player_list:
                self.players[player.player_id] = player

                if player.team_id not in self.team_roster:
                    self.team_roster[player.team_id] = set()
                self.team_roster[player.team_id].add(player.player_id)

    def get_player(self, player_id=None, team_id=None):
        league_logger.info('get_player function initialized')
        if player_id:
            player_id = int(player_id)
            league_logger.info(f'Searching for {player_id}')

            if player_id in self.players:
                league_logger.info(f'Player ID: {player_id} FOUND! Retrieving player')
                return self.players[player_id]
            
            else:
                return f'Player ID: {player_id} not found'
        
        if team_id:
            team_id = int(team_id)
            league_logger.info(f'Searching for Team: {team_id}...')

            if team_id in self.team_roster:
                league_logger.info(f'Team {team_id} found!')
                return [self.players[player_id] for player_id in self.team_roster[team_id]] if self.team_roster[team_id] else 'No Team Found'

class Player:
    def __init__(self, player_id, last_name, first_name, team_id, team, position):
        self.player_id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.team_id = team_id
        self.team = team
        self.position = position

    @classmethod
    def create_player(cls, df):
        records = df.to_dict('records')
        player_list = []
        for row in records:
            player = cls(
                row['Player ID'],
                row['Last Name'],
                row['First Name'],
                row['Team ID'],
                row['Team Name'],
                row['Position']
            )
            player_list.append(player)
        return player_list
 
    def get_info(self):
        league_logger.info(f'Retrieving {self.last_name}, {self.first_name}...\n')
        print('\nRetrieving Player\n')
        return {'ID': self.player_id,
                'Last Name': self.last_name,
                'First Name': self.first_name,
                'Team ID': self.team_id,
                'Team Name': self.team,
                'Position': self.position,  
                'Stats': self.stats}

class Batter(Player):
    def __init__(self, player):
        super().__init__(player.player_id, player.last_name,
                         player.first_name, player.team_id,
                         player.team, player.position)
        self.stats = {}

    def add_stats(self, df):
        league_logger.info('Adding Stats to Existing Player object...')

        records = df.to_dict('records')

        for row in records:
            self.stats = {
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

    
if __name__ == '__main__':
    
    pass
