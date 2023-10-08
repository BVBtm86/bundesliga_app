import pandas as pd
import numpy as np
import streamlit as st
from python_scripts.game_stats_app_scripts.game_stats_app_utils import config_teams_images, config_season_filter, filter_season_data, process_goals_opponent, buli_table_data

# ##### Bundesliga Table Page
def standings_page(data:pd.DataFrame, 
                   page_season:str, 
                   favourite_team:str) -> st:

    # ##### Standings Page Options
    st.sidebar.subheader("Options")

    # ##### Process Goals Against
    data_processed = process_goals_opponent(data=data)
    
    # ##### Process Season Data
    season_df = filter_season_data(data=data_processed)

    # ##### Check Max Match Day
    match_day = season_df['Week_No'].max()

    # ##### Season Table Filter
    filter_type = config_season_filter.season_filter[:-3]
    if match_day <= 17:
        filter_type.remove("2nd Half")
    season_type = st.sidebar.selectbox(label="Season Filter", 
                                       options=filter_type)

    # ##### Season Table
    buli_season_df = buli_table_data(data=season_df, 
                                     table_type=season_type)
    st.markdown(f'<h4>{page_season}</b> <b><font color = #d20614>{season_type}</font> Standings</h4>', unsafe_allow_html=True)

    # ##### Season Rank
    buli_season_df = buli_season_df.reset_index(drop=False)
    buli_season_df.rename(columns={'index': 'Rank'}, inplace=True)

    # ##### Team Logo
    logo_data = [config_teams_images['config_teams_logo'][team] for team in buli_season_df['Team']]
    buli_season_df.insert(0, " ", logo_data)

    # ##### Final Bundesliga Season Filter Table
    rank_team = buli_season_df[buli_season_df['Team'] == favourite_team].index[0]
    st.dataframe(data=buli_season_df.style.apply(lambda x: ['background-color: #ffffff' if i % 2 == 0 
                                                            else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
        lambda x: ['color: #d20614' if j == rank_team else 'color: #000000' for j in range(len(x))], axis=0), 
                    use_container_width=True, 
                    hide_index=True, 
                    height=35*len(buli_season_df)+38,
                    column_config={
                    "Team": st.column_config.Column(
                        width="large",
                    ),
                    " ": st.column_config.ImageColumn(
                        width="small"
                    ),
                    })