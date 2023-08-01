import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

# ##### Stadiums
stadiums = {"1. FC Köln": "RheinEnergieStadion", "1. FC Nürnberg": "Max-Morlock-Stadion",
            "TSG 1899 Hoffenheim": "PreZero Arena", "Arminia Bielefeld": "Schüco-Arena",
            "Bayer 04 Leverkusen": "BayArena", "FC Bayern München": "Allianz Arena",
            "Borussia Dortmund": "Signal Iduna Park", "Borussia Mönchengladbach": "Borussia-Park",
            "Eintracht Frankfurt": "Commerzbank-Arena", "FC Augsburg": "WWK Arena",
            "Fortuna Düsseldorf": "Merkur Spiel-Arena", "SpVgg Greuther Fürth": "Sportpark Ronhof Thomas Sommer",
            "Hamburger SV": "Volksparkstadion", "Hannover 96": "HDI-Arena", "Hertha Berlin": "Olympiastadion",
            "1. FSV Mainz 05": "Opel Arena", "RasenBallsport Leipzig": "Red Bull Arena",
            "Sport-Club Freiburg": ["Dreisamstadion", "Europa-Park Stadion"], "SC Paderborn 07": "Benteler-Arena",
            "FC Schalke 04": "Veltins-Arena", "1. FC Union Berlin": "Stadion An der Alten Försterei",
            "VfB Stuttgart": "Mercedes-Benz Arena", "VfL Bochum 1848": "Vonovia Ruhrstadion",
            "VfL Wolfsburg": "Volkswagen Arena", "SV Werder Bremen": "Weser-Stadion"}

# ##### General Statistics
general_stats = ["Manager", "Lineup", "Distance Covered (Km)", "Sprints", "Possession", "Duel Aerial Won %",
                 "Offsides", "Corners", "Fouls", "Yellow Cards", "Red Cards"]

general_emoji = ["👨‍💼", "📏", "🚄", "🏃‍", "⚽", "🤼‍", "🚫", "📐", "🤒", "🟨", "🟥"]

# ##### Offensive Statistics
offensive_stats = ["xGoal", "Assists", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %",
                   "Blocked Shots", "Dribbles", "Dribbles %"]

offensive_emoji = ["⚽", "🤝", "🔑", "👟", "🥅", "🎯", "🚫", "⛹️", "✅"]

# ##### Defensive Statistics
defensive_stats = ["Tackles", "Tackles Won %", "Clearances", "Interceptions", "Ball Recoveries", "Blocks", "Errors"]

defensive_emoji = ["🤼", "✅", "🆑", "🥷", "🤒", "🚫️", "⭕"]

# ##### Passing Statistics
passing_stats = ["Ball Touches", "Passes", "Pass %", "Pass Short %", "Pass Medium %", "Pass Long %", "Final Third",
                 "Crosses", "Crosses PA"]

passing_emoji = ["👟", "🔁", "✅", "✅", "✅", "✅", "🥅", "❎", "❎"]

# ##### Goalkeeper Statistics
gk_stats = ["Saves", "Saves %", "Post-Shot xGoal", "Total Passes", "Goal Kicks", "Throws", "Crosses Stopped",
            "Crosses Stopped %"]

gk_emoji = ["🧤", "✅", "⚽", "🔁", "👟", "🤾", "❎", "🚫"]


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


def stats_icons(stats):
    # ##### Return Match Day Stats Icons
    match_day_icons = []
    for i in range(len(stats)):
        if i % 2 == 0:
            match_day_icons.append(
                st.markdown(f'<p style="background-color:#e5e5e6; text-align: center; padding-right: 75rem;">'
                            f'{stats[i]}</p>', unsafe_allow_html=True))
        else:
            match_day_icons.append(st.markdown(f'<p>{stats[i]}</p>', unsafe_allow_html=True))

    return match_day_icons


