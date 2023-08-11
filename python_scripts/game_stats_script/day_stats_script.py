import pandas as pd
import numpy as np
import streamlit as st
from python_scripts.game_stats_script.game_stats_config import match_stats_config, team_logos_config, team_stadiums_config



def match_day_process_data(data, data_gk):
    # ##### Read Data
    buli_df = data.copy()
    buli_gk_df = data_gk.copy()

    # ##### Change Name Statistics
    buli_df['Team_Lineup'] = buli_df['Team_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df['Opp_Lineup'] = buli_df['Opp_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df.rename(columns={"Team_Lineup": "Lineup",
                            "Corner Kicks": "Corners",
                            "Dribbles": "Dribbles",
                            "Dribbles Completed": "Dribbles Completed",
                            "Dribbles Completed %": "Dribbles %",
                            "Passes Completed %": 'Pass %',
                            "Passes Short Completed %": 'Pass Short %',
                            "Passes Medium Completed %": 'Pass Medium %',
                            "Passes Long Completed %": 'Pass Long %',
                            "Passes Final 3rd": 'Final Third'}, inplace=True)

    # ##### Add Team Goalkeeper Statistics
    df_team_gk = \
        buli_gk_df.groupby(["Season", "Week_No", "Team", "Opponent", "Venue"])[["Shots on Target",
                                                                                "Saves", "Post-Shot xGoal",
                                                                                "Passes", "Goal Kicks", "Throws",
                                                                                "Crosses Faced",
                                                                                "Crosses Stopped"]].sum()

    df_team_gk.reset_index(inplace=True)
    df_team_gk['Saves %'] = np.round(df_team_gk['Saves'] / df_team_gk['Shots on Target'] * 100, 2)
    df_team_gk['Crosses Stopped %'] = np.round(df_team_gk['Crosses Stopped'] / df_team_gk['Crosses Faced'] * 100, 2)
    df_team_gk.drop(columns=['Shots on Target', "Crosses Faced"], inplace=True)
    df_team_gk.rename(columns={"Passes": "Total Passes"}, inplace=True)
    buli_df = pd.merge(buli_df, df_team_gk, left_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'],
                       right_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'])
    season_buli_df = buli_df.reset_index(drop=True)

    return season_buli_df


def stat_name_icon(stats):
    # ##### Return Match Day Stats Icons
    match_day_name_icon = []
    for i in range(len(stats)):
        match_day_name_icon.append(st.markdown(f'<p>{stats[i]}</p>', unsafe_allow_html=True))
    return match_day_name_icon


def match_day_stats(data, home_team, away_team, stats, venue):
    if venue == "Home":
        day_stats = data[(data['Team'] == home_team) & (data['Opponent'] == away_team) &
                         (data['Venue'] == venue)][stats].values[0]
    else:
        day_stats = data[(data['Opponent'] == home_team) & (data['Team'] == away_team) &
                         (data['Venue'] == venue)][stats].values[0]

    game_stats = []
    for i in range(len(day_stats)):
        if stats[i] in ["Possession", "Duel Aerial Won %", "Shot Accuracy %", "Dribbles %", "Tackles Won %",
                        "Saves %", "Crosses Stopped %", "Pass %", "Pass Short %", "Pass Medium %", "Pass Long %"]:
            game_stats.append(st.markdown(f"<p style='text-align: center;'p>{day_stats[i] / 100:.1%}", unsafe_allow_html=True))
        elif stats[i] in ["Distance Covered (Km)", "xGoal", "Post-Shot xGoal"]:
            game_stats.append(st.markdown(f"<p style='text-align: center;'p>{day_stats[i]:.1f}", unsafe_allow_html=True))
        elif stats[i] in ['Manager', 'Lineup']:
            st.markdown(f"<p style='text-align: center;'p>{day_stats[i]}", unsafe_allow_html=True)
        else:
            game_stats.append(st.markdown(f"<p style='text-align: center;'p>{day_stats[i]:.0f}", unsafe_allow_html=True))

    return game_stats


def match_day_page(data, data_gk, page_season, favourite_team):
    
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
    season_buli_df = match_day_process_data(data=data,
                                            data_gk=data_gk)

    # ##### Match Day Page Options
    st.sidebar.subheader("Options")

    # ##### Venue Options per Favourite Team
    game_venue_options = list(data[data['Team'] == favourite_team]['Venue'].values)
    venue_options = [game_venue_options[-1]]
    all_venue_options = [venue for venue in set(game_venue_options) if venue not in venue_options]
    venue_options.extend(all_venue_options)

    # ##### Select Match Day Venue
    venue_filter = st.sidebar.selectbox(label="Select Venue",
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
    opponent_team = st.sidebar.selectbox(f"Select Opponent",
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
        st.image(team_logos_config[home_team])

    with away_logo_col:
        st.image(team_logos_config[away_team])

    # ##### Match Day Statistic Sype
    stats_option = st.sidebar.selectbox(label="Statistics", 
                                        options=match_stats_config['stat_name'])

    # ##### Home/Away Score
    _, home_score, _, away_score, _ = st.columns([1.25, 2, 0.25, 2, 0.25])
    with home_score:
        home_goals = season_buli_df[(season_buli_df['Team'] == home_team) & 
                                    (season_buli_df['Opponent'] == away_team) & 
                                    (season_buli_df['Venue'] == 'Home')]['Goals'].values[0] + season_buli_df[(season_buli_df['Opponent'] == home_team) & 
                                    (season_buli_df['Team'] == away_team) & 
                                    (season_buli_df['Venue'] == 'Away')]['Own Goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{home_goals}</h1>", unsafe_allow_html=True)
    with away_score:
        away_goals = season_buli_df[(season_buli_df['Opponent'] == home_team) & 
                                    (season_buli_df['Team'] == away_team) & 
                                    (season_buli_df['Venue'] == 'Away')]['Goals'].values[0] + season_buli_df[(season_buli_df['Team'] == home_team) & 
                                    (season_buli_df['Opponent'] == away_team) & 
                                    (season_buli_df['Venue'] == 'Home')]['Own Goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{away_goals}</h1>", unsafe_allow_html=True)

    # ##### Match Day based on Home and Away Team selected
    match_day = \
        season_buli_df[(season_buli_df['Team'] == home_team) & 
                       (season_buli_df['Opponent'] == away_team) &
                       (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]

    # ##### Statistics Type Config
    icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.25, 1.25, 2.25, 3])
    stat_selection = match_stats_config['stat_name'].index(stats_option)

    # ##### Stat Option
    with match_day_col:
        st.markdown(" ")
        st.markdown(f"<h5 style='text-align: center;'p><font color = #d20614>{match_stats_config['stat_name'][stat_selection]}</font> Stats</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)

    # ##### Stat Icon
    with icon_col:
        stat_name_icon(stats=match_stats_config["stat_emoji"][stat_selection])

    # ##### Stat Name
    with stat_name_col:
        stat_name_icon(stats=match_stats_config['stat_type'][stat_selection])

    # ##### Stat Home Team
    with home_stat_col:
        match_day_stats(data=season_buli_df,
                        home_team=home_team,
                        away_team=away_team,
                        stats=match_stats_config['stat_type'][stat_selection],
                        venue="Home")
        
    # ##### Stat Away Team
    with away_stat_col:
        match_day_stats(data=season_buli_df,
                        home_team=home_team,
                        away_team=away_team,
                        stats=match_stats_config['stat_type'][stat_selection],
                        venue="Away")

    # ##### Stadium Info
    _, stadium_logo_col, stadium_name_col, _ = st.columns([3.5, 0.9, 2.25, 1])
    with stadium_logo_col:
        st.image(team_stadiums_config[home_team][0], width=55)

    with stadium_name_col:
        st.markdown("")
        if home_team == "Sport-Club Freiburg":
            if page_season in ['2022-2023', '2023-2024']:
                st.markdown(f"<i>{team_stadiums_config[home_team][2]}</i>", unsafe_allow_html=True)
            elif home_team == "Sport-Club Freiburg" and page_season=='2021-2022' and match_day > 6:
                st.markdown(f"<i>{team_stadiums_config[home_team][2]}</i>", unsafe_allow_html=True)
            else:
                st.markdown(f"<i>{team_stadiums_config[home_team][1]}</i>", unsafe_allow_html=True)
        else:
            st.markdown(f"<i>{team_stadiums_config[home_team][1]}</i>", unsafe_allow_html=True)
