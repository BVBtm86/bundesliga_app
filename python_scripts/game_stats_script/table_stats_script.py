import pandas as pd
import numpy as np
import streamlit as st
from python_scripts.game_stats_config import team_logos_config


st.cache()
def process_table_data(data):
    # ##### Read Data
    buli_df = data.copy()

    # ##### Creating Tabel Stats Filter
    buli_df['Win'] = np.where(buli_df['Result'] == 'Win', 1, 0)
    buli_df['Draw'] = np.where(buli_df['Result'] == 'Draw', 1, 0)
    buli_df['Defeat'] = np.where(buli_df['Result'] == 'Defeat', 1, 0)
    buli_df['Season'] = 1
    buli_df['Home'] = np.where(buli_df['Venue'] == "Home", 1, 0)
    buli_df['Away'] = np.where(buli_df['Venue'] == "Away", 1, 0)
    buli_df["1st Half"] = np.where(buli_df["Week_No"] <= 17, 1, 0)
    buli_df["2nd Half"] = np.where(buli_df["Week_No"] >= 18, 1, 0)
    form_games = list(buli_df["Week_No"].unique())[-5:]
    buli_df["Form"] = np.where(buli_df["Week_No"].isin(form_games),1, 0)

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
    # ##### Season Data
    buli_season = data[data[table_type] == 1].reset_index(drop=True)

    # ##### Create Tab
    buli_tab = buli_season.groupby(['Team'])[['Season', 'Win', 'Draw', 'Defeat', 'Goals', 'Goals Ag']].sum()
    buli_tab['Goal_Diff'] = buli_tab['Goals'] - buli_tab['Goals Ag']
    buli_tab['Points'] = buli_tab['Win'] * 3 + buli_tab['Draw']
    buli_tab.sort_values(by=['Points', 'Goal_Diff'], ascending=[False, False], inplace=True)
    buli_tab.reset_index(inplace=True)
    buli_tab['Rank'] = [i for i in range(1, len(buli_tab) + 1)]
    buli_tab.set_index('Rank', inplace=True)
    buli_tab.columns = ["Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]

    return buli_tab


def table_stats(season_data, stat, pos_favourite_team):
    st.markdown(f"<h4 style='text-align: center;'h4><b>{stat}</b>", unsafe_allow_html=True)
    teams_stat = season_data[stat].values
    stat_data = []
    for i in range(len(teams_stat)):
        if i == pos_favourite_team:
            if stat == 'Team':
                stat_data.append(st.markdown(f"<p style='text-align: left;'p><font color=#d20614><b>{teams_stat[i]}</b></font>", unsafe_allow_html=True))
            else:
                stat_data.append(st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{teams_stat[i]}</b></font>", unsafe_allow_html=True))
        else:
            if stat == 'Team':
                stat_data.append(st.markdown(f"<p style='text-align: left;'p>{teams_stat[i]}", unsafe_allow_html=True))
            else:
                stat_data.append(st.markdown(f"<p style='text-align: center;'p>{teams_stat[i]}", unsafe_allow_html=True))
        
    return stat_data




def table_page(data, page_season, favourite_team):
    # ##### Check Max Match Day
    season_df = process_table_data(data)
    match_day = season_df['Week_No'].max()

    ##### Season Table Filter
    filter_type = ["Season", "Form", "Home", "Away", "1st Half", "2nd Half"]
    if match_day <= 17:
        filter_type.remove("2nd Half")
    season_type = st.sidebar.selectbox("Season Filter", 
                                       options=filter_type)

    buli_season_df = buli_table_data(data=season_df, 
                                     table_type=season_type)
    st.markdown(f'<h4>{page_season}</b> <b><font color = #d20614>{season_type}</font> Table</h4>', unsafe_allow_html=True)

    teams_season = buli_season_df['Team'].unique()
    pos_favourite_team = list(teams_season).index(favourite_team)

    buli_season_df = buli_season_df.reset_index(drop=False)
    buli_season_df.rename(columns={'index': 'Rank'}, inplace=True)

    
    logo_data = [team_logos_config[team] for team in buli_season_df['Team']]
    buli_season_df.insert(0, " ", logo_data)
    
    st.dataframe(data=
                 buli_season_df.style.apply(lambda x: ['background-color: #ffffff' if i % 2 == 0 
                                                       else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
        lambda x: ['color: #d20614' if i == pos_favourite_team else 'color: #000000' for i in range(len(x))], axis=0), 
                    use_container_width=True, 
                    hide_index=True, 
                    height=35*len(buli_season_df)+38,
                    column_config={
                    "Rank": st.column_config.Column(
                        width="small",
                    ),
                    "Team": st.column_config.Column(
                        width="large",
                    ),
                    "MP": st.column_config.Column(
                        width="small",
                    ),
                    "W": st.column_config.Column(
                        width="small",
                    ),
                    "D": st.column_config.Column(
                        width="small",
                    ),
                    "L": st.column_config.Column(
                        width="small",
                    ),
                    "GF": st.column_config.Column(
                        width="small",
                    ),
                    "GA": st.column_config.Column(
                        width="small",
                    ),
                    "GD": st.column_config.Column(
                        width="small",
                    ),
                    "Pts": st.column_config.Column(
                        width="small",
                    ),
                    " ": st.column_config.ImageColumn(
                        width="small"
                    )})
