import pandas as pd
import numpy as np
from supabase import create_client
import streamlit as st


# ########## Supabase Connection
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)


supabase = init_connection()

# ########## Get Last 5 Seasons of Data
st.cache()
def retrieve_seasons_query():
    """ Return Available Seasons """
    data_query = supabase.table('buli_seasons').select('*').execute().data
    data = pd.DataFrame(data_query)
    all_seasons = list(data['Season'].unique())
    final_seasons = all_seasons[-5:]
    events_season = all_seasons[-1]

    return final_seasons, events_season


def retrieve_season_teams(season):
    """ Return Teams per Season """
    data_query = supabase.table("buli_stats_team").select('*').eq('Season', season).execute().data
    data = pd.DataFrame(data_query)
    all_teams = list(data['Team'].unique())
    all_teams.sort()
    bvb_position = all_teams.index("Borussia Dortmund")

    return all_teams, bvb_position


st.cache()
def retrieve_season_data(season):
    """ Return Season Data """
    data_query = supabase.table("buli_stats_team").select('*').eq('Season', season).execute().data
    season_data = pd.DataFrame(data_query)

    return season_data


st.cache()
def retrieve_season_player_data(season):
    """ Return Season Data """
    data_query = supabase.table("buli_stats_player").select('*').eq('Season', season).execute().data
    season_data = pd.DataFrame(data_query)

    return season_data

st.cache()
def retrieve_season_gk_data(season):
    """ Return Season Data """
    data_query = supabase.table("buli_stats_gk").select('*').eq('Season', season).execute().data
    season_data = pd.DataFrame(data_query)

    return season_data




