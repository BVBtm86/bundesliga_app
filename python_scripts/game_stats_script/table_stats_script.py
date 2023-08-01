import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image



st.cache()
def process_table_data(data):
    # ##### Read Data
    buli_df = data.copy()

    # ##### Creating Tabel Stats
    buli_df['Win'] = np.where(buli_df['Result'] == 'Win', 1, 0)
    buli_df['Draw'] = np.where(buli_df['Result'] == 'Draw', 1, 0)
    buli_df['Defeat'] = np.where(buli_df['Result'] == 'Defeat', 1, 0)
    buli_df['Total'] = 1
    buli_df['Home'] = np.where(buli_df['Venue'] == "Home", 1, 0)
    buli_df['Away'] = np.where(buli_df['Venue'] == "Away", 1, 0)
    buli_df["1st Period"] = np.where(buli_df["Week_No"] <= 17, 1, 0)
    buli_df["2nd Period"] = np.where(buli_df["Week_No"] >= 18, 1, 0)

    # ##### Goals Statistics
    home_df = buli_df[buli_df['Venue'] == 'Home'].copy()
    home_df.reset_index(drop=True, inplace=True)
    away_df = buli_df[buli_df['Venue'] == 'Away'].copy()
    away_df.reset_index(drop=True, inplace=True)
    home_df['Goals'] = home_df['Goals'] + away_df['Own Goals']
    away_df['Goals'] = away_df['Goals'] + home_df['Own Goals']
    home_df['Goals Ag'] = away_df['Goals']
    away_df['Goals Ag'] = home_df['Goals']
    final_df = pd.concat([home_df, away_df])

    return final_df


def buli_table_data(data, table_type):
    # #####season Data
    buli_season = data[data[table_type] == 1].reset_index(drop=True)

    # ##### Create Tab
    buli_tab = buli_season.groupby(['Team'])[['Total', 'Win', 'Draw', 'Defeat', 'Goals', 'Goals Ag']].sum()
    buli_tab['Goal_Diff'] = buli_tab['Goals'] - buli_tab['Goals Ag']
    buli_tab['Points'] = buli_tab['Win'] * 3 + buli_tab['Draw']
    buli_tab.sort_values(by=['Points', 'Goal_Diff'], ascending=[False, False], inplace=True)
    buli_tab.reset_index(inplace=True)
    buli_tab['Rank'] = [i for i in range(1, len(buli_tab) + 1)]
    buli_tab.set_index('Rank', inplace=True)
    buli_tab.columns = ["Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]

    return buli_tab


# def table_stats(season_data, page_season, favourite_team):
#
#     filter_type = ["Total", "Home", "Away", "1st Period", "2nd Period"]
#     if match_day <= 17:
#         filter_type.remove("2nd Period")
#
#     season_type = st.sidebar.selectbox("Season Filter", options=filter_type)
#     buli_season_df = buli_table_data(data=filter_season_df, table_type=season_type)
#
#     st.header(f'Season {page_season}: {season_type} Table Games')
#
#     logo_col, rank_col, team_col, mp_col, w_col, d_col, l_col, gf_col, ga_col, gd_col, pts_col = st.columns(
#         [0.5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1])
#
#     with logo_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b><font color='white'>#</font></b>", unsafe_allow_html=True)
#         teams_logo = buli_season_df['Team'].unique()
#         [st.image(Image.open(f'images/{teams_logo[i]}.png'),  width=26) for i in range(len(teams_logo))]
#         pos_favourite_team = list(teams_logo).index(favourite_team)
#
#     with rank_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>Rank</b>", unsafe_allow_html=True)
#         rank = buli_season_df.index
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{rank[i]}</b></font>",
#                      unsafe_allow_html=True)
#          if i == pos_favourite_team else st.markdown(f"<p style='text-align: center;'p>{rank[i]}",
#                                                      unsafe_allow_html=True) for i in range(len(rank))]
#
#     with team_col:
#         st.markdown(f"<h4 style='text-align: left;'h4><b>Team</b>", unsafe_allow_html=True)
#         team_names = buli_season_df['Team'].values
#         [st.markdown(f"<p style='text-align: left;'p><font color=#d20614><b>{team_names[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: left;'p>{team_names[i]}", unsafe_allow_html=True)
#          for i in range(len(team_names))]
#
#     with mp_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>MP</b>", unsafe_allow_html=True)
#         matches_played = buli_season_df['MP'].values
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{matches_played[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: center;'p>{matches_played[i]}", unsafe_allow_html=True)
#          for i in range(len(matches_played))]
#
#     with w_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>W</b>", unsafe_allow_html=True)
#         team_wins = buli_season_df['W'].values
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_wins[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: center;'p>{team_wins[i]}", unsafe_allow_html=True)
#          for i in range(len(team_wins))]
#
#     with d_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>D</b>", unsafe_allow_html=True)
#         team_draws = buli_season_df['D'].values
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_draws[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: center;'p>{team_draws[i]}", unsafe_allow_html=True)
#          for i in range(len(team_draws))]
#
#     with l_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>L</b>", unsafe_allow_html=True)
#         team_defeats = buli_season_df['L'].values
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_defeats[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: center;'p>{team_defeats[i]}", unsafe_allow_html=True)
#          for i in range(len(team_defeats))]
#
#     with gf_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>GF</b>", unsafe_allow_html=True)
#         team_goals_for = buli_season_df['GF'].values
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_goals_for[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: center;'p>{team_goals_for[i]}", unsafe_allow_html=True)
#          for i in range(len(team_goals_for))]
#
#     with ga_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>GA</b>", unsafe_allow_html=True)
#         team_goals_aga = buli_season_df['GA'].values
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_goals_aga[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: center;'p>{team_goals_aga[i]}", unsafe_allow_html=True)
#          for i in range(len(team_goals_aga))]
#
#     with gd_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>GD</b>", unsafe_allow_html=True)
#         team_goals_diff = buli_season_df['GD'].values
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_goals_diff[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: center;'p>{team_goals_diff[i]}", unsafe_allow_html=True)
#          for i in range(len(team_goals_diff))]
#
#     with pts_col:
#         st.markdown(f"<h4 style='text-align: center;'h4><b>Pts</b>", unsafe_allow_html=True)
#         team_points = buli_season_df['Pts'].values
#         [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_points[i]}</b></font>",
#                      unsafe_allow_html=True) if i == pos_favourite_team else
#          st.markdown(f"<p style='text-align: center;'p>{team_points[i]}", unsafe_allow_html=True)
#          for i in range(len(team_points))]
