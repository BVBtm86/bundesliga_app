import pandas as pd
import numpy as np
import streamlit as st

# ########## Supabase Tables
info_tab = "buli_seasons_info"
team_stats_tab = "buli_stats_team"
player_stats_tab = "buli_stats_player"
gk_stas_tab = "buli_stats_gk"

# ##### Team Logo
team_logos_config = {
    "1. FC Heidenheim 1846": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Heidenheim.png",
    "1. FC Köln": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Koeln.png", 
    "1. FC Nürnberg": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Nuernberg.png", 
    "1. FC Union Berlin": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Union-Berlin.png", 
    "1. FSV Mainz 05": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Mainz.png", 
    "Arminia Bielefeld": "https://img.bundesliga.com/tachyon/sites/2/2021/08/Bielefeld.png",
    "Bayer 04 Leverkusen": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Leverkusen.png", 
    "Borussia Dortmund": "https://assets.bundesliga.com/tachyon/sites/2/2022/06/Dortmund-BVB.png", 
    "Borussia Mönchengladbach": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Moenchengladbach.png", 
    "Eintracht Frankfurt": "https://assets.bundesliga.com/tachyon/sites/2/2022/06/Frankfurt-SGE.png", 
    "FC Augsburg": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Augsburg.png", 
    "FC Bayern München": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Bayern.png", 
    "FC Schalke 04": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Schalke.png", 
    "Fortuna Düsseldorf": "https://img.bundesliga.com/tachyon/sites/2/2019/07/F95-1.png", 
    "Hamburger SV": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Hamburg.png", 
    "Hannover 96": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Hannover.png", 
    "Hertha Berlin": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Berlin.png", 
    "RasenBallsport Leipzig": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Leipzig.png", 
    "SC Paderborn 07": "https://img.bundesliga.com/tachyon/sites/2/2019/07/SCP-1.png", 
    "Sport-Club Freiburg": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Freiburg.png", 
    "SpVgg Greuther Fürth": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Fuerth.png", 
    "SV Darmstadt 98": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Darmstadt.png",
    "SV Werder Bremen": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Bremen.png",
    "TSG 1899 Hoffenheim": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Hoffenheim.png", 
    "VfB Stuttgart": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Stuttgart.png", 
    "VfL Bochum 1848": "https://assets.bundesliga.com/tachyon/sites/2/2021/08/Bochum.png", 
    "VfL Wolfsburg": "https://assets.bundesliga.com/tachyon/sites/2/2022/06/Wolfsburg-WOB.png", 
    }


# ##### Team Stadium
team_stadiums_config = {
    "1. FC Heidenheim 1846": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00001E_B.png?fit=64,64", "Voith-Arena"],
    "1. FC Köln": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000008_B.png?fit=64,64", "RheinEnergieStadion"], 
    "1. FC Nürnberg":["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000I_B.png?fit=64,64", "Max-Morlock-Stadion"], 
    "1. FC Union Berlin": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000M_B.png?fit=64,64", "Stadion An der Alten Försterei"], 
    "1. FSV Mainz 05": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000E_B.png?fit=64,64", "Opel Arena"], 
    "Arminia Bielefeld": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00001A_B.png?fit=64,64", "Schüco-Arena"],
    "Bayer 04 Leverkusen": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000004_B.png?fit=64,64", "BayArena"], 
    "Borussia Dortmund": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000A_B.png?fit=64,64", "Signal Iduna Park"],
    "Borussia Mönchengladbach": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000002_B.png?fit=64,64", "Borussia-Park"], 
    "Eintracht Frankfurt": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000H_B.png?fit=64,64", "Commerzbank-Arena"], 
    "FC Augsburg": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000011_B.png?fit=64,64","WWK Arena"], 
    "FC Bayern München": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000006_B.png?fit=64,64", "Allianz Arena"], 
    "FC Schalke 04": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000005_B.png?fit=64,64", "Veltins-Arena"], 
    "Fortuna Düsseldorf": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000P_B.png?fit=64,64", "Merkur Spiel-Arena"], 
    "Hamburger SV": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000001_B.png?fit=64,64", "Volksparkstadion"], 
    "Hannover 96": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-J00290_B.png?fit=64,64", "HDI-Arena"], 
    "Hertha Berlin": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000010_B.png?fit=64,64", "Olympiastadion"], 
    "RasenBallsport Leipzig": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00001F_B.png?fit=64,64", "Red Bull Arena"], 
    "SC Paderborn 07": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-J0028Z_B.png?fit=64,64", "Benteler-Arena"], 
    "Sport-Club Freiburg": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-J0026L_B.png?fit=64,64", "Dreisamstadion", "Europa-Park Stadion"], 
    "SpVgg Greuther Fürth": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000N_B.png?fit=64,64", "Sportpark Ronhof Thomas Sommer"], 
    "SV Darmstadt 98": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00001D_B.png?fit=64,64", "Merck-Stadion am Böllenfalltor"],
    "SV Werder Bremen": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000C_B.png?fit=64,64", "Weser-Stadion"],
    "TSG 1899 Hoffenheim": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000NAI_B.png?fit=64,64", "PreZero Arena"], 
    "VfB Stuttgart": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-00000B_B.png?fit=64,64", "Mercedes-Benz Arena"], 
    "VfL Bochum 1848": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000N71_B.png?fit=64,64", "Vonovia Ruhrstadion"], 
    "VfL Wolfsburg": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000003_B.png?fit=64,64", "Volkswagen Arena"], 
}

