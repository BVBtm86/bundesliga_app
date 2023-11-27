import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from ml_collections import config_dict
from mplsoccer import Radar, grid

# ########## Supabase Tables
tab_info_dict = {
    'info_tab': "buli_seasons_info",
    'games_tab': "buli_games_schedule",
    'team_stats_tab': "buli_stats_team",
    'player_stats_tab': "buli_stats_player",
    'gk_stats_tab': "buli_stats_gk"
    }
supabase_tab_info = config_dict.ConfigDict(tab_info_dict)

# ##### Team Logo and Stadiums
config_teams_images = {
     "config_teams_logo":{
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
          "VfL Wolfsburg": "https://assets.bundesliga.com/tachyon/sites/2/2022/06/Wolfsburg-WOB.png"
        },
    "config_team_stadiums":{
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
         }}

# ##### Season Filter
season_filter_dict = {
     'season_filter':['Season', 'Form', 'Home', 'Away', '1st Half', '2nd Half', 'Win', 'Draw', 'Defeat']
     }
config_season_filter = config_dict.ConfigDict(season_filter_dict)

# ##### Match Day Stats
match_day_dict = {
     # ##### General Statistics
    'general_stats': ["Manager", "Lineup", "Distance Covered (Km)", "Sprints", "Possession", "% of Aerial Duel Won", "Offsides", 
                      "Corner Kicks", "Fouls Committed", "Fouls Drawn", "Yellow Cards", "Red Cards"],
    'general_emoji': ["👨‍💼", "📏", "🚄", "🏃‍", "⚽", "🤼‍", "🚫", "📐", "⛔", "🤒", "🟨", "🟥"],

    # ##### Offensive Statistics
    'offensive_stats': ["xGoal", 'xAssist', "Assists", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %", 
                        "Blocked Shots", "Take-Ons Attempted", "Successful Take-On %"],
    'offensive_emoji': ["⚽", "🔂", "🤝", "🔑", "👟", "🥅", "🎯", "⛔", "⛹️", "✅"],

    # ##### Defensive Statistics
    'defensive_stats': ["Tackles", "Tackles Won %", 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd', 
                        "Clearances", "Interceptions", "Ball Recoveries", "Blocks", "Errors"],
    'defensive_emoji': ["🤼", "✅", "⬇️", "↔️", "⬆️", "🆑", "🥷", "🤒", "⛔", "🚫️"],

    # ##### Passing Statistics
    'passing_stats': ["Touches", "Passes", "Passes Completion %", "Passes Short Completed %", "Passes Medium Completed %", "Passes Long Completed %", 
                      "Passes into Final 3rd", "Passes into Penalty Area", "Crosses", "Crosses into Penalty Area"],
    'passing_emoji': ["👟", "🔁", "✅", "⏏️", "⏫", "⏭️", "🥅", "❎", "↪️", "↗️"],

    # ##### Goalkeeper Statistics
    'gk_stats': ["Saves", "Saves %", "Post-Shot xGoal", "Gk Passes", "Goal Kicks", "Gk Throws", "Gk Crosses Faced", 
                 "Gk Crosses Stoped", "Gk Crosses Stoped %", 'Gk Sweeper Actions'],
    'gk_emoji': ["🧤", "✅", "⚽", "🔁", "👟", "🤾", "❎", "⛔", "🚫", "🏃‍♂️"]
    }
config_match_day = config_dict.ConfigDict(match_day_dict)

# ##### Match Day Statistics
match_day_stats_dict = {
    'stat_name':["General", "Offensive", "Defensive", "Passing", "Goalkeeper"],
    'stat_type': [config_match_day.general_stats, config_match_day.offensive_stats, config_match_day.defensive_stats, config_match_day.passing_stats, config_match_day.gk_stats],
    'stat_emoji': [config_match_day.general_emoji, config_match_day.offensive_emoji, config_match_day.defensive_emoji, config_match_day.passing_emoji, config_match_day.gk_emoji]
    }
