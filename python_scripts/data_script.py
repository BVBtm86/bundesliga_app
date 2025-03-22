import pandas as pd
from supabase import create_client
import streamlit as st


# ########## Supabase Connection
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]

    return create_client(url, key)

# Generic function to fetch all rows in batches
def fetch_all_rows(supabase, 
                   table, 
                   filters=None, 
                   batch_size=1000):
    all_data = []
    start = 0
    batch_size = batch_size

    while True:
        query = supabase.table(table).select('*').range(start, start + batch_size - 1)
        
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        batch = query.execute().data
        if not batch:
            break
        all_data.extend(batch)
        start += batch_size

    return all_data


# #################################################################################################### Bundesliga Info
class BunesligaInfo:

    def __init__(self) -> None:
        st.cache_resource()
        self.supabase = init_connection()

    # ✅ Retrieve Season Info
    st.cache_data
    def retrieve_season_info(self, table: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        """ Retrieve all available seasons """
        data_query = fetch_all_rows(self.supabase, table)
        data = pd.DataFrame(data_query)
        all_seasons = list(data['Season'].unique())
        return all_seasons[-5:], all_seasons[-5:]

    # ✅ Retrieve Season Games
    def retrieve_season_games(self, table: str, season: str) -> pd.DataFrame:
        """ Retrieve season games using batching """
        data_query = fetch_all_rows(self.supabase, table, filters={"Season": season})
        return pd.DataFrame(data_query)

    # ✅ Retrieve Season Teams
    def retrieve_season_teams(self, table: str, season: str) -> tuple[pd.DataFrame, int]:
        """ Retrieve teams for a season using batching """
        data_query = fetch_all_rows(self.supabase, table, filters={"Season": season})
        data = pd.DataFrame(data_query)
        all_teams = sorted(set(list(data['Team'].values) + list(data['Opponent'].values)))
        return all_teams, all_teams.index("Borussia Dortmund") if "Borussia Dortmund" in all_teams else -1


# #################################################################################################### Game Stats Data
class BundesligaGameData:

    def __init__(self) -> None:
        st.cache_resource()
        self.supabase = init_connection()

    # Retrieve Season Data
    st.cache_data
    def retrieve_season_data(self, table: str, season: str) -> pd.DataFrame:
        """ Retrieve all data for a specific season """
        data_query = fetch_all_rows(self.supabase, table, filters={"Season": season})
        return pd.DataFrame(data_query)

    # Retrieve All Seasons Data
    st.cache_data
    def retrieve_all_seasons_data(self, table: str, team: str, seasons: list, team_analysis: bool = False) -> pd.DataFrame:
        """ Retrieve all season data for a team with optional opponent stats """
        data_query = fetch_all_rows(self.supabase, table, filters={"Team": team})
        all_seasons_data = pd.DataFrame(data_query)
        all_seasons_data = all_seasons_data[all_seasons_data['Season'].isin(seasons)].reset_index(drop=True)
    
        # if team_analysis:
        #     data_opponent_query = fetch_all_rows(self.supabase, table, filters={"Opponent": team})
        #     opponent_seasons_data = pd.DataFrame(data_opponent_query)
        #     opponent_seasons_data = opponent_seasons_data[opponent_seasons_data['Season'].isin(seasons)].reset_index(drop=True)
        #     opponent_seasons_data.rename(columns={'Goals': 'Goals Ag'}, inplace=True)

        #     all_seasons_data = pd.merge(left=all_seasons_data,
        #                                 right=opponent_seasons_data,
        #                                 on=['Season', 'Week No'])

        return all_seasons_data

    # Retrieve Player Data
    st.cache_data
    def retrieve_all_seasons_player_data(self, table: str, player_name: str, seasons: list) -> pd.DataFrame:
        """ Retrieve all season data for a player """
        data_query = fetch_all_rows(self.supabase, table, filters={"Name": player_name})
        all_seasons_player_data = pd.DataFrame(data_query)
        return all_seasons_player_data[all_seasons_player_data['Season'].isin(seasons)].reset_index(drop=True)
