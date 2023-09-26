import pandas as pd
import numpy as np
import streamlit as st
from python_scripts.game_stats_app_scripts.game_stats_app_utils import config_teams_images


def game_results_page(data:pd.DataFrame,
                      page_season:str,
                      favourite_team:str) -> st:
    
    # ##### Game Results Page Options
    st.sidebar.subheader("Options")

    # ##### Season Data
    season_df = data.copy()

    # ##### Show Match Day
    available_match_days = np.linspace(1, season_df['Week_No'].max(), season_df['Week_No'].max(), dtype=np.int32)
    match_day = st.sidebar.selectbox(label="Select Match Day",
                                     options=available_match_days,
                                     index=len(available_match_days) - 1)
    
    # ##### Filter Season Data by Match Day and Format Data
    match_day_data = season_df[(season_df['Week_No'] == match_day) & (season_df['Venue'] == 'Home')].reset_index(drop=True)
    match_day_data['Result'] = match_day_data['Goals'].astype(str) + ' - ' + match_day_data['Goals Ag'].astype(str)
    match_day_data = match_day_data[['Team', 'Result', 'Opponent']]
    match_day_data.rename(columns={'Team':'Home Team', 'Opponent': 'Away Team'}, inplace=True)

    # ##### Teams Logo
    home_logo_data = [config_teams_images['config_teams_logo'][team] for team in match_day_data['Home Team']]
    match_day_data.insert(0, " ", home_logo_data)

    away_logo_data = [config_teams_images['config_teams_logo'][team] for team in match_day_data['Away Team']]
    match_day_data.insert(4, "  ", away_logo_data)

    st.markdown(f'<h4>Season <font color = #d20614>{page_season}</font> Match Day <font color = #d20614>{match_day}</font> Results</h4>', unsafe_allow_html=True)

    # ##### Final Bundesliga Season Filter Table
    try:
        pos_game = match_day_data['Home Team'].to_list().index(favourite_team)
    except:
        pos_game = match_day_data['Away Team'].to_list().index(favourite_team)

    st.dataframe(data=match_day_data.style.apply(lambda x: ['background-color: #ffffff' if i % 2 == 0 
                                                            else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
        lambda x: ['color: #d20614' if j == pos_game else 'color: #000000' for j in range(len(x))], axis=0),
                    use_container_width=True, 
                    hide_index=True, 
                    column_config={
                    "Home Team": st.column_config.Column(
                        width="large",
                    ),
                    "Away Team": st.column_config.Column(
                        width="large",
                    ),
                    " ": st.column_config.ImageColumn(
                        width="small"
                    ),
                    "  ": st.column_config.ImageColumn(
                        width="small"
                    ),
                    })