config_match_day_stats = config_dict.ConfigDict(match_day_stats_dict)

# ##### Team Most Important Stats
importance_stats_dict = {
     'team_important_stats': ['xGoal', 'Possession', 'Distance Covered (Km)', 'Shots', 'Goals', 'Goals Ag']
     }
config_importance_stats = config_dict.ConfigDict(importance_stats_dict)

# ##### Team Stats
team_stats_dict = {
     # #### Main Stats
     'stats_team': ['Possession', 'Distance Covered (Km)', 'Sprints', 'Goals', 'Assists', 'Shots', 'Shots on Target', 'Shot Accuracy %', 'xGoal', 'xAssist', 
                    'Non-Penalty xG', 'xGoal Assist', 'Shot Creating Actions', 'Goal Creating Actions', 'Key Passes', 'Passes', 'Passes Completed', 
                    'Passes Completion %', 'Passes Short', 'Passes Short Completed', 'Passes Short Completed %', 'Passes Medium', 'Passes Medium Completed', 
                    'Passes Medium Completed %', 'Passes Long', 'Passes Long Completed', 'Passes Long Completed %', 'Passes into Final 3rd', 'Passes into Penalty Area', 
                    'Passing Distance', 'Progressive Passes', 'Progressive Passing Distance', 'Live Ball Passes', 'Dead Ball Passes', 'Passes from Free Kicks', 
                    'Through Balls', 'Switches', 'Passes Blocked', 'Crosses', 'Crosses into Penalty Area', 'Throw Ins', 'Corner Kicks', 'Inswinging Corner Kicks', 
                    'Outswinging Corner Kicks', 'Straight Corner Kicks', 'Touches', 'Touches Defensive Penalty Area', 'Touches Defensive 3rd', 'Touches Middle 3rd', 
                    'Touches Attacking 3rd', 'Touches Attacking Penalty Area', 'Touches Live Ball', 'Take-Ons Attempted', 'Successful Take-Ons', 'Successful Take-On %', 
                    'Tackled During Take-On', 'Tackled During Take-On %', 'Carries', 'Carrying Distance', 'Progressive Carries', 'Progressive Carrying Distance', 
                    'Carries into Final 3rd', 'Carries into Penalty Area', 'Miscontrols', 'Dispossessed', 'Passes Received', 'Progressive Passes Received', 'Tackles', 
                    'Tackles Won', 'Tackles Won %', 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd', 'Dribblers Tackled', 'Dribbles Challenged', 
                    '% of Dribblers Tackled', 'Challenges Lost', 'Blocks', 'Blocked Shots', 'Blocked Passes', 'Interceptions', 'Ball Recoveries', 'Clearances', 
                    'Errors', 'Aerial Duel Won', 'Aerial Duel Lost', '% of Aerial Duel Won', 'Yellow Cards', 'Red Cards', 'Second Yellow Card', 'Fouls Committed', 
                    'Fouls Drawn', 'Offsides', 'Penalty Kicks Made', 'Penalty Kicks Attempted', 'Penalty Kicks Conceded', 'Own Goals'],

    # ##### Aggregate Stats for Count Calculation
    'stats_count_calculations': ['Possession', 'Distance Covered (Km)', 'Sprints', 'Goals', 'Assists', 'Shots', 'Shots on Target', 'xGoal', 'xAssist', 'Non-Penalty xG', 
                                'xGoal Assist', 'Shot Creating Actions', 'Goal Creating Actions', 'Key Passes', 'Passes', 'Passes Completed', 'Passes Short', 
                                'Passes Short Completed', 'Passes Short Completed %', 'Passes Medium', 'Passes Medium Completed', 'Passes Long', 'Passes Long Completed', 
                                'Passes into Final 3rd', 'Passes into Penalty Area', 'Passing Distance', 'Progressive Passes', 'Progressive Passing Distance', 
                                'Live Ball Passes', 'Dead Ball Passes', 'Passes from Free Kicks', 'Through Balls', 'Switches', 'Passes Blocked', 'Crosses', 
                                'Crosses into Penalty Area', 'Throw Ins', 'Corner Kicks', 'Inswinging Corner Kicks', 'Outswinging Corner Kicks', 'Straight Corner Kicks', 
                                'Touches', 'Touches Defensive Penalty Area', 'Touches Defensive 3rd', 'Touches Middle 3rd', 'Touches Attacking 3rd', 
                                'Touches Attacking Penalty Area', 'Touches Live Ball', 'Take-Ons Attempted', 'Successful Take-Ons', 'Tackled During Take-On', 
                                'Tackled During Take-On %', 'Carries', 'Carrying Distance', 'Progressive Carries', 'Progressive Carrying Distance', 
                                'Carries into Final 3rd', 'Carries into Penalty Area', 'Miscontrols', 'Dispossessed', 'Passes Received', 'Progressive Passes Received', 
                                'Tackles', 'Tackles Won', 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd', 'Dribblers Tackled', 
                                'Dribbles Challenged', 'Challenges Lost', 'Blocks', 'Blocked Shots', 'Blocked Passes', 'Interceptions', 'Ball Recoveries', 'Clearances', 
                                'Errors', 'Aerial Duel Won', 'Aerial Duel Lost', 'Yellow Cards', 'Red Cards', 'Second Yellow Card', 'Fouls Committed', 'Fouls Drawn', 
                                'Offsides', 'Penalty Kicks Made', 'Penalty Kicks Attempted', 'Penalty Kicks Conceded', 'Own Goals'],

    # ##### Aggregate Stats for Percentage Calculation
    'stats_perc_calculations': {'Shot Accuracy %':['Shots', 'Shots on Target'], 'Passes Completion %':['Passes', 'Passes Completed'], 
                                'Passes Medium Completed %':['Passes Medium', 'Passes Medium Completed'], 
                                'Passes Long Completed %':['Passes Long', 'Passes Long Completed'], 'Tackles Won %':['Tackles', 'Tackles Won'], 
                                'Successful Take-On %':['Take-Ons Attempted', 'Successful Take-Ons'], 
                                '% of Dribblers Tackled':['Dribbles Challenged', 'Dribblers Tackled'], '% of Aerial Duel Won':['Aerial Duel', 'Aerial Duel Won']}
                                }
