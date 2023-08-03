import streamlit as st
from streamlit_option_menu import option_menu
from python_scripts.game_stats_script.day_stats_script import match_day_page
from python_scripts.game_stats_script.table_stats_script import *


def game_stats_analysis(data, data_gk, team, season):
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

    # ##### Match Day Statistics
    if statistics_track == 'Match Day Statistics':
        match_day_page(data=data,
                       data_gk=data_gk,
                       page_season=season,
                       favourite_team=team)

    # ##### Season Table
    elif statistics_track == 'Season Table':
        table_page(data=data,
                   page_season=season,
                   favourite_team=team)

    # # ##### Team Statistics
    # elif statistics_track == 'Team Statistics':
    #     team_page(page_season=season,
    #               favourite_team=team,
    #               all_seasons=app_seasons)
    #
    # # ##### Player Statistics
    # elif statistics_track == 'Player Statistics':
    #     player_page(page_season=season,
    #                 favourite_team=team,
    #                 all_seasons=app_seasons)
    #
    # # ##### Goalkeeper Statistics
    # elif statistics_track == 'Goalkeeper Statistics':
    #     gk_page(page_season=season,
    #             favourite_team=team,
    #             all_seasons=app_seasons)