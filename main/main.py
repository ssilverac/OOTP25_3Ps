import pandas as pd
import os
from league import League, Roster, Player
from utils import csvLoader
from fileLog import get_logger

    
# define filepaths
data_path = '../data/cleaned'
master_roster_file = 'master_roster.csv'
teams = 'masterTeamID.csv'
batting_stats_path = 'playerBattingStats.csv'

main_logger = get_logger('MainLogger', 'main.log')

if __name__ == '__main__':


    #initialize logger
    main_logger.info('Starting main script')

    # load team list df
    team_df_loader = csvLoader(os.path.join(data_path, teams))
    team_names_df = team_df_loader.csv_to_df()
   
    #initiate League object
    mlb = League('mlb')
    # add teams to League object
    mlb.add_teams(team_names_df)

    # use League function to capture dict of all teams. Keys = team ID, values = Team Name
    teams_dict = mlb.list_all_teams(team_list=True)

    # load master roster df
    master_roster_loader = csvLoader(os.path.join(data_path, master_roster_file))
    master_roster = master_roster_loader.csv_to_df()
    
    player_list = Player.create_player(master_roster)
    #create Roster object
    roster = Roster()
    roster.add_players(player_list)

    batter_loader = csvLoader(os.path.join(data_path, batting_stats_path))
    batting_stats_df = batter_loader.csv_to_df()


    batting_stats = batting_stats_df.loc[batting_stats_df['split_id'] == 1]

    Edwards = roster.get_player(player_id=4)
    print(Edwards.get_info())