config_team_stats = config_dict.ConfigDict(team_stats_dict)

# ##### Player Stats
player_stats_dict = {
     # #### Main Stats
     'stats_player': ['Goals', 'Assists', 'Shots', 'Shots on Target', 'Shot Accuracy %', 'xGoal', 'xAssist', 
                    'Non-Penalty xG', 'xGoal Assist', 'Shot Creating Actions', 'Goal Creating Actions', 'Key Passes', 'Passes', 'Passes Completed', 
                    'Passes Completion %', 'Passes Short', 'Passes Short Completed', 'Passes Short Completed %', 'Passes Medium', 'Passes Medium Completed', 
                    'Passes Medium Completed %', 'Passes Long', 'Passes Long Completed', 'Passes Long Completed %', 'Passes into Final 3rd', 'Passes into Penalty Area', 
                    'Passing Distance', 'Progressive Passes', 'Progressive Passing Distance', 'Live Ball Passes', 'Dead Ball Passes', 'Passes from Free Kicks', 
                    'Through Balls', 'Switches', 'Passes Blocked', 'Crosses', 'Crosses into Penalty Area', 'Throw Ins', 'Corner Kicks', 'Inswinging Corner Kicks', 
                    'Outswinging Corner Kicks', 'Straight Corner Kicks', 'Touches', 'Touches Defensive Penalty Area', 'Touches Defensive 3rd', 'Touches Middle 3rd', 
                    'Touches Attacking 3rd', 'Touches Attacking Penalty Area', 'Touches Live Ball', 'Take-Ons Attempted', 'Successful Take-Ons', 'Successful Take-On %', 
                    'Tackled During Take-On', 'Tackled During Take-On %', 'Carries', 'Carrying Distance', 'Progressive Carries', 'Progressive Carrying Distance', 
                    'Carries into Final 3rd', 'Carries into Penalty Area', 'Miscontrols', 'Dispossessed', 'Passes Received', 'Progressive Passes Received', 'Tackles', 
                    'Tackles Won', 'Tackles Won %', 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd', 'Dribblers Tackled', 'Dribbles Challenged', 
                    '% of Dribblers Tackled', 'Challenges Lost', 'Blocks', 'Blocked Shots', 'Blocked Passes', 'Interceptions', 'Ball Recoveries', 'Clearances', 
                    'Errors', 'Aerial Duel Won', 'Aerial Duel Lost', '% of Aerial Duel Won', 'Yellow Cards', 'Red Cards', 'Second Yellow Card', 'Fouls Committed', 
                    'Fouls Drawn', 'Offsides', 'Penalty Kicks Made', 'Penalty Kicks Attempted', 'Penalty Kicks Conceded', 'Own Goals'],

    # ##### Aggregate Stats for Count Calculation
    'stats_count_calculations': ['Goals', 'Assists', 'Shots', 'Shots on Target', 'xGoal', 'xAssist', 'Non-Penalty xG', 
                                'xGoal Assist', 'Shot Creating Actions', 'Goal Creating Actions', 'Key Passes', 'Passes', 'Passes Completed', 'Passes Short', 
                                'Passes Short Completed', 'Passes Short Completed %', 'Passes Medium', 'Passes Medium Completed', 'Passes Long', 'Passes Long Completed', 
                                'Passes into Final 3rd', 'Passes into Penalty Area', 'Passing Distance', 'Progressive Passes', 'Progressive Passing Distance', 
                                'Live Ball Passes', 'Dead Ball Passes', 'Passes from Free Kicks', 'Through Balls', 'Switches', 'Passes Blocked', 'Crosses', 
                                'Crosses into Penalty Area', 'Throw Ins', 'Corner Kicks', 'Inswinging Corner Kicks', 'Outswinging Corner Kicks', 'Straight Corner Kicks', 
                                'Touches', 'Touches Defensive Penalty Area', 'Touches Defensive 3rd', 'Touches Middle 3rd', 'Touches Attacking 3rd', 
                                'Touches Attacking Penalty Area', 'Touches Live Ball', 'Take-Ons Attempted', 'Successful Take-Ons', 'Tackled During Take-On', 
                                'Tackled During Take-On %', 'Carries', 'Carrying Distance', 'Progressive Carries', 'Progressive Carrying Distance', 
                                'Carries into Final 3rd', 'Carries into Penalty Area', 'Miscontrols', 'Dispossessed', 'Passes Received', 'Progressive Passes Received', 
                                'Tackles', 'Tackles Won', 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd', 'Dribblers Tackled', 
                                'Dribbles Challenged', 'Challenges Lost', 'Blocks', 'Blocked Shots', 'Blocked Passes', 'Interceptions', 'Ball Recoveries', 'Clearances', 
                                'Errors', 'Aerial Duel Won', 'Aerial Duel Lost', 'Yellow Cards', 'Red Cards', 'Second Yellow Card', 'Fouls Committed', 'Fouls Drawn', 
                                'Offsides', 'Penalty Kicks Made', 'Penalty Kicks Attempted', 'Penalty Kicks Conceded', 'Own Goals'],

    # ##### Aggregate Stats for Percentage Calculation
    'stats_perc_calculations': {'Shot Accuracy %':['Shots', 'Shots on Target'], 'Passes Completion %':['Passes', 'Passes Completed'], 
                                'Passes Medium Completed %':['Passes Medium', 'Passes Medium Completed'], 
                                'Passes Long Completed %':['Passes Long', 'Passes Long Completed'], 'Tackles Won %':['Tackles', 'Tackles Won'], 
                                'Successful Take-On %':['Take-Ons Attempted', 'Successful Take-Ons'], 
                                '% of Dribblers Tackled':['Dribbles Challenged', 'Dribblers Tackled'], '% of Aerial Duel Won':['Aerial Duel', 'Aerial Duel Won']}
                                }
