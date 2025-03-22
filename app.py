import streamlit as st
from supabase import create_client
from PIL import Image
from streamlit_option_menu import option_menu
from python_scripts.data_script import BunesligaInfo, BundesligaGameData
from python_scripts.game_stats_app_scripts.game_stats_utils import GameStatsConfiguration, GameStatsProcessing
from python_scripts.game_stats_app import game_stats_analysis


def main() -> st:

    # ##### Initialize Data
    bundesliga_info = BunesligaInfo()
    bundesliga_game_data = BundesligaGameData()

    # ##### Initialize Configuration
    game_stats_config = GameStatsConfiguration()
    game_stats_processing = GameStatsProcessing()

    # ##### Bundesliga Logo
    st.logo('images/Bundesliga.png', size="large")

    # # ##### Available Seasons
    table_info = game_stats_config.get_tab_info()
    last_5_seasons, _ = bundesliga_info.retrieve_season_info(table=table_info.info_tab)

    # ##### Set Application Name and Options
    st.markdown(f"<h1><font color = #d20614>Bundesliga</font> Stats</h1>", unsafe_allow_html=True)
    st.markdown("")

    # ##### Select Season
    season_selected = st.sidebar.selectbox(label="Season",
                                            options=last_5_seasons,
                                            index=4)

    ##### Select Favourite Team
    available_teams, pos_index = bundesliga_info.retrieve_season_teams(table=table_info.info_tab,
                                                                       season=season_selected)
    favourite_team = st.sidebar.selectbox(label="Team", 
                                          options=available_teams, 
                                          index=pos_index)

    # ##### Game Stats Analysis
    game_stats_analysis(bundesliga_info=bundesliga_info,
                        bundesliga_game_data=bundesliga_game_data,
                        game_stats_config=game_stats_config,
                        game_stats_processing=game_stats_processing,
                        team=favourite_team,
                        season_teams=available_teams,
                        season=season_selected,
                        last_5_seasons=last_5_seasons)

    # ##### App Source Info
    with st.expander(label="Data Source"):
        source_sites, fan_club_logo, _ = st.columns([8, 1, 0.5])
        with source_sites:
            st.markdown(
                f"<b><font color=#d20614>Data Reference</font></b><ul><li><a href='https://fbref.com' "
                "style='text-decoration: none; '>Team & Players Stats</a></li><li><a href='https://www.bundesliga.com' "
                "style='text-decoration: none; '>Tracking Stats</a></li>", unsafe_allow_html=True)

            st.markdown(
                f"<b><font color=#d20614>App Development</font></b><ul><li><a href='https://supabase.com' "
                "style='text-decoration: none; '>Database Storage</a></li><li><a href='https://streamlit.io' "
                "style='text-decoration: none; '>UI Framework</a></li><li><a href='https://github.com/BVBtm86/buli_app'"
                " style='text-decoration: none; '>Code Repo</a></li>", unsafe_allow_html=True)

        with fan_club_logo:
            st.image("http://bvb09.ro/wp-content/uploads/2018/02/BDR_logo-01-1024x1024.png", width=75)


if __name__ == "__main__":

    # ##### Bundesliga App Settings
    st.set_page_config(layout="wide", 
                       page_title="Bundesliga App", 
                       page_icon=Image.open('images/Bundesliga.png'), 
                       initial_sidebar_state="expanded")
    
    # ##### Remove Empty Top Space
    st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

    # ###### Bundesliga Logo CSS Format
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                margin-left: auto;
                margin-right: auto;
                margin-top: -80px;
                width: 50%;
            }
        </style>
        <style>
            section[data-testid="stSidebar"] {
                width: 325px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True)
    
    # ##### Run the App
    main()
