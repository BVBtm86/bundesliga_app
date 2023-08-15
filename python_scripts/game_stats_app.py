import streamlit as st
from streamlit_option_menu import option_menu
from python_scripts.data_script import retrieve_season_data, retrieve_all_seasons_data
from python_scripts.game_stats_scripts.day_stats_script import match_day_page
from python_scripts.game_stats_scripts.table_stats_script import table_page
from python_scripts.game_stats_scripts.team_stats_script import team_page
from python_scripts.game_stats_scripts.game_stats_utils import process_team_data, process_goal_data, team_stats_tab, player_stats_tab, gk_stas_tab

def game_stats_analysis(team:str, 
                        season:str, 
                        last_5_seasons:list) -> st:

    # ##### Load Season Data
    season_team_data = retrieve_season_data(table=team_stats_tab, 
                                            season=season)
    season_gk_data = retrieve_season_data(table=gk_stas_tab,
                                          season=season)
    
    season_data = process_goal_data(data=process_team_data(data=season_team_data, 
                                                           data_gk=season_gk_data))

    # ##### Page Description
    st.markdown(
        'Analyse different types of <b>Bundesliga</b> <b><font color = #d20614>Game Stats</font></b> at both <b>'
        '<font color = #d20614>Team</font></b> and <b><font color = #d20614>Player</font></b> level',
        unsafe_allow_html=True)

    # ##### Game Stats Analysis Types
    statistics_type = ["Match Day Statistics",
                       "Season Table",
                       "Team Statistics",
                       "Player Statistics",
                       "Goalkeeper Statistics"]

    with st.sidebar:
        st.subheader("Statistics")
        statistics_track = option_menu(menu_title=None,
                                       options=statistics_type,
                                       icons=["calendar3", "table", "reception-4",
                                              "person-lines-fill", "shield-shaded"],
                                       styles={"nav-link": {"--hover-color": "#e5e5e6"}})

    # # ##### Match Day Statistics
    if statistics_track == 'Match Day Statistics':
        match_day_page(data=season_data,
                       page_season=season,
                       favourite_team=team)

    # ##### Season Table
    elif statistics_track == 'Season Table':
        table_page(data=season_data,
                   page_season=season,
                   favourite_team=team)

    # ##### Team Statistics
    elif statistics_track == 'Team Statistics':
        # ##### Load Last 5 Seasons Data
        all_seasons_team_data = retrieve_all_seasons_data(table=team_stats_tab, 
                                                          team=team,
                                                          seasons=last_5_seasons,
                                                          team_analysis=True)
        all_seasons_gk_data = retrieve_all_seasons_data(table=gk_stas_tab,
                                                        team=team,
                                                        seasons=last_5_seasons)
        
        # ##### Process Last 5 Seasons Data
        all_seasons_data = process_team_data(data=all_seasons_team_data, 
                                             data_gk=all_seasons_gk_data)

        team_page(data=season_data,
                  data_all=all_seasons_data,
                  page_season=season,
                  favourite_team=team)
    
    # ##### Player Statistics
    elif statistics_track == 'Player Statistics':
        pass
        # season_player_data = retrieve_season_data(table=player_stats_tab,
        #                                           season=season)
        # all_seasons_player_data = retrieve_all_seasons_data(table=player_stats_tab,
        #                                                     team=team,
        #                                                     seasons=last_5_seasons)
        # player_page(page_season=season,
        #             favourite_team=team,
        #             all_seasons=app_seasons)
    
    # ##### Goalkeeper Statistics
    elif statistics_track == 'Goalkeeper Statistics':
        pass
        # gk_page(page_season=season,
        #         favourite_team=team,
        #         all_seasons=app_seasons)
    st.sidebar.markdown("")