config_player_stats = config_dict.ConfigDict(player_stats_dict)

# ##### Gk Stats
gk_stats_dict = {
     # #### Main Stats
     'stats_gk': ["Saves", "Saves %", "Gk Shots on Target Against", "Gk Goals Against", "Post-Shot xGoal", "Launched Passes", "Launched Passes Completed", 
                  "Launched Passes Completed %", "Gk Passes", "Gk Throws", "Gk Average Pass Length", "Goal Kicks", "Goal Kicks Launch %", 
                  "Goal Kicks Average Length", "Gk Crosses Faced", "Gk Crosses Stoped", "Gk Crosses Stoped %", "Gk Sweeper Actions", 
                  "Gk Sweeper Average Distance"],

    # ##### Aggregate Stats for Count Calculation
    'stats_count_calculations': ["Saves", "Gk Shots on Target Against", "Gk Goals Against", "Post-Shot xGoal", "Launched Passes", "Launched Passes Completed", 
                  "Gk Passes", "Gk Throws", "Gk Average Pass Length", "Goal Kicks", "Goal Kicks Launch %", "Goal Kicks Average Length", "Gk Crosses Faced", 
                  "Gk Crosses Stoped", "Gk Sweeper Actions", "Gk Sweeper Average Distance"],

    # ##### Aggregate Stats for Percentage Calculation
    'stats_perc_calculations': {"Saves %":["Gk Shots on Target Against", "Saves"], "Launched Passes Completed %":["Launched Passes", "Launched Passes Completed"], 
                                "Gk Crosses Stoped %":["Gk Crosses Faced", "Gk Crosses Stoped"]}}
