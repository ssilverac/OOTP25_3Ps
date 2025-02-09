from fileLog import get_logger


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

    def add_stats(self, df):
        league_logger.info('Adding stats to player objects\n')

        records = df.to_dict('records')
        for row in records:
            player_id = row.get('player ID')
            if player_id in self.players:
                player = self.players[player_id]
                if 'gdp' in row:
                    if not isinstance(player, Batter):
                        new_player = Batter(player)
                        new_player.add_stats(row)
                        self.players[player_id] = new_player
                        league_logger.info(f'Converted {player_id} into Batter object Successfully')
                    else:
                        league_logger.info(f'Player: {player_id} already Batter. Adding stats')
                        player.add_stats(row)

                elif 'ip' in row:
                    if not isinstance(player, Pitcher):
                        new_player = Pitcher(player)
                        new_player.add_stats(row)
                        self.players[player_id] = new_player
                        league_logger.info(f'Converted {player_id} into Pitcher Object Successfully')
                    else:
                        league_logger.info(f'Player {player_id} Already a Pitcher. Adding stats')
   

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
        print(f'\nRetrieving Player: {self.last_name}, {self.first_name}\n')
        return {'ID': self.player_id,
                'Last Name': self.last_name,
                'First Name': self.first_name,
                'Team ID': self.team_id,
                'Team Name': self.team,
                'Position': self.position}

class Batter(Player):
    def __init__(self, player):
        super().__init__(player.player_id, player.last_name,
                         player.first_name, player.team_id,
                         player.team, player.position)
        self.stats = {}

    def add_stats(self, row):
        league_logger.info('Adding Stats to Existing Player object...')


        self.stats = {
            'Games': row.get('g', 0),
            'Games Started': row.get('gs', 0),
            'Plate App': row.get('pa', 0),
            'At Bats': row.get('ab', 0),
            'Hits': row.get('h', 0),
            'Doubles': row.get('2b', 0),
            'Triples': row.get('3b', 0),
            'Home Runs': row.get('hr', 0),
            'RBI': row.get('rbi', 0),
            'Runs': row.get('r', 0),
            'Stolen Bases': row.get('sb', 0),
            'Caught Stealing': row.get('cs', 0),
            'Walks': row.get('bb', 0),
            'HBP': row.get('hbp', 0),
            'Strikeouts': row.get('k'),
            'Sac Hits': row.get('sh', 0),
            'Sac Flys': row.get('sf', 0),
            'GIDP': row.get('gdp', 0),
            'IBB': row.get('ibb', 0),
            'Catch Int': row.get('ci', 0),
            'Pitches Seen': row.get('pitches seen', 0)
        }
    
    def get_info(self):
        info = super().get_info()
        info['Stats'] = self.stats
        return info

class Pitcher(Player):
    def __init__(self, player):
        super().__init__(player.player_id, player.last_name,
                         player.first_name, player.team_id,
                         player.team, player.position)
        self.stats = {}

    def add_stats(self, row):
        league_logger.info('Add Stats function initialized for PITCHER')
       
        self.stats = {
            'Games': row.get('g', 0),
            'Wins': row.get('w', 0),
            'Losess': row.get('l', 0),
            'Saves': row.get('s', 0),
            'Innings Pitched': row.get('ip', 0),
            'Hits Allowed': row.get('ha', 0),
            'Runs': row.get('R', 0),
            'Earned Runs': row.get('er', 0),
            'Walks': row.get('bb', 0),
            'Hit by Pitch': row.get('hp', 0),
            'Strikeouts': row.get('k', 0),
            'Batters Faced': row.get('bf', 0),
            'At Bats': row.get('ab', 0),
            'Singles': row.get('1b', 0),
            'Doubles': row.get('2b', 0),
            'Triples': row.get('3b', 0),
            'Home Runs': row.get('hr', 0),
            'Total Bases': row.get('tb', 0),
            'Sac Hits': row.get('sh', 0),
            'Sac Flies': row.get('sf', 0),
            'Intent Walks': row.get('iw', 0),
            'Balks': row.get('bk', 0),
            'Wild Pitches': row.get('wp', 0),
            'Double Plays': row.get('dp', 0),
            'Quality Starts': row.get('qs', 0),
            'Save Opps': row.get('saveopp', 0),
            'Blown Saves': row.get('blownsv', 0),
            'Holds': row.get('holds', 0),
            'Stolen Bases': row.get('sb', 0),
            'Caught Stealing': row.get('cs', 0),
            'Ground Balls': row.get('gb', 0),
            'Fly Balls': row.get('fb', 0),
            'Pitches': row.get('pitches', 0)
        }

    def get_info(self):
        info = super().get_info()
        info['Stats'] = self.stats
        return info

if __name__ == '__main__':
    
    pass
