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
pitching_stats_path = 'playerPitchingStats.csv'

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

    #create list of player objects using master roster 
    player_list = Player.create_player(master_roster)
    #create Roster object
    roster = Roster()
    #add player objects to roster
    roster.add_players(player_list)

    #load the batting stats, select only split_id == 1 (overall stats)
    batter_loader = csvLoader(os.path.join(data_path, batting_stats_path))
    batting_stats_df = batter_loader.csv_to_df()
    batting_stats = batting_stats_df.loc[batting_stats_df['split_id'] == 1]

    #load pitching stats and select split_id == 1 (overall stats)
    pitcher_loader = csvLoader(os.path.join(data_path, pitching_stats_path))
    pitching_stats_df = pitcher_loader.csv_to_df()
    pitching_stats = pitching_stats_df.loc[pitching_stats_df['split_id'] == 1]

    main_logger.info(f'\n{pitching_stats.head(10)}')
    main_logger.info(batting_stats.head(10))
   
   #add batting and pitching stats to roster, which will in turn assign them to the corresponding player
    roster.add_stats(batting_stats)
    roster.add_stats(pitching_stats)

    Edwards = roster.get_player(player_id=4)
    Alejandro = roster.get_player(player_id='4744')
    Reimer = roster.get_player(player_id=411)
    Abreu = roster.get_player(player_id=211)
    Pacheco = roster.get_player(player_id=3751)
    Pavlik = roster.get_player(player_id='1270')


    print(Reimer.get_info())
    print(Alejandro.get_info())
    print(Abreu.get_info())
    print(Edwards.get_info())
    print(Pacheco.get_info())
    print(Pavlik.get_info())
    