config_gk_stats = config_dict.ConfigDict(gk_stats_dict)


# ##### Previous Season for Each Current Season
previous_seasons_dict = {
     'season_comparison': {'2018-2019':'2017-2018',
                           '2019-2020':'2018-2019', 
                           '2020-2021':'2019-2020', 
                           '2021-2022':'2020-2021', 
                           '2022-2023':'2021-2022', 
                           '2023-2024':'2022-2023'},
    'season_id':{'2018-2019':1,
                 '2019-2020':2, 
                 '2020-2021':3,
                 '2021-2022':4, 
                 '2022-2023':5,
                 '2023-2024':6}}
config_previous_seasons = config_dict.ConfigDict(previous_seasons_dict)

# ##### Comparison Statistics
comparison_stats_dict = {
     # #### Team Comparison Stats
     'team_stats_name': ["General", "Offensive", "Defensive", "Passing"],
     'team_stats_list': {
                    "General": ["Distance Covered (Km)", "Sprints", "Possession", "% of Aerial Duel Won", "Offsides", 
                                "Corner Kicks", "Fouls Committed", "Fouls Drawn", "Yellow Cards", "Red Cards"],
                    "Offensive": ["xGoal", 'xAssist', "Assists", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %", 
                                  "Blocked Shots", "Take-Ons Attempted", "Successful Take-On %"],
                    "Defensive": ["Tackles", "Tackles Won %", 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd',
                                  "Clearances", "Interceptions", "Ball Recoveries", "Blocks", "Errors"],
                    "Passing": ["Touches", "Passes", "Passes Completion %", "Passes Short Completed %", "Passes Medium Completed %", "Passes Long Completed %", 
                                "Passes into Final 3rd", "Passes into Penalty Area", "Crosses", "Crosses into Penalty Area"]},
     # #### Player Comparison Stats
     'player_stats_name': ["Offensive", "Defensive", "Passing"],
     'player_stats_list': {
                    "Offensive": ["xGoal", 'xAssist', "Assists", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %", 
                                  "Blocked Shots", "Take-Ons Attempted", "Successful Take-On %", "% of Aerial Duel Won", "Offsides"],
                    "Defensive": ["Tackles", "Tackles Won %", 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd',
                                  "Clearances", "Interceptions", "Ball Recoveries", "Blocks", "Errors", "Fouls Committed", "Fouls Drawn", 
                                  "Yellow Cards"],
                    "Passing": ["Touches", "Passes", "Passes Completion %", "Passes Short Completed %", "Passes Medium Completed %", "Passes Long Completed %", 
                                "Passes into Final 3rd", "Passes into Penalty Area", "Corner Kicks", "Crosses", "Crosses into Penalty Area"]},
        'gk_stats':["Saves", "Saves %", "Post-Shot xGoal", "Gk Passes", "Goal Kicks", "Gk Throws", "Gk Crosses Faced", "Gk Crosses Stoped", 
                    "Gk Crosses Stoped %", "Gk Sweeper Actions"]}
