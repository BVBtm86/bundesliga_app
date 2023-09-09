import streamlit as st
from supabase import create_client
from PIL import Image
from streamlit_option_menu import option_menu
from python_scripts.game_stats_scripts.game_stats_utils import supabase_tab_info
from python_scripts.data_script import retrieve_season_info, retrieve_season_teams
from python_scripts.game_stats_app import game_stats_analysis


def main() -> st:

    # ##### Bundesliga Logo
    st.sidebar.image(Image.open('images/Bundesliga.png'))

    # ##### Available Seasons
    last_5_seasons, last_5_seasons_id = retrieve_season_info(table=supabase_tab_info.info_tab)

    # ##### Set Application Name and Options
    st.markdown(f"<h1><font color = #d20614>Bundesliga</font> Application</h1>", unsafe_allow_html=True)
    st.markdown("")

    # ##### Select App Analysis 
    app_main_menu = ["Game Statistics", "Game Events"]
    app_selection = option_menu(menu_title=None,
                                options=app_main_menu,
                                icons=["clipboard-data-fill", "fast-forward-circle-fill"],
                                orientation="horizontal",
                                styles={
                                    "container": {"width": "100%!important",
                                                  "background-color": "#e5e5e6"},
                                    "nav-link": {"--hover-color": "#ffffff"},
                                })

    # ##### Select Season
    season_selected = st.sidebar.selectbox(label="Select Season",
                                            options=last_5_seasons,
                                            index=4)

    # ##### Select Favourite Team
    available_teams, pos_index = retrieve_season_teams(table=supabase_tab_info.info_tab,
                                                       season=season_selected)
    favourite_team = st.sidebar.selectbox(label="Select Team", 
                                          options=available_teams, 
                                          index=pos_index)

    # ##### Game Stats Analysis
    if app_selection == "Game Statistics":

        # ##### Game Stats Page
        game_stats_analysis(team=favourite_team,
                            season_teams=available_teams,
                            season=season_selected,
                            last_5_seasons=last_5_seasons)

    # ##### Game Events Analysis
    elif app_selection == "Game Events":
        
        # ##### Game Events Analysis
        pass

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
                width: 300px; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True)
    
    # ##### Run the App
    main()
