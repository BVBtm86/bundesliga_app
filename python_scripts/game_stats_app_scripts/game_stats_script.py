import pandas as pd
import streamlit as st
from python_scripts.game_stats_app_scripts.game_stats_utils import GameDayStats

# ##### Game Stats Page
def game_stats_page(data:pd.DataFrame, 
                    page_season:str, 
                    favourite_team:str) -> st:
    
    # ##### Initialize Game Stats
    game_day_stats = GameDayStats()

    # ##### Style Team Logo
    st.markdown(
        """
        <style>
            [data-testid=stImage]{
                margin-left: 90px;
                width:25%;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # ##### Season Data
    season_buli_df = data.copy()

    # ##### Game Statistics Page Options
    st.sidebar.subheader("Options")

    # ##### Venue Options per Favourite Team
    game_venue_options = list(data[data['Team'] == favourite_team]['Venue'].values)
    venue_options = [game_venue_options[-1]]
    all_venue_options = [venue for venue in set(game_venue_options) if venue not in venue_options]
    venue_options.extend(all_venue_options)

    # ##### Select Match Day Venue
    venue_filter = st.sidebar.selectbox(label="Venue",
                                        options=venue_options)
    st.markdown(f'<b>Match Day Statistics</b> <b><font color = #d20614>{page_season}</font></b>',
                unsafe_allow_html=True)
    
    # ##### Select Opponent Team
    if venue_filter == 'Home':
        opponent_teams = list(
            season_buli_df[(season_buli_df['Team'] == favourite_team) & (season_buli_df['Venue'] == "Home")]['Opponent'].values)
    else:
        opponent_teams = list(
            season_buli_df[(season_buli_df['Team'] == favourite_team) & (season_buli_df['Venue'] == "Away")]['Opponent'].values)
    opponent_team = st.sidebar.selectbox(f"Opponent",
                                         options=opponent_teams,
                                         index=len(opponent_teams) - 1)

    # ##### Based on Previous Selection define Home/Away Team
    if venue_filter == 'Home':
        home_team = favourite_team
        away_team = opponent_team
    else:
        home_team = opponent_team
        away_team = favourite_team

    # ##### Home/Away Team Logo
    match_day_col, home_logo_col, _, away_logo_col, _ = st.columns([2.75, 3, 0.9, 3, 0.3])
    with home_logo_col:
        st.image(game_day_stats.teams_info['config_teams_logo'][home_team])

    with away_logo_col:
        st.image(game_day_stats.teams_info['config_teams_logo'][away_team])

    ##### Match Day Statistic Sype
    stats_option = st.sidebar.selectbox(label="Statistics", 
                                        options=game_day_stats.stats_game.stat_name)

    # ##### Home/Away Score
    _, home_score, _, away_score, _ = st.columns([1.25, 2, 0.25, 2, 0.25])
    with home_score:
        home_goals = season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) & (season_buli_df['Venue'] == 'Home')]['Goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{home_goals}</h1>", unsafe_allow_html=True)
    with away_score:
        away_goals = season_buli_df[(season_buli_df['Team'] == away_team) & (season_buli_df['Opponent'] == home_team) & (season_buli_df['Venue'] == 'Away')]['Goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{away_goals}</h1>", unsafe_allow_html=True)

    # ##### Match Day based on Home and Away Team selected
    match_day = \
        season_buli_df[(season_buli_df['Team'] == home_team) & 
                       (season_buli_df['Opponent'] == away_team) &
                       (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]

    # ##### Statistics Type Config
    icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.25, 1.25, 2.25, 3])
    stat_selection = game_day_stats.stats_game.stat_name.index(stats_option)

    # ##### Stat Option
    with match_day_col:
        st.markdown(" ")
        st.markdown(f"<h5 style='text-align: center;'p><font color = #d20614>{game_day_stats.stats_game.stat_name[stat_selection]}</font> Stats</h5>", 
                    unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'p>Match Day: <b>{match_day}</b></p>", unsafe_allow_html=True)
    
    # ##### Stat Icon
    with icon_col:
        game_day_stats.stat_name_icon(stats=game_day_stats.stats_game.stat_emoji[stat_selection])

    # ##### Stat Name
    with stat_name_col:
        game_day_stats.stat_name_icon(stats=game_day_stats.stats_game.stat_type[stat_selection])

    # ##### Stat Home Team
    with home_stat_col:
        game_day_stats.game_stats(data=season_buli_df,
                                  home_team=home_team,
                                  away_team=away_team,
                                  stats=game_day_stats.stats_game.stat_type[stat_selection],
                                  venue="Home")
        
    # ##### Stat Away Team
    with away_stat_col:
        game_day_stats.game_stats(data=season_buli_df,
                                  home_team=home_team,
                                  away_team=away_team,
                                  stats=game_day_stats.stats_game.stat_type[stat_selection],
                                  venue="Away")

    # ##### Stadium Info
    _, stadium_logo_col, stadium_name_col, _ = st.columns([3.5, 0.9, 2.25, 1])
    with stadium_logo_col:
        st.image(game_day_stats.teams_info['config_team_stadiums'][home_team][0], width=55)

    with stadium_name_col:
        st.markdown("")
        if home_team == "Sport-Club Freiburg":
            if page_season in ['2022-2023', '2023-2024']:
                st.markdown(f"<i>{game_day_stats.teams_info['config_team_stadiums'][home_team][2]}</i>", unsafe_allow_html=True)
            elif home_team == "Sport-Club Freiburg" and page_season=='2021-2022' and match_day > 6:
                st.markdown(f"<i>{game_day_stats.teams_info['config_team_stadiums'][home_team][2]}</i>", unsafe_allow_html=True)
            else:
                st.markdown(f"<i>{game_day_stats.teams_info['config_team_stadiums'][home_team][1]}</i>", unsafe_allow_html=True)
        else:
            st.markdown(f"<i>{game_day_stats.teams_info['config_team_stadiums'][home_team][1]}</i>", unsafe_allow_html=True)
