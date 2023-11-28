import streamlit as st
from streamlit_option_menu import option_menu
from python_scripts.data_script import BunesligaInfo, BundesligaGameData
from python_scripts.game_stats_app_scripts.game_stats_utils import GameStatsConfiguration, GameStatsProcessing
from python_scripts.game_stats_app_scripts.game_results_script import game_results_page
from python_scripts.game_stats_app_scripts.standings_stats_script import standings_page
from python_scripts.game_stats_app_scripts.game_stats_script import game_stats_page
from python_scripts.game_stats_app_scripts.team_stats_script import team_page
from python_scripts.game_stats_app_scripts.player_stats_script import player_page
from python_scripts.game_stats_app_scripts.gk_stats_script import gk_page

def game_stats_analysis(bundesliga_info:BunesligaInfo,
                        bundesliga_game_data:BundesligaGameData,
                        game_stats_config:GameStatsConfiguration,
                        game_stats_processing:GameStatsProcessing,
                        team:str, 
                        season_teams:list,
                        season:str, 
                        last_5_seasons:list) -> st:


    # ##### Load Season Data
    table_info = game_stats_config.get_tab_info()
    season_team_data = bundesliga_game_data.retrieve_season_data(table=table_info.team_stats_tab, 
                                                                 season=season)
    season_gk_data = bundesliga_game_data.retrieve_season_data(table=table_info.gk_stats_tab,
                                                               season=season)

    season_data = game_stats_processing.filter_season_data(
        data=game_stats_processing.process_goals_opponent(
            data=game_stats_processing.process_team_data(data=season_team_data, 
                                                         data_gk=season_gk_data)))
    
    # ##### Page Description
    st.markdown(
        'Analyse different types of <b>Bundesliga</b> <b><font color = #d20614>Game Stats</font></b> at both <b>'
        '<font color = #d20614>Team</font></b> and <b><font color = #d20614>Player</font></b> level',
        unsafe_allow_html=True)

    # ##### Game Stats Analysis Types
    statistics_type = ["Match Day Results",
                       "Season Standings",
                       "Game Statistics",
                       "Team Statistics",
                       "Player Statistics",
                       "Gk Statistics"]

    with st.sidebar:
        st.subheader("Statistics")
        statistics_track = option_menu(menu_title=None,
                                       options=statistics_type,
                                       icons=["calendar3", "table", "clipboard-data",
                                              "reception-4", "person-lines-fill", "shield-shaded"],
                                       styles={"nav-link": {"--hover-color": "#e5e5e6"}})

    ##### Match Day Results
    if statistics_track == 'Match Day Results':
        game_results_page(game_stats_config=game_stats_config,
                          data=season_data,
                          page_season=season, 
                          favourite_team=team)

    # ##### Season Table
    elif statistics_track == 'Season Standings':
        standings_page(game_stats_config=game_stats_config,
                       game_stats_processing=game_stats_processing,
                       data=season_data, 
                       page_season=season,
                       favourite_team=team)
    
    # ##### Game Statistics
    elif statistics_track == 'Game Statistics':
        game_stats_page(data=season_data,
                        page_season=season,
                        favourite_team=team)

    ##### Team Statistics
    elif statistics_track == 'Team Statistics':
        # ##### Load Last 5 Seasons Data
        all_seasons_team_data = bundesliga_game_data.retrieve_all_seasons_data(table=table_info.team_stats_tab,
                                                                               team=team,
                                                                               seasons=last_5_seasons,
                                                                               team_analysis=True)
        all_seasons_gk_data = bundesliga_game_data.retrieve_all_seasons_data(table=table_info.gk_stats_tab,
                                                                             team=team,
                                                                             seasons=last_5_seasons)
        
        # ##### Process Last 5 Seasons Data
        all_seasons_data = game_stats_processing.filter_season_data(
            data=game_stats_processing.process_team_data(data=all_seasons_team_data,
                                                         data_gk=all_seasons_gk_data))
        
        # ##### Retrieve Season Games
        season_games_schedule=bundesliga_info.retrieve_season_games(table=table_info.games_tab,
                                                                    season=season)

        # ##### Team Page
        team_page(data=season_data,
                  data_all=all_seasons_data,
                  games_schedule=season_games_schedule,
                  page_season=season,
                  favourite_team=team,
                  season_teams=season_teams)
    
    # # ##### Player Statistics
    elif statistics_track == 'Player Statistics':
        season_player_data = game_stats_processing.filter_season_data(data=bundesliga_game_data.retrieve_season_data(
            table=table_info.player_stats_tab, season=season))
  
        player_page(data=season_player_data,
                    favourite_team=team,
                    page_season=season,
                    season_teams=season_teams,
                    last_5_seasons=last_5_seasons)
    
    # ##### Goalkeeper Statistics
    elif statistics_track == 'Gk Statistics':
        season_gk_data = game_stats_processing.filter_season_data(data=season_gk_data)

        gk_page(data=season_gk_data,
                favourite_team=team,
                page_season=season,
                season_teams=season_teams,
                last_5_seasons=last_5_seasons)
        
    st.sidebar.markdown("")