def match_day_stats(data, home_team, away_team, stats, venue):
    if venue == "Home":
        day_stats = data[(data['Team'] == home_team) & (data['Opponent'] == away_team) &
                         (data['Venue'] == venue)][stats].values[0]
    else:
        day_stats = data[(data['Opponent'] == home_team) & (data['Team'] == away_team) &
                         (data['Venue'] == venue)][stats].values[0]

    game_stats = []
    for i in range(len(day_stats)):
        if i % 2 == 0:
            if stats[i] in ["Possession", "Duel Aerial Won %", "Shot Accuracy %", "Dribbles %", "Tackles Won %",
                            "Saves %", "Crosses Stopped %", "Pass %", "Pass Short %", "Pass Medium %", "Pass Long %"]:
                game_stats.append(
                    st.markdown(f"<p style='text-align: center; background-color:#e5e5e6; 'p>{day_stats[i] / 100:.2%}", unsafe_allow_html=True))
            elif stats[i] in ["Distance Covered (Km)", "xGoal", "Post-Shot xGoal"]:
                game_stats.append(
                    st.markdown(f"<p style='text-align: center; background-color:#e5e5e6; 'p>{day_stats[i]:.1f}", unsafe_allow_html=True))
            else:
                game_stats.append(
                    st.markdown(f"<p style='text-align: center; background-color:#e5e5e6;'p>{day_stats[i]}", unsafe_allow_html=True))
        else:
            if stats[i] in ["Possession", "Duel Aerial Won %", "Shot Accuracy %", "Dribbles %", "Tackles Won %",
                            "Saves %", "Crosses Stopped %", "Pass %", "Pass Short %", "Pass Medium %", "Pass Long %"]:
                game_stats.append(
                    st.markdown(f"<p style='text-align: center;'p>{day_stats[i] / 100:.2%}", unsafe_allow_html=True))
            elif stats[i] in ["Distance Covered (Km)", "xGoal", "Post-Shot xGoal"]:
                game_stats.append(
                    st.markdown(f"<p style='text-align: center;'p>{day_stats[i]:.1f}", unsafe_allow_html=True))
            else:
                game_stats.append(
                    st.markdown(f"<p style='text-align: center;'p>{day_stats[i]}", unsafe_allow_html=True))

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

    st.sidebar.subheader("Options")
    game_venue_options = list(data[data['Team'] == favourite_team]['Venue'].values)
    venue_options = [game_venue_options[-1]]
    all_venue_options = [venue for venue in set(game_venue_options) if venue not in venue_options]
    venue_options.extend(all_venue_options)

    # ##### Match Day Statistics
    venue_filter = st.sidebar.selectbox(label="Select Venue",
                                        options=venue_options)
    st.markdown(f'<b>Match Day Statistics</b> <b><font color = #d20614>{page_season}</font></b>',
                unsafe_allow_html=True)
    season_buli_df = match_day_process_data(data=data,
                                            data_gk=data_gk)
    if venue_filter == 'Home':
        opponent_teams = list(
            season_buli_df[(season_buli_df['Team'] == favourite_team) & (season_buli_df['Venue'] == "Home")][
                'Opponent'].values)
    else:
        opponent_teams = list(
            season_buli_df[(season_buli_df['Team'] == favourite_team) & (season_buli_df['Venue'] == "Away")][
                'Opponent'].values)

    opponent_team = st.sidebar.selectbox(f"Select Opponent",
                                         options=opponent_teams,
                                         index=len(opponent_teams) - 1)

    if venue_filter == 'Home':
        home_team = favourite_team
        away_team = opponent_team
    else:
        home_team = opponent_team
        away_team = favourite_team

    match_day_col, home_logo_col, _, away_logo_col, _ = st.columns([2.75, 3, 0.9, 3, 0.3])
    with home_logo_col:
        st.image(Image.open(f'images/{home_team}.png'))

    with away_logo_col:
        st.image(Image.open(f'images/{away_team}.png'))

    stats_type = ["General", "Offensive", "Defensive", "Passing", "Goalkeeper"]
    stats_options = st.sidebar.selectbox("Statistics", stats_type)

    _, home_score, _, away_score, _ = st.columns([1.25, 2, 0.25, 2, 0.25])
    with home_score:
        home_goals = season_buli_df[
                         (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                         (season_buli_df['Venue'] == 'Home')]['Goals'].values[0] + season_buli_df[
                         (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                         (season_buli_df['Venue'] == 'Away')]['Own Goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{home_goals}</h1>", unsafe_allow_html=True)
    with away_score:
        away_goals = season_buli_df[
                         (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                         (season_buli_df['Venue'] == 'Away')]['Goals'].values[0] + season_buli_df[
                         (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                         (season_buli_df['Venue'] == 'Home')]['Own Goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{away_goals}</h1>", unsafe_allow_html=True)

    # Select Match Day
    match_day = \
        season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                       (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]
    with match_day_col:
        st.markdown(" ")
        st.markdown("<h5 style='text-align: center;'p>General Stats</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)

    icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.25, 1.25, 2.25, 3])
    # ##### General Statistics
    if stats_options == 'General':
        with icon_col:
            stats_icons(stats=general_emoji)

        with stat_name_col:
            [st.markdown(general_stats[i]) for i in range(len(general_stats))]

        with home_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=general_stats,
                            venue="Home")

        with away_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=general_stats,
                            venue="Away")

    # ##### Offensive Statistics
    if stats_options == 'Offensive':
        with icon_col:
            stats_icons(stats=offensive_emoji)

        with stat_name_col:
            [st.markdown(offensive_stats[i]) for i in range(len(offensive_stats))]

        with home_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=offensive_stats,
                            venue="Home")

        with away_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=offensive_stats,
                            venue="Away")

    # ##### Defensive Statistics
    if stats_options == 'Defensive':
        with icon_col:
            stats_icons(stats=defensive_emoji)

        with stat_name_col:
            [st.markdown(defensive_stats[i]) for i in range(len(defensive_stats))]

        with home_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=defensive_stats,
                            venue="Home")

        with away_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=defensive_stats,
                            venue="Away")

    # ##### Passing Statistics
    if stats_options == 'Passing':
        with icon_col:
            stats_icons(stats=passing_emoji)

        with stat_name_col:
            [st.markdown(passing_stats[i]) for i in range(len(passing_stats))]

        with home_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=passing_stats,
                            venue="Home")

        with away_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=passing_stats,
                            venue="Away")

    # ##### Goalkeeper Statistics
    if stats_options == 'Goalkeeper':
        with icon_col:
            stats_icons(stats=gk_emoji)

        with stat_name_col:
            [st.markdown(gk_stats[i]) for i in range(len(gk_stats))]

        with home_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=gk_stats,
                            venue="Home")

        with away_stat_col:
            match_day_stats(data=season_buli_df,
                            home_team=home_team,
                            away_team=away_team,
                            stats=gk_stats,
                            venue="Away")

    # ##### Stadium Info
    _, stadium_logo, _ = st.columns([2, 1, 1])
    with stadium_logo:
        if (home_team == "Sport-Club Freiburg") and (page_season == '2022-2023'):
            stadium_name = stadiums[home_team][1]
        elif (home_team == "Sport-Club Freiburg") and (page_season == '2021-2022') and (match_day > 6):
            stadium_name = stadiums[home_team][1]
        elif (home_team == "Sport-Club Freiburg") and (page_season == '2021-2022') and (match_day <= 6):
            stadium_name = stadiums[home_team][0]
        elif (home_team == "Sport-Club Freiburg") and (page_season != '2021-2022'):
            stadium_name = stadiums[home_team][0]
        else:
            stadium_name = stadiums[home_team]
        st.markdown(f"🏟️ {stadium_name}")