# ##### Season Filter
season_filter = ['Season', 'Form', 'Home', 'Away', '1st Half', '2nd Half', 'Win', 'Draw', 'Defeat']

# ##### Team Most Important Stats
team_most_important_stats = ['xGoal', 'Possession', 'Distance Covered (Km)', 'Shots', 'Goals', 'Goals Ag']

# ##### General Statistics
general_stats = ["Manager", "Lineup", "Distance Covered (Km)", "Sprints", "Possession", "Duel Aerial Won %", "Offsides", "Corners", "Fouls", "Yellow Cards", "Red Cards"]
general_emoji = ["👨‍💼", "📏", "🚄", "🏃‍", "⚽", "🤼‍", "🚫", "📐", "🤒", "🟨", "🟥"]

# ##### Offensive Statistics
offensive_stats = ["xGoal", "Assists", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %", "Blocked Shots", "Dribbles", "Dribbles %"]
offensive_emoji = ["⚽", "🤝", "🔑", "👟", "🥅", "🎯", "🚫", "⛹️", "✅"]

# ##### Defensive Statistics
defensive_stats = ["Tackles", "Tackles Won %", "Clearances", "Interceptions", "Ball Recoveries", "Blocks", "Errors"]
defensive_emoji = ["🤼", "✅", "🆑", "🥷", "🤒", "🚫️", "⭕"]

# ##### Passing Statistics
passing_stats = ["Ball Touches", "Passes", "Pass %", "Pass Short %", "Pass Medium %", "Pass Long %", "Final Third", "Crosses", "Crosses PA"]
passing_emoji = ["👟", "🔁", "✅", "✅", "✅", "✅", "🥅", "❎", "❎"]

# ##### Goalkeeper Statistics
gk_stats = ["Saves", "Saves %", "Post-Shot xGoal", "Total Passes", "Goal Kicks", "Throws", "Crosses Stopped", "Crosses Stopped %"]
gk_emoji = ["🧤", "✅", "⚽", "🔁", "👟", "🤾", "❎", "🚫"]

# ##### Statistics Config
match_stats_config = {
    'stat_name':["General", "Offensive", "Defensive", "Passing", "Goalkeeper"],
    'stat_type': [general_stats, offensive_stats, defensive_stats, passing_stats, gk_stats],
    'stat_emoji': [general_emoji, offensive_emoji, defensive_emoji, passing_emoji, gk_emoji],
}

# ##### Stats
stats_team = ['Possession', 'Distance Covered (Km)', 'Sprints', 'Goals', 'Assists', 'xGoal', 'xAssist', 'Goal Created Action', 'Non-Penalty xGoal', 'xGoal Assist', 
              'Shots', 'Shots on Target', 'Shot Accuracy %', 'Shot Created Action', 'Key Passes', 'Penalty Goal', 'Penalty Attempted', 'Own Goals', 'Passes', 
              'Passes Completed', 'Passes Completed %', 'Passes Short', 'Passes Short Completed','Passes Short Completed %', 'Passes Medium', 'Passes Medium Completed', 
              'Passes Medium Completed %', 'Passes Long', 'Passes Long Completed', 'Passes Long Completed %', 'Passes Final Third', 'Passes PA', 'Progressive Passes', 
              'Passes Distance', 'Passes Progressive Distance', 'Passes Received', 'Progressive Passes Received', 'Passes Free Kicks', 'Passes Live', 'Passes Dead', 
              'Passes Switches', 'Passes Blocked', 'Through Balls', 'Ball Touches', 'Touches Def PA', 'Touches Def 3rd', 'Touches Mid 3rd', 'Touches Att 3rd', 
              'Touches Att PA', 'Touches Live Ball', 'Dribbles', 'Dribbles Completed', "Dribbles Completed %", 'Crosses', 'Crosses PA', 'Interceptions', 
              'Ball Recoveries', 'Tackles','Tackles Won', 'Tackles Won %', 'Tackles Def 3rd', 'Tackles Mid 3rd', 'Tackles Att 3rd', 'Duel Aerial Won',  
              'Duel Aerial Won %', 'Duel Aerial Lost', 'Dribbles Tackled', 'Dribbles Tackled %', 'Dribbles Contested','Dribbled Past', 'Blocks', 'Blocked Shots', 
              'Blocked Passes', 'Clearances', 'Corners', 'Offsides', 'Penalty Won', 'Penalty Conceded', 'Throw Ins', 'Misscontrols', 'Dispossessed', 'Fouls', 'Fouled', 
              'Yellow Cards', 'Red Cards', 'Errors', 'Saves', 'Saves %', 'Goal Kicks', 'Throws', 'Crosses Stopped', 'Crosses Stopped %']

# ##### Aggregate Stats for Count Calculation
stats_count_calculations = ['Possession', 'Goals', 'Assists', 'Shots', 'Shots on Target', 'xGoal', 'Non-Penalty xGoal', 'xGoal Assist', 'xAssist', 
              'Goal Created Action', 'Shot Created Action', 'Key Passes', 'Penalty Goal', 'Penalty Attempted', 'Own Goals', 'Distance Covered (Km)', 'Sprints',
              'Passes', 'Passes Completed', 'Passes Short', 'Passes Short Completed', 'Passes Medium', 
              'Passes Medium Completed', 'Passes Long', 'Passes Long Completed', 'Passes Final Third', 
              'Passes PA', 'Progressive Passes', 'Passes Distance', 'Passes Progressive Distance', 'Passes Received', 'Progressive Passes Received', 
              'Passes Free Kicks', 'Passes Live', 'Passes Dead', 'Passes Switches', 'Passes Blocked', 'Through Balls', 'Ball Touches', 
              'Touches Def PA', 'Touches Def 3rd', 'Touches Mid 3rd', 'Touches Att 3rd', 'Touches Att PA', 'Touches Live Ball', 'Dribbles', 'Dribbles Completed', 
              'Crosses', 'Crosses PA', 'Interceptions', 'Ball Recoveries', 'Corners', 
              'Tackles', 'Tackles Won', 'Tackles Def 3rd', 'Tackles Mid 3rd', 'Tackles Att 3rd', 
              'Duel Aerial Won', 'Duel Aerial Lost', 'Dribbles Tackled', 'Dribbles Contested', 'Dribbled Past', 'Blocks', 
              'Blocked Shots', 'Blocked Passes', 'Clearances', 'Offsides', 'Penalty Won', 'Penalty Conceded', 'Throw Ins', 'Misscontrols', 'Dispossessed', 'Fouls', 
              'Fouled', 'Yellow Cards', 'Red Cards', 'Errors', 'Saves', 'Goal Kicks', 'Throws', 'Crosses Stopped']

# ##### Aggregate Stats for Percentage Calculation
stats_perc_calculations = {'Shot Accuracy %': ['Shots', 'Shots on Target'], 'Passes Completed %': ['Passes', 'Passes Completed'], 
                           'Passes Short Completed %': ['Passes Short', 'Passes Short Completed'], 
                           'Passes Medium Completed %': ['Passes Medium', 'Passes Medium Completed'], 
                           'Passes Long Completed %': ['Passes Long', 'Passes Long Completed'],  'Dribbles Completed %':  ['Dribbles', 'Dribbles Completed'], 
                           'Tackles Won %': ['Tackles', 'Tackles Won'], 'Duel Aerial Won %': ['Duel Aerial', 'Duel Aerial Won'], 
                           'Dribbles Tackled %': ['Dribbles Contested', 'Dribbles Tackled'], 'Saves %': ['Shots on Target', 'Saves'], 
                           'Crosses Stopped %': ['Crosses', 'Crosses Stopped']}

# ##### Previous Season for Each Current Season
previous_seasons = {'2019-2020':'2018-2019', 
                    '2020-2021':'2019-2020', 
                    '2021-2022':'2020-2021', 
                    '2022-2023':'2021-2022'}

# ##### Process Bundesliga Team and Gk Data
st.cache_data(ttl=3600)
def process_team_data(data, data_gk):
    # ##### Read Data
    buli_df = data.copy()
    buli_gk_df = data_gk.copy()

    # ##### Change Name Statistics
    buli_df['Team_Lineup'] = buli_df['Team_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df['Opp_Lineup'] = buli_df['Opp_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df.rename(columns={"Team_Lineup": "Lineup",
                            "Corner Kicks": "Corners",
                            "Dribbles Completed %": "Dribbles %",
                            "Passes Completed %": 'Pass %',
                            "Passes Short Completed %": 'Pass Short %',
                            "Passes Medium Completed %": 'Pass Medium %',
                            "Passes Long Completed %": 'Pass Long %',
                            "Passes Final 3rd": 'Final Third'}, inplace=True)
    
    # ##### Goals Statistics
    home_df = buli_df[buli_df['Venue'] == 'Home'].copy()
    home_df.reset_index(drop=True, inplace=True)
    away_df = buli_df[buli_df['Venue'] == 'Away'].copy()
    away_df.reset_index(drop=True, inplace=True)
    home_df['Goals'] = home_df['Goals'] + away_df['Own Goals']
    away_df['Goals'] = away_df['Goals'] + home_df['Own Goals']
    home_df['Goals Ag'] = away_df['Goals']
    away_df['Goals Ag'] = home_df['Goals']
    final_buli_df = pd.concat([home_df, away_df])
    final_buli_df = final_buli_df.sort_values(by=['Id'])
    final_buli_df.reset_index(drop=True, inplace=True)

    # ##### Aggregate Goalkeeper Statistics
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

    # ##### Create Final Bundesliga data
    final_buli_df = pd.merge(left=final_buli_df, 
                             right=df_team_gk, 
                             left_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'],
                             right_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'])
    final_buli_df = final_buli_df.reset_index(drop=True)

    return final_buli_df


# ##### Process Season Bundesliga Data
st.cache_data(ttl=3600)
def filter_season_data(data):
    buli_df = data.copy()

    # ##### Creating Tabel Stats Filter
    buli_df['Win'] = np.where(buli_df['Result'] == 'Win', 1, 0)
    buli_df['Draw'] = np.where(buli_df['Result'] == 'Draw', 1, 0)
    buli_df['Defeat'] = np.where(buli_df['Result'] == 'Defeat', 1, 0)
    buli_df['Season'] = 1
    buli_df['Home'] = np.where(buli_df['Venue'] == "Home", 1, 0)
    buli_df['Away'] = np.where(buli_df['Venue'] == "Away", 1, 0)
    buli_df["1st Half"] = np.where(buli_df["Week_No"] <= 17, 1, 0)
    buli_df["2nd Half"] = np.where(buli_df["Week_No"] >= 18, 1, 0)
    form_games = list(buli_df["Week_No"].unique())[-5:]
    buli_df["Form"] = np.where(buli_df["Week_No"].isin(form_games),1, 0)

    return buli_df

# ##### Metrics Cars Style
def style_metric_cards(
        background_color: str = "#e5e5e6",
        border_radius_px: int = 15,
        border_top_color: str = "#d20614",
        border_left_color: str = "#d20614",
        border_right_color: str = "#ffffff",
        border_bottom_color: str = "#ffffff",
        box_shadow: bool = True,
    ):

        box_shadow_str = ("box-shadow: 0 0 1rem 0 #e5e5e6 !important;" if box_shadow 
                            else "box-shadow: none !important;")
        st.markdown(
            f"""
            <style>
                div[data-testid="metric-container"] {{
                    background-color: {background_color};
                    padding: 5% 5% 5% 5%;
                    border-radius: {border_radius_px}px;
                    border-top: 0.2rem solid {border_top_color} !important;
                    border-left: 0.2rem solid {border_left_color} !important;
                    border-bottom: 0.2rem solid {border_bottom_color} !important;
                    border-right: 0.2rem solid {border_right_color} !important;
                    {box_shadow_str}
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
