import pandas as pd
import numpy as np
from PIL import Image
from supabase import create_client
import streamlit as st


# ########## Supabase Connection
st.cache_resource()
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()

# ########## Retrieve Season Info
st.cache_data(ttl=3600)
def retrieve_season_info(table):
    """ Available Seasons querry """
    data_query = supabase.table(table).select('*').execute().data
    data = pd.DataFrame(data_query)

    """ Game Stats and Events Stats Seasons """
    all_seasons = list(data['Season'].unique())
    game_stats_seasons = all_seasons[-5:]
    events_season = all_seasons[-1]

    return game_stats_seasons, events_season

# #################################################################################################### Game Stats Analysis
# ########## Retrieve Season Teams
def retrieve_season_teams(table, season):
    """ Teams per Season querry """
    data_query = supabase.table(table).select('*').eq('Season', season).execute().data
    data = pd.DataFrame(data_query)

    """ All Season Teams and position of BVB """
    all_teams = list(data[data['Season'] == season]['Team'].values)
    all_teams.sort()
    bvb_position = all_teams.index("Borussia Dortmund")

    return all_teams, bvb_position


# ########## Retrieve Season Data
st.cache_data(ttl=3600)
def retrieve_season_data(table, season):
    """ Return Season Data """
    data_query = supabase.table(table).select('*').eq('Season', season).execute().data
    season_data = pd.DataFrame(data_query)  

    return season_data


# # ########## Retrieve Last 5 Seasons Data
st.cache_data(ttl=3600)
def retrieve_all_seasons_data(table, team, seasons, team_analysis=False):
    """ Return All Seasons Data """
    data_query = supabase.table(table).select('*').eq('Team', team).execute().data
    all_seasons_data = pd.DataFrame(data_query)
    all_seasons_data = all_seasons_data[all_seasons_data['Season'].isin(seasons)].reset_index(drop=True)

    if team_analysis:
        data_opponent_query = supabase.table(table).select('*').eq('Opponent', team).execute().data
        all_seasons_opponent_data = pd.DataFrame(data_opponent_query)
        all_seasons_opponent_data = all_seasons_opponent_data[all_seasons_opponent_data['Season'].isin(seasons)].reset_index(drop=True)
        all_seasons_data = pd.concat([all_seasons_data, all_seasons_opponent_data])

    return all_seasons_data

# #################################################################################################### Game Events Analysis