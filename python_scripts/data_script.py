import pandas as pd
from supabase import create_client
import streamlit as st


# ########## Supabase Connection
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]

    return create_client(url, key)


# #################################################################################################### Bundesliga Info
class BunesligaInfo:

    def __init__(self) -> None:
        st.cache_resource()
        self.supabase = init_connection()


    # ########## Retrieve Season Info
    st.cache_data
    def retrieve_season_info(self, table:str) -> tuple[pd.DataFrame, pd.DataFrame]:
        """ Available Seasons query """
        data_query = self.supabase.table(table).select('*').execute().data
        data = pd.DataFrame(data_query)
        all_seasons = list(data['Season'].unique())
        game_stats_seasons = all_seasons[-5:]
        all_seasons_id = list(data['Season'].unique())
        game_id_seasons = all_seasons_id[-5:]

        return game_stats_seasons, game_id_seasons

    # ########## Retrieve Season Games
    def retrieve_season_games(self, table:str, season:str) -> pd.DataFrame:
        """ Season Games Schedule """
        data_query = self.supabase.table(table).select('*').eq('Season', season).execute().data
        season_games = pd.DataFrame(data_query)

        return season_games


    # ########## Retrieve Season Teams
    def retrieve_season_teams(self, table:str, season:str) -> tuple[pd.DataFrame, int]:
        """ Teams per Season query """
        data_query = self.supabase.table(table).select('*').eq('Season', season).execute().data
        data = pd.DataFrame(data_query)
        all_teams = list(data[data['Season'] == season]['Team'].values)
        all_teams.sort()
        bvb_position = all_teams.index("Borussia Dortmund")

        return all_teams, bvb_position


# #################################################################################################### Game Stats Data
class BundesligaGameData:

    def __init__(self) -> None:
        st.cache_resource()
        self.supabase = init_connection()


    # ########## Retrieve Season Data
    st.cache_data
    def retrieve_season_data(self, table:str, season:str) -> pd.DataFrame:
        """ Return Season Data """
        data_query = self.supabase.table(table).select('*').eq('Season', season).execute().data
        season_data = pd.DataFrame(data_query)  

        return season_data


    # ########## Retrieve Last 5 Seasons Data
    st.cache_data
    def retrieve_all_seasons_data(self, table:str, team:str, seasons:str, team_analysis:bool=False) -> pd.DataFrame:
        """ Return All Seasons Data """
        data_query = self.supabase.table(table).select('*').eq('Team', team).execute().data
        all_seasons_data = pd.DataFrame(data_query)
        all_seasons_data = all_seasons_data[all_seasons_data['Season'].isin(seasons)].reset_index(drop=True)

        if team_analysis:
            data_opponent_query = self.supabase.table(table).select('Season', 'Week_No', 'Goals').eq('Opponent', team).execute().data
            opponent_seasons_data = pd.DataFrame(data_opponent_query)
            opponent_seasons_data = opponent_seasons_data[opponent_seasons_data['Season'].isin(seasons)].reset_index(drop=True)
            opponent_seasons_data.rename(columns={'Goals':'Goals Ag'}, inplace=True)
            all_seasons_data = pd.merge(left=all_seasons_data,
                                        right=opponent_seasons_data,
                                        on=['Season', 'Week_No'])

        return all_seasons_data

    st.cache_data
    def retrieve_all_seasons_player_data(self, table:str, player_name:str, seasons:str) -> pd.DataFrame:
        """ Retrieve All Players Season Data """
        data_query = self.supabase.table(table).select('*').eq('Name', player_name).execute().data
        all_seasons_player_data = pd.DataFrame(data_query)
        all_seasons_player_data = all_seasons_player_data[all_seasons_player_data['Season'].isin(seasons)].reset_index(drop=True)

        return all_seasons_player_data


# #################################################################################################### Game Events Analysis