config_comparison_stats = config_dict.ConfigDict(comparison_stats_dict)

# ##### Process Bundesliga Team and Gk Data
st.cache_data
def process_team_data(data:pd.DataFrame, 
                      data_gk:pd.DataFrame) -> pd.DataFrame:
    # ##### Read Data
    buli_df = data.copy()
    buli_gk_df = data_gk.copy()

    # ##### Change Name Statistics
    buli_df['Team_Lineup'] = buli_df['Team_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df['Opp_Lineup'] = buli_df['Opp_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df.rename(columns={"Team_Lineup": "Lineup"}, inplace=True)

    # ##### Aggregate Goalkeeper Statistics
    df_team_gk = \
        buli_gk_df.groupby(["Season", "Week_No", "Team", "Opponent", "Venue"])[['Gk Shots on Target Against', 'Saves', 'Post-Shot xGoal', 'Launched Passes', 
                                                                                'Launched Passes Completed', 'Gk Passes', 'Gk Throws', 'Goal Kicks', 'Gk Crosses Faced', 
                                                                                'Gk Crosses Stoped',  'Gk Sweeper Actions']].sum()
    
    df_team_gk.reset_index(inplace=True)
    df_team_gk['Saves %'] = np.round(df_team_gk['Saves'] / df_team_gk['Gk Shots on Target Against'] * 100, 2)
    df_team_gk['Launched Passes Completed %'] = np.round(df_team_gk['Launched Passes Completed'] / df_team_gk['Launched Passes'] * 100, 2)
    df_team_gk['Gk Crosses Stoped %'] = np.round(df_team_gk['Gk Crosses Stoped'] /(df_team_gk['Gk Crosses Faced'] + df_team_gk['Gk Crosses Stoped']) * 100, 2)

    # ##### Create Final Bundesliga data
    final_buli_df = pd.merge(left=buli_df, 
                             right=df_team_gk, 
                             left_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'],
                             right_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'])
    final_buli_df = final_buli_df.reset_index(drop=True)

    return final_buli_df

# ##### Create Goals Against
def process_goals_opponent(data:pd.DataFrame) -> pd.DataFrame:

    # ##### Goals Agains Statistics
    buli_df = data.copy()
    home_df = buli_df[buli_df['Venue'] == 'Home'].copy()
    home_df.reset_index(drop=True, inplace=True)
    away_df = buli_df[buli_df['Venue'] == 'Away'].copy()
    away_df.reset_index(drop=True, inplace=True)
    home_df['Goals Ag'] = away_df['Goals']
    away_df['Goals Ag'] = home_df['Goals']
    final_buli_df = pd.concat([home_df, away_df])
    final_buli_df = final_buli_df.sort_values(by=['Id'])
    final_buli_df.reset_index(drop=True, inplace=True)

    return final_buli_df


# ##### Process Season Bundesliga Data
st.cache_data
def filter_season_data(data:pd.DataFrame) -> pd.DataFrame:
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

# ##### Create Season Bundesliga Table
def buli_table_data(data:pd.DataFrame, 
                    table_type:str) -> pd.DataFrame:
    # ##### Season Data
    buli_season = data[data[table_type] == 1].reset_index(drop=True)

    # ##### Create Tabel Stats
    buli_tab = buli_season.groupby(['Team'])[['Season', 'Win', 'Draw', 'Defeat', 'Goals', 'Goals Ag']].sum()
    buli_tab['Goal_Diff'] = buli_tab['Goals'] - buli_tab['Goals Ag']
    buli_tab['Points'] = buli_tab['Win'] * 3 + buli_tab['Draw']
    buli_tab.sort_values(by=['Points', 'Goal_Diff'], ascending=[False, False], inplace=True)
    buli_tab.reset_index(inplace=True)
    buli_tab['Rank'] = [i for i in range(1, len(buli_tab) + 1)]
    buli_tab.set_index('Rank', inplace=True)
    buli_tab.columns = ["Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]

    return buli_tab

# ##### Metrics Cars Style
def style_metric_cards(background_color: str = "#e5e5e6", 
                       border_radius_px: int = 15, 
                       border_top_color: str = "#d20614", 
                       border_left_color: str = "#d20614", 
                       border_right_color: str = "#ffffff", 
                       border_bottom_color: str = "#ffffff", 
                       box_shadow: bool = True) -> st:

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

# ##### Radar Mosaic
def radar_mosaic(radar_height:float=0.500, title_height:int=0, figheight:int=2):
    endnote_height = 1 - title_height - radar_height
    figwidth = figheight * radar_height
    figure, axes = plt.subplot_mosaic([['title'], ['radar'], ['endnote']],
                                      gridspec_kw={'height_ratios': [title_height, radar_height, endnote_height],
                                                   'bottom': 0, 
                                                   'left': 0, 
                                                   'top': 1,
                                                   'right': 1, 
                                                   'hspace': 0},
                                      figsize=(figwidth, figheight))
    axes['title'].axis('off')
    axes['endnote'].axis('off')

    return figure, axes

# ##### Radar Plot
def radar_plot(stats:list,
               comparison_stats:list,
               min_stats:list,
               max_stats:list,
               radar_name:bool=False,
               player_name:str='') -> plt:
    
    # ##### Default Radar
    radar = Radar(comparison_stats, 
                  min_stats, 
                  max_stats,
              round_int=[False]*len(comparison_stats),
              num_rings=7,
              ring_width=1, center_circle_radius=1)

    # ##### Create Radar Plot
    radar_fig, axs = grid(figheight=15, grid_height=0.5, title_height=0.01, endnote_height=0.01,
                    title_space=0, endnote_space=0, grid_key='radar', axis=False)

    radar.setup_axis(ax=axs['radar'], facecolor='None')
    radar.draw_circles(ax=axs['radar'], facecolor='#e5e5e6', edgecolor='#ffffff')
    radar_output = radar.draw_radar(stats, ax=axs['radar'],
                                    kwargs_radar={'facecolor': '#d20614', 'alpha': 0.25},
                                    kwargs_rings={'facecolor': '#ffffff', 'alpha': 0.25})

    _, _, vertices = radar_output
    radar.draw_range_labels(ax=axs['radar'], fontsize=10, color='#000000', font="Sans serif")
    radar.draw_param_labels(ax=axs['radar'], fontsize=12.5, color='#000000', font="Sans serif")
    axs['radar'].scatter(vertices[:, 0], vertices[:, 1],  c='#d20614', edgecolors='#000000', marker='o', s=100)

    if radar_name:
         axs['title'].text(0.5, 1, player_name, fontsize=15, color='#d20614', ha='center', va='center')
    
    return radar_fig
