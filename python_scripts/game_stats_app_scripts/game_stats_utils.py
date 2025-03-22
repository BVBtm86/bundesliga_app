import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.stats import ttest_ind
from ml_collections import config_dict
from mplsoccer import Radar, grid, Bumpy

# #################################################################################################### Game Stats Configuration
class GameStatsConfiguration:
     
    def __init__(self) -> None:
        st.cache_resource()

        # ########## Supabase Tables
        self.tab_info_dict = {
            "info_tab": "buli_seasons_info",
            "team_stats_tab": "buli_stats_team",
            "team_tracking_tab": "buli_tracking_team",
            "player_stats_tab": "buli_stats_player",
            "gk_stats_tab": "buli_stats_gk"
            }
        
        # ##### Team Logo and Stadiums
        self.teams_info_dict = {
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
                "VfL Wolfsburg": ["https://assets.bundesliga.com/stadium/icon/DFL-STA-000003_B.png?fit=64,64", "Volkswagen Arena"]}
                }
        
        # ###### Season Info
        self.seasons_info_dict = {
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
                        '2023-2024':6}
                        }
        
        # ##### Season Filter
        self.season_filter_dict = {
            'season_filter':['Season', 'Form', 'Home', 'Away', '1st Half', '2nd Half', 'Win', 'Draw', 'Defeat']
            }
        
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
        
        self.match_day_stats_dict = {
            'stat_name':["General", "Offensive", "Defensive", "Passing", "Goalkeeper"],
            'stat_type': [match_day_dict["general_stats"], match_day_dict["offensive_stats"], 
                          match_day_dict["defensive_stats"], match_day_dict["passing_stats"], match_day_dict["gk_stats"]],
            'stat_emoji': [match_day_dict["general_emoji"], match_day_dict["offensive_emoji"], 
                           match_day_dict["defensive_emoji"], match_day_dict["passing_emoji"], match_day_dict["gk_emoji"]]
            }
        
        # ##### Team Most Important Stats
        self.importance_stats_dict = {
            'team_important_stats': ['xGoal', 'Possession', 'Distance Covered (Km)', 'Shots', 'Goals', 'Goals Ag']
            }

        # ##### Team Stats
        self.team_stats_dict = {
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
        
        # ##### Player Stats
        self.player_stats_dict = {
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
        
        # ##### Gk Stats
        self.gk_stats_dict = {
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
                                        "Gk Crosses Stoped %":["Gk Crosses Faced", "Gk Crosses Stoped"]}
                                        }

        # ##### Comparison Stats
        self.comparison_stats_dict = {
            # #### Team Comparison Stats
            'team_stats_name': ["General", "Offensive", "Defensive", "Passing"],
            'team_stats_list': {
                            "General": ["Distance Covered (Km)", "Sprints", "Possession", "% of Aerial Duel Won", "Offsides", 
                                        "Corner Kicks", "Fouls Committed", "Fouls Drawn", "Yellow Cards", "Red Cards"],
                            "Offensive": ["xGoal", 'xAssist', "Assists", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %", 
                                        "Blocked Shots", "Take-Ons Attempted", "Successful Take-On %"],
                            "Defensive": ["Tackles", "Tackles Won %", 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd',
                                        "Clearances", "Interceptions", "Ball Recoveries", "Blocks", "Errors"],
                            "Passing": ["Touches", "Passes", "Passes Completion %", "Passes Short Completed %", "Passes Medium Completed %", 
                                        "Passes Long Completed %", "Passes into Final 3rd", "Passes into Penalty Area", "Crosses", "Crosses into Penalty Area"]},

            # #### Player Comparison Stats
            'player_stats_name': ["Offensive", "Defensive", "Passing"],
            'player_stats_list': {
                            "Offensive": ["xGoal", 'xAssist', "Assists", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %", 
                                        "Blocked Shots", "Take-Ons Attempted", "Successful Take-On %", "% of Aerial Duel Won", "Offsides"],
                            "Defensive": ["Tackles", "Tackles Won %", 'Tackles Defensive 3rd', 'Tackles Middle 3rd', 'Tackles Attacking 3rd',
                                        "Clearances", "Interceptions", "Ball Recoveries", "Blocks", "Errors", "Fouls Committed", "Fouls Drawn", 
                                        "Yellow Cards"],
                            "Passing": ["Touches", "Passes", "Passes Completion %", "Passes Short Completed %", "Passes Medium Completed %", 
                                        "Passes Long Completed %", "Passes into Final 3rd", "Passes into Penalty Area", "Corner Kicks", "Crosses", 
                                        "Crosses into Penalty Area"]},

            # #### Gk Comparison Stats
            'gk_stats':["Saves", "Saves %", "Post-Shot xGoal", "Gk Passes", "Goal Kicks", "Gk Throws", "Gk Crosses Faced", "Gk Crosses Stoped", 
                        "Gk Crosses Stoped %", "Gk Sweeper Actions"]
                        }

    # ##### Supabase Table Info
    def get_tab_info(self) -> config_dict:
         return config_dict.ConfigDict(self.tab_info_dict)
    
    # ##### Teams Images
    def get_teams_info(self) -> dict:
         return self.teams_info_dict
    
    # ##### Season Info
    def get_season_info(self) -> config_dict:
         return config_dict.ConfigDict(self.seasons_info_dict)
    
    # ##### Season Filters
    def get_season_filter(self) -> config_dict:
         return config_dict.ConfigDict(self.season_filter_dict)

    # ##### Match Day Stats
    def get_match_day_stats(self) -> config_dict:
         return config_dict.ConfigDict(self.match_day_stats_dict)
    
    # ##### Importance Stats
    def get_importance_stats(self) -> config_dict:
         return config_dict.ConfigDict(self.importance_stats_dict)
    
    # ##### Team Stats
    def get_team_stats(self) -> config_dict:
         return config_dict.ConfigDict(self.team_stats_dict)
    
    # ##### Importance Stats
    def get_player_stats(self) -> config_dict:
         return config_dict.ConfigDict(self.player_stats_dict)
    
    # ##### Gk Stats
    def get_gk_stats(self) -> config_dict:
         return config_dict.ConfigDict(self.gk_stats_dict)
    
    # ##### Comparison Stats
    def get_comparison_stats(self) -> config_dict:
         return config_dict.ConfigDict(self.comparison_stats_dict)

# #################################################################################################### Game Stats Data Processing
class GameStatsProcessing:
     
    def __init__(self) -> None:
        
        self.groupby_stats = ["Season", "Week No", "Team", "Opponent", "Venue"]
        self.agg_gk_stats = ['Gk Shots on Target Against', 'Saves', 'Post-Shot xGoal', 'Launched Passes', 'Launched Passes Completed', 'Gk Passes', 
                             'Gk Throws', 'Goal Kicks', 'Gk Crosses Faced', 'Gk Crosses Stoped', 'Gk Sweeper Actions']
        self.merge_stats = ['Season', 'Week No', 'Team', 'Opponent', 'Venue']
        self.table_group = ['Season', 'Win', 'Draw', 'Defeat', 'Goals', 'Goals Ag']
        self.table_stats = ["Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]

    # ##### Process Bundesliga Team and Gk Data
    st.cache_data
    def process_team_data(self, 
                          data:pd.DataFrame, 
                          data_gk:pd.DataFrame) -> pd.DataFrame:
        
        # ##### Read Data
        buli_df = data.copy()
        buli_gk_df = data_gk.copy()

        # ##### Change Name Statistics
        buli_df['Team Lineup'] = buli_df['Team Lineup'].apply(lambda x: x.replace("◆", ""))
        buli_df['Opp Lineup'] = buli_df['Opp Lineup'].apply(lambda x: x.replace("◆", ""))
        buli_df.rename(columns={"Team Lineup": "Lineup"}, inplace=True)

        # ##### Aggregate Goalkeeper Statistics
        df_team_gk = \
            buli_gk_df.groupby(self.groupby_stats)[self.agg_gk_stats].sum()
        
        df_team_gk.reset_index(inplace=True)
        df_team_gk['Saves %'] = np.round(df_team_gk['Saves'] / df_team_gk['Gk Shots on Target Against'] * 100, 2)
        df_team_gk['Launched Passes Completed %'] = np.round(df_team_gk['Launched Passes Completed'] / df_team_gk['Launched Passes'] * 100, 2)
        df_team_gk['Gk Crosses Stoped %'] = np.round(df_team_gk['Gk Crosses Stoped'] /(df_team_gk['Gk Crosses Faced'] + df_team_gk['Gk Crosses Stoped']) * 100, 2)

        # ##### Create Final Bundesliga data
        final_buli_df = pd.merge(left=buli_df, 
                                right=df_team_gk, 
                                left_on=self.merge_stats,
                                right_on=self.merge_stats)
        final_buli_df = final_buli_df.reset_index(drop=True)

        return final_buli_df

    # ##### Create Goals Against
    def process_goals_opponent(self,
                               data:pd.DataFrame) -> pd.DataFrame:

        # ##### Goals Agains Statistics
        buli_df = data.copy()
        home_df = buli_df[buli_df['Venue'] == 'Home'].copy()
        home_df.reset_index(drop=True, inplace=True)
        away_df = buli_df[buli_df['Venue'] == 'Away'].copy()
        away_df.reset_index(drop=True, inplace=True)
        home_df['Goals Ag'] = away_df['Goals']
        away_df['Goals Ag'] = home_df['Goals']
        final_buli_df = pd.concat([home_df, away_df])
        final_buli_df = final_buli_df.sort_values(by=['id'])
        final_buli_df.reset_index(drop=True, inplace=True)

        return final_buli_df

    # ##### Process Season Bundesliga Data
    st.cache_data
    def filter_season_data(self,
                           data:pd.DataFrame) -> pd.DataFrame:
        buli_df = data.copy()

        # ##### Creating Tabel Stats Filter
        buli_df['Win'] = np.where(buli_df['Result'] == 'Win', 1, 0)
        buli_df['Draw'] = np.where(buli_df['Result'] == 'Draw', 1, 0)
        buli_df['Defeat'] = np.where(buli_df['Result'] == 'Defeat', 1, 0)
        buli_df['Season'] = 1
        buli_df['Home'] = np.where(buli_df['Venue'] == "Home", 1, 0)
        buli_df['Away'] = np.where(buli_df['Venue'] == "Away", 1, 0)
        buli_df["1st Half"] = np.where(buli_df["Week No"] <= 17, 1, 0)
        buli_df["2nd Half"] = np.where(buli_df["Week No"] >= 18, 1, 0)
        form_games = list(buli_df["Week No"].unique())[-5:]
        buli_df["Form"] = np.where(buli_df["Week No"].isin(form_games),1, 0)

        return buli_df

    # ##### Create Season Bundesliga Table
    def buli_table_data(self,
                        data:pd.DataFrame, 
                        table_type:str) -> pd.DataFrame:
        # ##### Season Data
        buli_season = data[data[table_type] == 1].reset_index(drop=True)

        # ##### Create Tabel Stats
        buli_tab = buli_season.groupby(['Team'])[self.table_group].sum()
        buli_tab['Goal_Diff'] = buli_tab['Goals'] - buli_tab['Goals Ag']
        buli_tab['Points'] = buli_tab['Win'] * 3 + buli_tab['Draw']
        buli_tab.sort_values(by=['Points', 'Goal_Diff'], ascending=[False, False], inplace=True)
        buli_tab.reset_index(inplace=True)
        buli_tab['Rank'] = [i for i in range(1, len(buli_tab) + 1)]
        buli_tab.set_index('Rank', inplace=True)
        buli_tab.columns = self.table_stats

        return buli_tab

# #################################################################################################### Game Stats Style
class GameStatsStyle:

    def __init__(self) -> None:
        # ##### Style Metrics
        self.background_color="#e5e5e6"
        self.border_radius_px=15
        self.border_top_color="#d20614"
        self.border_left_color="#d20614"
        self.border_right_color="#ffffff"
        self.border_bottom_color="#ffffff"
        self.box_shadow=True

        # ##### Radar Parameters
        self.radar_height=0.500, 
        self.title_height=0
        self.figheight=2
         
         
    # ##### Metrics Card Style
    def style_metric_cards(self) -> st:

            box_shadow_str = ("box-shadow: 0 0 1rem 0 #e5e5e6 !important;" if self.box_shadow 
                                else "box-shadow: none !important;")
            st.markdown(
                f"""
                <style>
                    div[data-testid="metric-container"] {{
                        background-color: {self.background_color};
                        padding: 5% 5% 5% 5%;
                        border-radius: {self.border_radius_px}px;
                        border-top: 0.2rem solid {self.border_top_color} !important;
                        border-left: 0.2rem solid {self.border_left_color} !important;
                        border-bottom: 0.2rem solid {self.border_bottom_color} !important;
                        border-right: 0.2rem solid {self.border_right_color} !important;
                        {box_shadow_str}
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )

    # ##### Radar Mosaic
    def radar_mosaic(self):
        endnote_height = 1 - self.title_height - self.radar_height
        figwidth = self.figheight * self.radar_height
        figure, axes = plt.subplot_mosaic([['title'], ['radar'], ['endnote']],
                                        gridspec_kw={'height_ratios': [self.title_height, self.radar_height, endnote_height],
                                                    'bottom': 0, 
                                                    'left': 0, 
                                                    'top': 1,
                                                    'right': 1, 
                                                    'hspace': 0},
                                        figsize=(figwidth, self.figheight))
        axes['title'].axis('off')
        axes['endnote'].axis('off')

        return figure, axes

    # ##### Radar Plot
    def radar_plot(self,
                   stats:list,
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
                      ring_width=1, 
                      center_circle_radius=1)

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

# #################################################################################################### Game Stats Analysis
class GameDayStats:

    def __init__(self) -> None:
        self.perc_stats = ["Possession", "% of Aerial Duel Won", "Shot Accuracy %", "Tackles Won %", "Saves %", "Gk Crosses Stoped %", 
                           "Passes Completion %", "Passes Short Completed %", "Passes Medium Completed %", "Passes Long Completed %", "Successful Take-On %"]
        self.count_stats = ["Distance Covered (Km)", "xGoal", "xAssist", "Post-Shot xGoal"]
        self.info_stats = ['Manager', 'Lineup']
        self.teams_info = GameStatsConfiguration().get_teams_info()
        self.stats_game = GameStatsConfiguration().get_match_day_stats()

    # ##### Process Match Day Stats Incons
    def stat_name_icon(self,
                       stats:str) -> list:

        # ##### Return Match Day Stats Icons
        match_day_name_icon = []
        for i in range(len(stats)):
            match_day_name_icon.append(st.markdown(f'<p>{stats[i]}</p>', unsafe_allow_html=True))
        return match_day_name_icon


    # ##### Match Day Stats
    def game_stats(self,
                   data:pd.DataFrame,
                   home_team:str,
                   away_team:str,
                   stats:list,
                   venue:str) -> list:

        if venue == "Home":
            day_stats = data[(data['Team'] == home_team) & (data['Opponent'] == away_team) &
                            (data['Venue'] == venue)][stats].values[0]
        else:
            day_stats = data[(data['Opponent'] == home_team) & (data['Team'] == away_team) &
                            (data['Venue'] == venue)][stats].values[0]

        game_stats = []
        for i in range(len(day_stats)):
            if stats[i] in self.perc_stats:
                game_stats.append(st.markdown(f"<p style='text-align: center;'p>{day_stats[i] / 100:.1%}", unsafe_allow_html=True))
            elif stats[i] in self.count_stats:
                game_stats.append(st.markdown(f"<p style='text-align: center;'p>{day_stats[i]:.1f}", unsafe_allow_html=True))
            elif stats[i] in self.info_stats:
                st.markdown(f"<p style='text-align: center;'p>{day_stats[i]}", unsafe_allow_html=True)
            else:
                game_stats.append(st.markdown(f"<p style='text-align: center;'p>{day_stats[i]:.0f}", unsafe_allow_html=True))

        return game_stats

class TeamStatsAnalysis:

    def __init__(self) -> None:
        self.season_info = GameStatsConfiguration().get_season_info()
        self.season_filter = GameStatsConfiguration().get_season_filter()
        self.team_stats = GameStatsConfiguration().get_team_stats()
        self.importance_stats = GameStatsConfiguration().get_importance_stats()
        self.teams_info = GameStatsConfiguration().get_teams_info()
        self.comparison_stats = GameStatsConfiguration().get_comparison_stats()
        self.game_stats_style = GameStatsStyle()

    # ##### Important Stats
    def most_important_stats(self,
                             data:pd.DataFrame, 
                             data_all:pd.DataFrame, 
                             current_season:str, 
                             previous_seasons:dict, 
                             team:str) -> tuple[list, 
                                                list]:

        season_data = data.copy()
        # ##### Current Season Avg Stats
        season_important_stats = list(season_data[season_data['Team'] == team][self.importance_stats.team_important_stats[:4]].mean().round(2).values)

        # ##### Current Season Sum Stats
        season_data['Win'] = np.where(season_data['Result'] == 'Win', 1, 0)
        season_data['Draw'] = np.where(season_data['Result'] == 'Draw', 1, 0)
        season_important_stats.append((season_data[season_data['Team'] == team]['Win'] * 3 + season_data[season_data['Team'] == team]['Draw']).sum())
        season_important_stats.append(season_data[season_data['Team'] == team][self.importance_stats.team_important_stats[4]].sum())
        season_important_stats.append(season_data[season_data['Team'] == team][self.importance_stats.team_important_stats[5]].sum())
        current_season_match_day = season_data['Week No'].max()

        # ##### Last Season Stats
        season_previous = previous_seasons[current_season]
        previous_data_season = data_all[(data_all['Season Id'] == season_previous) & (data_all['Week No'] <= current_season_match_day)].reset_index(drop=True)
        if previous_data_season.shape[0] > 0:
            previous_season_important_stats = list(previous_data_season[previous_data_season['Team'] == team][self.importance_stats.team_important_stats[:4]].mean().round(2).values)
            previous_data_season['Win'] = np.where(previous_data_season['Result'] == 'Win', 1, 0)
            previous_data_season['Draw'] = np.where(previous_data_season['Result'] == 'Draw', 1, 0)
            previous_season_important_stats.append((previous_data_season[previous_data_season['Team'] == team]['Win'] * 3 + previous_data_season[previous_data_season['Team'] == team]['Draw']).sum())
            previous_season_important_stats.append(previous_data_season[previous_data_season['Team'] == team][self.importance_stats.team_important_stats[4]].sum())
            previous_season_important_stats.append(previous_data_season[previous_data_season['Team'] == team][self.importance_stats.team_important_stats[5]].sum())
            diff_important_stats = list(pd.Series(season_important_stats) - pd.Series(previous_season_important_stats))
            diff_important_stats[:4] = np.round(diff_important_stats[:4],2)
        else:
            diff_important_stats = ["", "", "", "", "", "", ""]

        return season_important_stats, diff_important_stats

    # ##### Match Day Analysis
    def teams_day_analysis(self,
                           data:pd.DataFrame,
                           team:str, 
                           stat_name:str) -> tuple[px.bar, 
                                                   float,
                                                   float,
                                                   float,
                                                   str]:
        
        # ##### Create Aerial Duel Total Stat
        df_match_day = data.copy()
        df_match_day['Aerial Duel'] = df_match_day['Aerial Duel Won'] + df_match_day['Aerial Duel Lost']

        # ##### Filter Season Data by Selected Team
        df_team = df_match_day[(df_match_day['Team'] == team)].reset_index(drop=True)
        df_opp = df_match_day[(df_match_day['Opponent'] == team)].reset_index(drop=True)

        # ##### Create Team Chart
        df_team['TEAM'] = df_team['Team']
        df_opp['TEAM'] = "Opponent"
        df_team['Game'] = df_team['Week No']
        df_opp['Game'] = df_opp['Week No']
        plot_data = pd.concat([df_team, df_opp])
        min_value = np.min(plot_data[stat_name]) * 0.8
        if min_value < 10:
            min_value = 0
        max_value = np.max(plot_data[stat_name]) * 1.1
        if plot_data[stat_name].sum() > 0:
            match_day_fig = px.bar(plot_data, 
                                x="Game", 
                                y=stat_name, 
                                color="Result", 
                                facet_col="TEAM", 
                                color_discrete_map={
                                    'Win': "rgb(200,11,1)",
                                    'Draw': "rgb(179, 179, 179)",
                                    'Defeat': "rgb(78,78,80)"},
                                    text=stat_name,
                                    hover_name='Team')
            match_day_fig.update_layout({
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
            },
                xaxis1=dict(
                    tickmode='array',
                    tickvals=[i for i in range(1, len(df_team) + 1)],
                    ticktext=plot_data['Game'].unique(),
                ),
                xaxis2=dict(
                    tickmode='array',
                    tickvals=[i for i in range(1, len(df_opp) + 1)],
                    ticktext=plot_data['Game'].unique(),
                ),
                yaxis_range=[min_value, max_value]
            )

            # #### Insight Statistics
            if stat_name in self.team_stats.stats_perc_calculations.keys():
                stats_agg = self.team_stats.stats_perc_calculations[stat_name]
                avg_team_calc = pd.DataFrame(df_team[stats_agg].sum()).T
                avg_team = np.round(avg_team_calc[stats_agg[1]] / avg_team_calc[stats_agg[0]] * 100, 2).values[0]
                avg_opp_calc = pd.DataFrame(df_opp[stats_agg].sum()).T
                avg_opp = np.round(avg_opp_calc[stats_agg[1]] / avg_opp_calc[stats_agg[0]] * 100, 2).values[0]
            else:
                avg_team = np.round(df_team[stat_name].mean(), 2)
                avg_opp = np.round(df_opp[stat_name].mean(), 2)

            better = np.round(np.sum(df_team[stat_name] > df_opp[stat_name]) / len(df_opp) * 100, 2)
            # ##### Statistical Significance
            stat_sig = ttest_ind(df_team[stat_name].values,
                                df_opp[stat_name].values)[1]

            if len(df_team) >= 10:
                if stat_sig <= 0.05:
                    if avg_team > avg_opp:
                        stat_sig_name = "Statistically Better"
                    elif avg_team < avg_opp:
                        stat_sig_name = "Statistically Worse"
                    else:
                        stat_sig_name = ""
                else:
                    stat_sig_name = ""
            else:
                stat_sig_name = ""
        else:
            match_day_fig = None
            avg_team = ""
            avg_opp = ""
            better = ""
            stat_sig_name = ""

        return match_day_fig, avg_team, avg_opp, better, stat_sig_name
    
    # ##### Season Stats
    st.cache_data
    def team_season_stats(self,
                          data:pd.DataFrame, 
                          team:str) -> tuple[pd.DataFrame, 
                                            pd.DataFrame]:

        team_season_data = data.copy()

        # ##### Filter Data Based on Team
        team_data_stats = team_season_data[team_season_data['Team'] == team].reset_index(drop=True)
        opponent_data_stats = team_season_data[team_season_data['Opponent'] == team].reset_index(drop=True)

        # ##### Stats Aggregation based on Season Filter
        possible_season_filters = pd.concat([team_data_stats, opponent_data_stats])[self.season_filter.season_filter].sum() > 0
        season_filters = pd.concat([team_data_stats, opponent_data_stats])[self.season_filter.season_filter].sum()[possible_season_filters].index.to_list()

        # ##### Create Team / Opponent Count Stats
        season_team_stats = []
        season_opponent_stats = []
        for filter in season_filters:
            season_team_stats.append(list(team_data_stats[team_data_stats[filter] == 1][self.team_stats.stats_count_calculations].mean().values))
            season_opponent_stats.append(list(opponent_data_stats[opponent_data_stats[filter] == 1][self.team_stats.stats_count_calculations].mean().values))
        season_team_stats = pd.DataFrame(season_team_stats, columns=self.team_stats.stats_count_calculations, index=season_filters)
        season_opponent_stats = pd.DataFrame(season_opponent_stats, columns=self.team_stats.stats_count_calculations, index=season_filters)
        season_team_stats['Aerial Duel'] = season_team_stats['Aerial Duel Won'] + season_team_stats['Aerial Duel Lost']
        season_opponent_stats['Aerial Duel'] = season_opponent_stats['Aerial Duel Won'] + season_opponent_stats['Aerial Duel Lost']

        # ##### Aggregate % Stats
        for stat in self.team_stats.stats_perc_calculations.keys():
            season_team_stats[stat] = season_team_stats[self.team_stats.stats_perc_calculations[stat][1]] / season_team_stats[
                self.team_stats.stats_perc_calculations[stat][0]] * 100
            season_opponent_stats[stat] = season_opponent_stats[self.team_stats.stats_perc_calculations[stat][1]] / season_opponent_stats[
                self.team_stats.stats_perc_calculations[stat][0]] * 100

        # ##### Final Processing for Team Statistics
        season_team_stats.drop(columns=['Aerial Duel'], inplace=True)
        season_team_stats = season_team_stats.T
        season_team_stats = season_team_stats.reindex(self.team_stats.stats_team)
        season_team_stats = season_team_stats.reset_index(drop=False)
        season_team_stats.rename(columns={'index':'Stat'}, inplace=True)
        season_team_stats.replace([np.inf, -np.inf], np.nan, inplace=True)

        # ##### Final Processing for Opponent Statistics
        season_opponent_stats.drop(columns=['Aerial Duel'], inplace=True)
        season_opponent_stats = season_opponent_stats.T
        season_opponent_stats = season_opponent_stats.reindex(self.team_stats.stats_team)
        season_opponent_stats = season_opponent_stats.reset_index(drop=False)
        season_opponent_stats.rename(columns={'index':'Stat'}, inplace=True)
        season_opponent_stats.replace([np.inf, -np.inf], np.nan, inplace=True)

        return season_team_stats, season_opponent_stats

    # ##### Season Filter
    def team_season_filter(self,
                           data_team_agg:pd.DataFrame, 
                           data_opp_agg:pd.DataFrame, 
                           team:str,
                           stat_name:str) -> tuple[px.bar, 
                                                list, 
                                                float, 
                                                float, 
                                                list, 
                                                float, 
                                                float]:

        # ##### Season Filter Stats
        team_stat = data_team_agg[data_team_agg['Stat'] == stat_name]
        opponent_stat = data_opp_agg[data_opp_agg['Stat'] == stat_name]
        data_agg = pd.concat([team_stat.drop(columns='Stat'), opponent_stat.drop(columns='Stat')], axis=1).T
        data_agg.reset_index(drop=False, inplace=True)
        data_agg.loc[:int(len(data_agg) / 2), 'Team'] = team
        data_agg.loc[int(len(data_agg) / 2):, 'Team'] = 'Opponent'
        data_agg.columns = ['Season Filter', stat_name, 'Team']

        # ##### Plot Min and Max Values
        min_value = np.min(data_agg[stat_name]) * 0.8
        if min_value < 10:
            min_value = 0
        max_value = np.max(data_agg[stat_name]) * 1.1

        # ##### Plot Data
        team_stat_fig = px.bar(data_agg,
                            x="Season Filter",
                            y=stat_name,
                            color="Team",
                            barmode='group',
                            color_discrete_map={
                                team: "rgb(200,11,1)",
                                'Opponent': "rgb(179, 179, 179)"}, 
                                height=400,
                                text=stat_name,
                                text_auto='.2f',
                                title=f"{team} {stat_name} per Game")
        team_stat_fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)"},
            yaxis_range=[min_value, max_value])

        # ##### Season Filter Insights Home vs Away
        team_insight_data = data_agg[data_agg['Team'] == team]
        period_venue = ""
        period_venue_1 = np.nan
        period_venue_2 = np.nan
        if ("Home" in team_insight_data.dropna()['Season Filter'].values) and ("Away" in team_insight_data.dropna()['Season Filter'].values):
            if team_insight_data[team_insight_data['Season Filter'] == 'Home'][stat_name].values[0] > team_insight_data[team_insight_data['Season Filter'] == 'Away'][stat_name].values[0]:
                period_venue = ['Home', 'Away']
                period_venue_1 = team_insight_data[team_insight_data['Season Filter'] == 'Home'][stat_name].values[0]
                period_venue_2 = team_insight_data[team_insight_data['Season Filter'] == 'Away'][stat_name].values[0]
            else:
                period_venue = ['Away', 'Home']
                period_venue_1 = team_insight_data[team_insight_data['Season Filter'] == 'Away'][stat_name].values[0]
                period_venue_2 = team_insight_data[team_insight_data['Season Filter'] == 'Home'][stat_name].values[0]

        # ##### Season Filter Insights 1st Half vs 2nd Half
        period_insights = ""
        period_insights_1 = np.nan
        period_insights_2 = np.nan
        if "2nd Half" in team_insight_data.dropna()['Season Filter'].values:
            if team_insight_data[team_insight_data['Season Filter'] == '1st Half'][stat_name].values[0] > team_insight_data[team_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]:
                period_insights = ['1st Half', '2nd Half']
                period_insights_1 = team_insight_data[team_insight_data['Season Filter'] == '1st Half'][stat_name].values[0]
                period_insights_2 = team_insight_data[team_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]
            else:
                period_insights = ['2nd Half', '1st Half']
                period_insights_1 = team_insight_data[team_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]
                period_insights_2 = team_insight_data[team_insight_data['Season Filter'] == '1st Half'][stat_name].values[0]

        return team_stat_fig, period_venue, period_venue_1, period_venue_2, period_insights, period_insights_1, period_insights_2

    # ##### Comparison Stats
    def last_games_results(self,
                           data:pd.DataFrame,
                           team_opponent:str,
                           season_filter:str) -> pd.DataFrame:
        seasons_data = data.copy()
        # ##### Filter Only Team and Opponent Games
        games_opponent = seasons_data[(seasons_data['Opponent'] == team_opponent) & 
                                    (seasons_data['Season Id'] <= self.season_info.season_id[season_filter] + 1)].sort_values(by=['Season Id', 'Week No'], ascending=[False, False])

        # ##### Get Last 5 Games Played
        last_5_games_df = games_opponent.iloc[:5,:][['Season Id', 'Week No', 'Venue', 'Team', 'Opponent', 'Goals', 'Goals Ag']]

        # ##### Create Last 5 Games
        change_opponent = last_5_games_df.loc[last_5_games_df['Venue'] == 'Away',['Opponent','Team']]
        last_5_games_df.loc[last_5_games_df['Venue'] == 'Away','Team'] = change_opponent['Opponent']
        last_5_games_df.loc[last_5_games_df['Venue'] == 'Away','Opponent'] = change_opponent['Team']
        change_goals = last_5_games_df.loc[last_5_games_df['Venue'] == 'Away',['Goals','Goals Ag']]
        last_5_games_df.loc[last_5_games_df['Venue'] == 'Away', 'Goals'] = change_goals['Goals Ag']
        last_5_games_df.loc[last_5_games_df['Venue'] == 'Away', 'Goals Ag'] = change_goals['Goals']
        last_5_games_df['Result'] = last_5_games_df['Goals'].astype(str) + '-' + last_5_games_df['Goals Ag'].astype(str)
        last_5_games_df = last_5_games_df[['Season Id', 'Week No', 'Team', 'Result', 'Opponent']]
        last_5_games_df['Season Id'] = last_5_games_df['Season Id'].map(dict((int(value+1), key) for key, value in self.season_info.season_id.items()))

        last_5_games_df.rename(columns={'Season Id':'Season', 'Week No':'Week No', 'Team':'Home Team', 'Opponent':'Away Team'}, inplace=True)
        
        return last_5_games_df

    def _comparison_all_stats(self,
                             data:pd.DataFrame,
                             team:str,
                             opponent:str,
                             filter_season:str) -> tuple[pd.DataFrame, list]:

        season_data = data.copy()
        team_season_data = season_data[(season_data['Team'].isin([team, opponent])) & (season_data[filter_season] == 1)].copy()

        # ##### Aggregate Team Count Stats
        season_team_data = team_season_data.groupby('Team')[self.team_stats.stats_count_calculations].mean().T

        # ##### Aggregate % Stats
        for stat in self.team_stats.stats_perc_calculations.keys():
            stat_perc = pd.DataFrame(team_season_data.groupby('Team')[self.team_stats.stats_perc_calculations[stat][1]].sum() / 
                team_season_data.groupby('Team')[self.team_stats.stats_perc_calculations[stat][0]].sum() * 100).T
            stat_perc.index = [stat]
            season_team_data = pd.concat([season_team_data, stat_perc])
        
        # ##### Merge Team Comparison Stats
        season_team_data = season_team_data.reindex(self.team_stats.stats_team)
        if team not in season_team_data.columns:
            season_team_data[team] = np.nan
        if opponent not in season_team_data.columns:
            season_team_data[opponent] = np.nan

        # ##### Calculate Significance Level
        sig_comparison_test = []
        for stat in self.team_stats.stats_team:
            sig_comparison_test.append(ttest_ind(a=team_season_data[team_season_data['Team'] == team][stat].values, 
                                                b=team_season_data[team_season_data['Team'] == opponent][stat].values).pvalue)
        season_team_data['Sig'] = sig_comparison_test
        season_team_data['Sig'] = season_team_data.apply(lambda x: "🟢" if x['Sig'] <=0.05 and x[team] > x[opponent] else (
            "🔴" if x['Sig'] <=0.05 and x[team] < x[opponent] else np.nan), axis=1)
            
        season_team_data = season_team_data[[team, opponent, "Sig"]].reset_index(drop=False)
        season_team_data.rename(columns={"index": "Statistics"}, inplace=True)

        # ##### Insight Significance Level
        insight_df = season_team_data['Sig'].value_counts().reset_index(drop=False)
        insight_df['Sig'] = insight_df['Sig'].map({"🟢":'Up',"🔴":'Down'})
        insight_data = []
        if "Up" in insight_df['Sig'].values:
            insight_data.append(insight_df[insight_df['Sig'] == "Up"]['count'].values[0]),
        else:
            insight_data.append(0)
        if "Down" in insight_df['Sig'].values:
            insight_data.append(insight_df[insight_df['Sig'] == "Down"]['count'].values[0]),
        else:
            insight_data.append(0)

        return season_team_data, insight_data

    def team_stats_comparison(self,
                              data:pd.DataFrame,
                            team:str,
                            opponent:str,
                            filter_stats:str,
                            filter_season:str) -> tuple[GameStatsStyle.radar_plot, 
                                                        GameStatsStyle.radar_plot, 
                                                        pd.DataFrame, 
                                                        list]:
        
        season_data = data.copy()
        season_data['Aerial Duel'] = season_data['Aerial Duel Won'] + season_data['Aerial Duel Lost']

        # ##### Stats Filter
        comparison_stats = self.comparison_stats.team_stats_list[filter_stats]

        # ##### Team Statistics
        team_data = season_data[(season_data['Team'] == team) & (season_data[filter_season] == 1)].reset_index()
        season_team_stats = []
        for stat in comparison_stats:
            if stat in self.team_stats.stats_count_calculations:
                season_team_stats.append(team_data[stat].mean())
            else:
                season_team_stats.append(team_data[self.team_stats.stats_perc_calculations[stat][1]].sum() / team_data[
                    self.team_stats.stats_perc_calculations[stat][0]].sum() * 100)

        # ##### Opponent Data
        opponent_data = season_data[(season_data['Team'] == opponent) & (season_data[filter_season] == 1)].reset_index()
        season_opponent_stats = []
        for stat in comparison_stats:
            if stat in self.team_stats.stats_count_calculations:
                season_opponent_stats.append(opponent_data[stat].mean())
            else:
                season_opponent_stats.append(opponent_data[self.team_stats.stats_perc_calculations[stat][1]].sum() / opponent_data[
                    self.team_stats.stats_perc_calculations[stat][0]].sum() * 100)

        # ##### Radar Ranges
        min_stats = []
        max_stats = []
        for stat in comparison_stats:
            min_stats.append(season_data[stat].min())
            max_stats.append(season_data[stat].max())
            
        # ##### Team Radar Plot
        team_plot = self.game_stats_style.radar_plot(stats=season_team_stats,
                            comparison_stats=comparison_stats,
                            min_stats=min_stats,
                            max_stats=max_stats)
        
        # ##### Team Radar Plot
        opponent_plot = self.game_stats_style.radar_plot(stats=season_opponent_stats,
                            comparison_stats=comparison_stats,
                            min_stats=min_stats,
                            max_stats=max_stats)
        
        # ##### All Stats Comparison
        stats_comparison, comparison_insights = self._comparison_all_stats(data=season_data, 
                                                                    team=team, 
                                                                    opponent=opponent,
                                                                    filter_season=filter_season)
        
        return team_plot, opponent_plot, stats_comparison, comparison_insights

    st.cache_data
    def team_week_rank(self,
                       data:pd.DataFrame,
                       team:str, 
                       opponent:str, 
                       season) -> plt:
        
        # ##### Season Data
        season_df = data.copy()
        max_day = season_df['Week No'].max()

        # #### Create Match Day Tab
        team_rank = []
        opponent_rank = []
        for day in range(1, max_day + 1):
            match_day_df = season_df[season_df['Week No'] <= day]
            # ##### Run Table Data
            tab_data = GameStatsProcessing().buli_table_data(data=match_day_df,
                                                             table_type='Season')
            team_rank.append(tab_data[tab_data['Team'] == team].index[0])
            opponent_rank.append(tab_data[tab_data['Team'] == opponent].index[0])
        
        # ##### Team vs Team Match Day Rank
        team_week_rank = {team:team_rank, 
                        opponent:opponent_rank}
        
        # ##### match-week
        match_day = ["Week " + str(num) for num in range(1, max_day + 1)]

        # ##### highlight dict
        highlight_dict = {
            team: "#d20614",
            opponent: "#000000",
        }

        # ##### instantiate object
        bumpy = Bumpy(
            background_color="#ffffff", 
            line_color="#e5e5e6",
            scatter_color="#e5e5e6",
            label_color="#000000",
            rotate_xticks=90, 
            ticklabel_size=10, 
            label_size=15,
            scatter_points='D', 
            scatter_primary='o', 
            scatter_size=100,  
            show_right=True,
            plot_labels=True,
            alignment_yvalue=0.1, 
            alignment_xvalue=0.065 
        )

        # ##### plot bumpy chart
        fig, _ = bumpy.plot(
            x_list=match_day,
            y_list=np.linspace(1, 18, 18).astype(int),
            values=team_week_rank,
            secondary_alpha=0.2,
            highlight_dict=highlight_dict,
            figsize=(20, 10),
            x_label='Week', 
            y_label='Position',
            ylim=(-0.1, 20),
            lw=2.5,
            font="Sans serif"
        )

        plt.tight_layout(pad=0.5)

        return fig

    # ##### Last 5 Season Stats
    def team_last_seasons_stats(self,
                                data:pd.DataFrame,
                                season_filter:str,
                                stat_filter:str):

        all_seasons_data = data.copy()
        all_seasons_data['Aerial Duel'] = all_seasons_data['Aerial Duel Won'] + all_seasons_data['Aerial Duel Lost']

        # ##### Filter Data by Season Filter
        all_seasons_data = all_seasons_data[all_seasons_data[season_filter] == 1].reset_index(drop=True)
        
        # ##### Map Season Id
        all_seasons_data['Season Id'] = all_seasons_data['Season Id'].map(dict((value + 1, key) for key, value in self.season_info.season_id.items()))
        
        # ##### Create Team Count Stats
        seasons_team_data = all_seasons_data.groupby('Season Id')[self.team_stats.stats_count_calculations].mean().T

        # ##### Aggregate % Stats
        for stat in self.team_stats.stats_perc_calculations.keys():
            stat_perc = pd.DataFrame(all_seasons_data.groupby('Season Id')[self.team_stats.stats_perc_calculations[stat][1]].sum() / 
                                    all_seasons_data.groupby('Season Id')[self.team_stats.stats_perc_calculations[stat][0]].sum() * 100).T
            stat_perc.index = [stat]
            seasons_team_data = pd.concat([seasons_team_data, stat_perc])

        # ##### Calculate Season Comparison Significance Level
        current_season = all_seasons_data['Season Id'].unique()[-1]
        if all_seasons_data['Season Id'].nunique() > 1:
            previous_season = all_seasons_data['Season Id'].unique()[-2]
        else:
            previous_season = current_season

        sig_comparison_test = []
        for stat in self.team_stats.stats_team:
            sig_comparison_test.append(ttest_ind(a=all_seasons_data[all_seasons_data['Season Id'] == current_season][stat].values, 
                                                b=all_seasons_data[all_seasons_data['Season Id'] == previous_season][stat].values).pvalue)
        seasons_team_data['Sig'] = sig_comparison_test
        seasons_team_data['Sig'] = seasons_team_data.apply(
            lambda x: "🟢" if x['Sig'] <=0.05 and x[self.season_info.season_id.keys()[-1]] > 
            x[self.season_info.season_id.keys()[-2]] else (
            "🔴" if x['Sig'] <=0.05 and x[self.season_info.season_id.keys()[-1]] < x[self.season_info.season_id.keys()[-2]] else np.nan), axis=1)
        seasons_team_data.reset_index(drop=False, inplace=True)
        seasons_team_data.rename(columns = {'index':'Statistics'}, inplace=True)

        # ##### Insight Significance Level
        insight_df = seasons_team_data['Sig'].value_counts().reset_index(drop=False)
        insight_df['Sig'] = insight_df['Sig'].map({"🟢":'Up',"🔴":'Down'})
        insight_season_comparison = [current_season, previous_season]
        if "Up" in insight_df['Sig'].values:
            insight_season_comparison.append(insight_df[insight_df['Sig'] == "Up"]['count'].values[0]),
        else:
            insight_season_comparison.append(0)
        if "Down" in insight_df['Sig'].values:
            insight_season_comparison.append(insight_df[insight_df['Sig'] == "Down"]['count'].values[0]),
        else:
            insight_season_comparison.append(0)

        # ##### Last 5 Season Stats Plot Data
        plot_data = seasons_team_data[seasons_team_data['Statistics'] == stat_filter]
        seasons = list(seasons_team_data.columns[1:-1])
        plot_seasons = pd.pivot_table(plot_data, 
                                    values=seasons, 
                                    columns=[stat_filter]).reset_index(drop=False)
        plot_seasons.rename(columns={'Season Id':'Season'}, inplace=True)

        # ##### Find Min and Max Plot Values
        min_value = np.min(plot_seasons[stat_filter]) * 0.8
        if min_value < 10:
            min_value = 0
        max_value = np.max(plot_seasons[stat_filter]) * 1.1

        seasons_fig = px.bar(plot_seasons, 
                            x='Season', 
                            y=stat_filter, 
                            color="Season", 
                            color_discrete_map={
                                self.season_info.season_id.keys()[-5]: "#000000",
                                self.season_info.season_id.keys()[-4]: "#A0A0A0",
                                self.season_info.season_id.keys()[-3]: "#e5e5e6",
                                self.season_info.season_id.keys()[-2]: "#FFA0A0",
                                self.season_info.season_id.keys()[-1]: "#d20614"},
                            height=400, 
                            text=stat_filter, 
                            text_auto='.2f', 
                            title=f"Last 5 Seasons {stat_filter} per Game")
        seasons_fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)"}, 
            yaxis_range=[min_value, max_value])
        
        # ##### Insights Previous 5 Seasons
        insights_5_seasons = [plot_seasons.shape[0], 
                            plot_seasons.sort_values(by=stat_filter, ascending=False)['Season'].values[0]]
            
        return seasons_team_data, seasons_fig, insight_season_comparison, insights_5_seasons

class PlayerStatsAnalysis:

    def __init__(self, player_type:str='') -> None:

        self.season_info = GameStatsConfiguration().get_season_info()
        self.season_filter = GameStatsConfiguration().get_season_filter()
        self.player_type = player_type
        if self.player_type != 'Gk':
            self.player_stats = GameStatsConfiguration().get_player_stats()
            self.analysis_options = ["Season", "Player vs Player", "Last 5 Seasons"]
        else:
            self.player_stats = GameStatsConfiguration().get_gk_stats()
            self.analysis_options = ["Season", "Gk vs Gk", "Last 5 Seasons"]
        self.comparison_stats = GameStatsConfiguration().get_comparison_stats()
        self.teams_info = GameStatsConfiguration().get_teams_info()
        self.game_stats_style = GameStatsStyle()

    # ##### Match Day Analysis
    def player_day_analysis(self,
                            data:pd.DataFrame, 
                            team:str, 
                            player:str,
                            stat_name:str) -> px:
    
        # ##### Create Aerial Duel Total Stat
        df_match_day = data[(data['Team'] == team) & (data['Name'] == player)].reset_index(drop=False)
        if self.player_type != 'Gk':
            df_match_day['Aerial Duel'] = df_match_day['Aerial Duel Won'] + df_match_day['Aerial Duel Lost']

        # ##### Create Player Chart
        min_value = np.min(df_match_day[stat_name]) * 0.8
        if min_value < 10:
            min_value = 0
        max_value = np.max(df_match_day[stat_name]) * 1.1

        if df_match_day[stat_name].sum() > 0:
            match_day_fig = px.bar(df_match_day, 
                                x="Week No", 
                                y=stat_name, 
                                color="Result", 
                                color_discrete_map={
                                    'Win': "rgb(200,11,1)",
                                    'Draw': "rgb(179, 179, 179)",
                                    'Defeat': "rgb(78,78,80)",}, 
                                text=stat_name,
                                title=f"{player} {stat_name}")
            match_day_fig.update_layout({
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
            },
                xaxis1=dict(
                    tickmode='array',
                    tickvals=[i for i in range(1, len(df_match_day) + 1)],
                    ticktext=df_match_day['Week No'].unique(),
                ), 
                yaxis_range=[min_value, max_value]
            )
        else:
            match_day_fig = None

        return match_day_fig
    
    st.cache_data
    # ##### Season Stats
    def player_season_stats(self,
                            data:pd.DataFrame, 
                            team:str, 
                            player:str) -> pd.DataFrame:

        # # ##### Filter Data Based on Player
        player_season_data = data[(data['Team'] == team) & (data['Name'] == player)].reset_index(drop=False)

        # ##### Stats Aggregation based on Season Filter
        possible_season_filters = player_season_data[self.season_filter.season_filter].sum() > 0
        season_filters = player_season_data[self.season_filter.season_filter].sum()[possible_season_filters].index.to_list()

        # ##### Create Count Stats
        season_player_stats = []
        for filter in season_filters:
            season_player_stats.append(list(player_season_data[player_season_data[filter] == 1][self.player_stats.stats_count_calculations].mean().values))
        season_player_stats = pd.DataFrame(season_player_stats, columns=self.player_stats.stats_count_calculations, index=season_filters)
        if self.player_type != 'Gk':
            season_player_stats['Aerial Duel'] = season_player_stats['Aerial Duel Won'] + season_player_stats['Aerial Duel Lost']

        # ##### Aggregate % Stats
        for stat in self.player_stats.stats_perc_calculations.keys():
            season_player_stats[stat] = season_player_stats[self.player_stats.stats_perc_calculations[stat][1]] / season_player_stats[
                self.player_stats.stats_perc_calculations[stat][0]] * 100

        # ##### Final Processing for Player Statistics
        if self.player_type != 'Gk':
            season_player_stats.drop(columns=['Aerial Duel'], inplace=True)
            stats_name = self.player_stats.stats_player
        else:
            stats_name = self.player_stats.stats_gk
        season_player_stats = season_player_stats.T
        season_player_stats = season_player_stats.reindex(stats_name)
        season_player_stats = season_player_stats.reset_index(drop=False)
        season_player_stats.rename(columns={'index':'Stat'}, inplace=True)
        season_player_stats.replace([np.inf, -np.inf], np.nan, inplace=True)

        return season_player_stats
    
    # ##### Season Filter
    def player_season_filter(self,
                             data_player_agg:pd.DataFrame, 
                             player:str, 
                             stat_name:str) -> tuple[px.bar, 
                                                list, 
                                                float, 
                                                float, 
                                                list, 
                                                float, 
                                                float]:

        # ##### Season Filter Stats
        data_agg = data_player_agg[data_player_agg['Stat'] == stat_name].T.reset_index(drop=False)
        data_agg = data_agg.iloc[1:]
        data_agg.columns = ['Season Filter', stat_name]

        # ##### Plot Min and Max Values
        min_value = np.min(data_agg[stat_name]) * 0.8
        if min_value < 10:
            min_value = 0
        max_value = np.max(data_agg[stat_name]) * 1.1

        # ##### Plot Data
        player_stat_fig = px.bar(data_agg,
                                x="Season Filter",
                                y=stat_name,
                                height=400,
                                text=stat_name,
                                text_auto='.2f',
                                title=f"{player} {stat_name} per Game")
        player_stat_fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)"},
            yaxis_range=[min_value, max_value])
        player_stat_fig.update_traces(marker_color="rgb(200,11,1)")

        # ##### Season Filter Insights Home vs Away
        player_insight_data = data_agg.copy()
        period_venue = ""
        period_venue_1 = np.nan
        period_venue_2 = np.nan
        if ("Home" in player_insight_data.dropna()['Season Filter'].values) and ("Away" in player_insight_data.dropna()['Season Filter'].values):
            if player_insight_data[player_insight_data['Season Filter'] == 'Home'][stat_name].values[0] > player_insight_data[player_insight_data['Season Filter'] == 'Away'][stat_name].values[0]:
                period_venue = ['Home', 'Away']
                period_venue_1 = player_insight_data[player_insight_data['Season Filter'] == 'Home'][stat_name].values[0]
                period_venue_2 = player_insight_data[player_insight_data['Season Filter'] == 'Away'][stat_name].values[0]
            else:
                period_venue = ['Away', 'Home']
                period_venue_1 = player_insight_data[player_insight_data['Season Filter'] == 'Away'][stat_name].values[0]
                period_venue_2 = player_insight_data[player_insight_data['Season Filter'] == 'Home'][stat_name].values[0]

        # ##### Season Filter Insights 1st Half vs 2nd Half
        period_insights = ""
        period_insights_1 = np.nan
        period_insights_2 = np.nan
        if "2nd Half" in player_insight_data.dropna()['Season Filter'].values:
            if player_insight_data[player_insight_data['Season Filter'] == '1st Half'][stat_name].values[0] > player_insight_data[player_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]:
                period_insights = ['1st Half', '2nd Half']
                period_insights_1 = player_insight_data[player_insight_data['Season Filter'] == '1st Half'][stat_name].values[0]
                period_insights_2 = player_insight_data[player_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]
            else:
                period_insights = ['2nd Half', '1st Half']
                period_insights_1 = player_insight_data[player_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]
                period_insights_2 = player_insight_data[player_insight_data['Season Filter'] == '1st Half'][stat_name].values[0]

        return player_stat_fig, period_venue, period_venue_1, period_venue_2, period_insights, period_insights_1, period_insights_2

    # ##### Comparison Stats
    def _comparison_all_stats(self,
                            data:pd.DataFrame,
                            team:str,
                            team_player:str,
                            opponent:str,
                            opponent_player:str,
                            filter_season:str) -> tuple[pd.DataFrame, list]:

        season_data = data.copy()
        players_season_data = season_data[(season_data['Team'].isin([team, opponent])) & 
                                        (season_data['Name'].isin([team_player, opponent_player])) & 
                                        (season_data[filter_season] == 1)].copy()
   
        # ##### Aggregate Player Count Stats
        season_players_data = players_season_data.groupby('Name')[self.player_stats.stats_count_calculations].mean().T

        # ##### Aggregate % Stats
        for stat in self.player_stats.stats_perc_calculations.keys():
            stat_perc = pd.DataFrame(players_season_data.groupby('Name')[self.player_stats.stats_perc_calculations[stat][1]].sum() / 
                players_season_data.groupby('Name')[self.player_stats.stats_perc_calculations[stat][0]].sum() * 100).T
            stat_perc.index = [stat]
            season_players_data = pd.concat([season_players_data, stat_perc])
        
        # ##### Merge Player Comparison Stats
        if self.player_type != 'Gk':
            stats_name = self.player_stats.stats_player
        else:
            stats_name = self.player_stats.stats_gk
        season_players_data = season_players_data.reindex(stats_name)
        if team_player not in season_players_data.columns:
            season_players_data[team_player] = np.nan
        if opponent_player not in season_players_data.columns:
            season_players_data[opponent_player] = np.nan

        # ##### Calculate Significance Level
        sig_comparison_test = []
        if self.player_type != "Gk":
            for stat in self.player_stats.stats_player:
                    sig_comparison_test.append(ttest_ind(a=players_season_data[players_season_data['Name'] == team_player][stat].values, 
                                                        b=players_season_data[players_season_data['Name'] == opponent_player][stat].values).pvalue)
        else:
            for stat in self.player_stats.stats_gk:
                    sig_comparison_test.append(ttest_ind(a=players_season_data[players_season_data['Name'] == team_player][stat].values, 
                                                        b=players_season_data[players_season_data['Name'] == opponent_player][stat].values).pvalue)
        season_players_data['Sig'] = sig_comparison_test
        season_players_data['Sig'] = season_players_data.apply(lambda x: "🟢" if x['Sig'] <=0.05 and x[team_player] > x[opponent_player] else (
            "🔴" if x['Sig'] <=0.05 and x[team_player] < x[opponent_player] else np.nan), axis=1)
            
        season_players_data = season_players_data[[team_player, opponent_player, "Sig"]].reset_index(drop=False)
        season_players_data.rename(columns={"index": "Statistics"}, inplace=True)
        
        # ##### Insight Significance Level
        insight_df = season_players_data['Sig'].value_counts().reset_index(drop=False)
        insight_df['Sig'] = insight_df['Sig'].map({"🟢":'Up',"🔴":'Down'})
        insight_data = []
        if "Up" in insight_df['Sig'].values:
            insight_data.append(insight_df[insight_df['Sig'] == "Up"]['count'].values[0]),
        else:
            insight_data.append(0)
        if "Down" in insight_df['Sig'].values:
            insight_data.append(insight_df[insight_df['Sig'] == "Down"]['count'].values[0]),
        else:
            insight_data.append(0)

        return season_players_data, insight_data
    
    def player_stats_comparison(self,
                                data:pd.DataFrame,
                                team:str,
                                team_player:str,
                                opponent:str,
                                opponent_player:str,
                                filter_season:str,
                                filter_stats:str=None):
    
        season_data = data.copy()
        if self.player_type != 'Gk':
            season_data['Aerial Duel'] = season_data['Aerial Duel Won'] + season_data['Aerial Duel Lost']
            ##### Stats Filter
            comparison_stats = self.comparison_stats.player_stats_list[filter_stats]
        else:
            ##### Stats Filter
            comparison_stats = self.comparison_stats.gk_stats

        # ##### Player Statistics
        team_player_data = season_data[(season_data['Team'] == team) & 
                                    (season_data['Name'] == team_player) & 
                                    (season_data[filter_season] == 1)].reset_index()
        team_player_stats = []
        for stat in comparison_stats:
            if stat in self.player_stats.stats_count_calculations:
                team_player_stats.append(team_player_data[stat].mean())
            else:
                team_player_stats.append(team_player_data[self.player_stats.stats_perc_calculations[stat][1]].sum() / team_player_data[
                    self.player_stats.stats_perc_calculations[stat][0]].sum() * 100)

        # ##### Opponent Player Statistics
        opponent_player_data = season_data[(season_data['Team'] == opponent) & 
                                        (season_data['Name'] == opponent_player) & 
                                        (season_data[filter_season] == 1)].reset_index()    
        opponent_player_stats = []
        for stat in comparison_stats:
            if stat in self.player_stats.stats_count_calculations:
                opponent_player_stats.append(opponent_player_data[stat].mean())
            else:
                opponent_player_stats.append(opponent_player_data[self.player_stats.stats_perc_calculations[stat][1]].sum() / opponent_player_data[
                    self.player_stats.stats_perc_calculations[stat][0]].sum() * 100)

        # ##### Radar Ranges
        min_stats = []
        max_stats = []
        for stat in comparison_stats:
            min_stats.append(season_data[stat].min())
            max_stats.append(season_data[stat].max())
            
        # ##### Player Radar Plot
        team_player_plot = self.game_stats_style.radar_plot(stats=team_player_stats,
                                    comparison_stats=comparison_stats,
                                    min_stats=min_stats,
                                    max_stats=max_stats,
                                    radar_name=True,
                                    player_name=team_player)
        
        # ##### Opponent Radar Plot
        opponent_player_plot = self.game_stats_style.radar_plot(stats=opponent_player_stats,
                                                         comparison_stats=comparison_stats,
                                                         min_stats=min_stats,
                                                         max_stats=max_stats,
                                                         radar_name=True,
                                                         player_name=opponent_player)
        
        # ##### All Stats Comparison
        stats_comparison, comparison_insights = self._comparison_all_stats(
            data=season_data,
            team=team,
            team_player=team_player,
            opponent=opponent,
            opponent_player=opponent_player,
            filter_season=filter_season)
        
        return team_player_plot, opponent_player_plot, stats_comparison, comparison_insights
         
    # ##### Last 5 Season Stats
    def player_last_seasons_stats(self,
                                  data:pd.DataFrame,
                                  team:str,
                                  season_filter:str,
                                  stat_filter:str):

        all_seasons_data = data.copy()
        if self.player_type != 'Gk':
            all_seasons_data['Aerial Duel'] = all_seasons_data['Aerial Duel Won'] + all_seasons_data['Aerial Duel Lost']

        # ##### Filter Data by Season Filter
        all_seasons_data = all_seasons_data[all_seasons_data[season_filter] == 1].reset_index(drop=True)
        
        # ##### Map Season Id
        all_seasons_data['Season Id'] = all_seasons_data['Season Id'].map(dict((value + 1, key) for key, value in self.season_info.season_id.items()))
        
        # ##### Create Player Count Stats
        seasons_player_data = all_seasons_data.groupby('Season Id')[self.player_stats.stats_count_calculations].mean().T

        # ##### Aggregate % Stats
        for stat in self.player_stats.stats_perc_calculations.keys():
            stat_perc = pd.DataFrame(all_seasons_data.groupby('Season Id')[self.player_stats.stats_perc_calculations[stat][1]].sum() / 
                                    all_seasons_data.groupby('Season Id')[self.player_stats.stats_perc_calculations[stat][0]].sum() * 100).T
            stat_perc.index = [stat]
            seasons_player_data = pd.concat([seasons_player_data, stat_perc])

        # ##### Calculate Season Comparison Significance Level
        current_season = all_seasons_data['Season Id'].unique()[-1]
        if all_seasons_data['Season Id'].nunique() > 1:
            previous_season = all_seasons_data['Season Id'].unique()[-2]
        else:
            previous_season = current_season

        sig_comparison_test = []
        if self.player_type != 'Gk':
            for stat in self.player_stats.stats_player:
                sig_comparison_test.append(ttest_ind(a=all_seasons_data[all_seasons_data['Season Id'] == current_season][stat].values, 
                                                    b=all_seasons_data[all_seasons_data['Season Id'] == previous_season][stat].values).pvalue)
        else:
            for stat in self.player_stats.stats_gk:
                sig_comparison_test.append(ttest_ind(a=all_seasons_data[all_seasons_data['Season Id'] == current_season][stat].values, 
                                                    b=all_seasons_data[all_seasons_data['Season Id'] == previous_season][stat].values).pvalue)
        seasons_player_data['Sig'] = sig_comparison_test
        seasons_player_data['Sig'] = seasons_player_data.apply(
            lambda x: "🟢" if x['Sig'] <=0.05 and x[current_season] > x[previous_season] else (
                    "🔴" if x['Sig'] <=0.05 and x[current_season] < x[previous_season] else np.nan), axis=1)
        seasons_player_data['Sig_count'] = sig_comparison_test
        seasons_player_data['Sig_count'] = seasons_player_data.apply(
            lambda x: "Sig Team" if x['Sig_count'] <=0.05 and x[current_season] > x[previous_season] else (
                    "Sig Opp" if x['Sig_count'] <=0.05 and x[current_season] < x[previous_season] else np.nan), axis=1)
        seasons_player_data.reset_index(drop=False, inplace=True)
        seasons_player_data.rename(columns = {'index':'Statistics'}, inplace=True)
        
        # ##### Insight Significance Level
        insight_df = seasons_player_data['Sig_count'].value_counts().reset_index(drop=False)
        insight_season_comparison = [current_season, previous_season]
        if "Sig Team" in insight_df['index'].values:
            insight_season_comparison.append(insight_df[insight_df['index'] == "Sig Team"]['Sig_count'].values[0]),
        else:
            insight_season_comparison.append(0)
        if "Sig Opp" in insight_df['index'].values:
            insight_season_comparison.append(insight_df[insight_df['index'] == "Sig Opp"]['Sig_count'].values[0]),
        else:
            insight_season_comparison.append(0)
        seasons_player_data = seasons_player_data.drop(columns='Sig_count')

        # ##### Last 5 Season Stats Plot Data
        plot_data = seasons_player_data[seasons_player_data['Statistics'] == stat_filter]
        seasons = list(seasons_player_data.columns[1:-1])
        plot_seasons = pd.pivot_table(plot_data, 
                                    values=seasons, 
                                    columns=[stat_filter]).reset_index(drop=False)
        plot_seasons.rename(columns={'Season Id':'Season'}, inplace=True)
        season_team = all_seasons_data.groupby('Season Id')['Team'].unique().reset_index(drop=False)
        season_team.rename(columns={'Season Id':'Season'}, inplace=True)
        plot_seasons = pd.merge(plot_seasons,
                                season_team,
                                on='Season')

        # ##### Find Min and Max Plot Values
        min_value = np.min(plot_seasons[stat_filter]) * 0.8
        if min_value < 10:
            min_value = 0
        max_value = np.max(plot_seasons[stat_filter]) * 1.1
        seasons_fig = px.bar(plot_seasons, 
                            x='Season', 
                            y=stat_filter, 
                            color="Season", 
                            color_discrete_map={
                                self.season_info.season_id.keys()[-5]: "#000000",
                                self.season_info.season_id.keys()[-4]: "#A0A0A0",
                                self.season_info.season_id.keys()[-3]: "#e5e5e6",
                                self.season_info.season_id.keys()[-2]: "#FFA0A0",
                                self.season_info.season_id.keys()[-1]: "#d20614"},
                            hover_name='Team',
                            height=400, 
                            text=stat_filter, 
                            text_auto='.2f', 
                            title=f"Last 5 Seasons {stat_filter} per Game")
        seasons_fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)"}, 
            yaxis_range=[min_value, max_value])
        
        # ##### No of Times in the last 5 season player played for Team
        player_team_season = plot_seasons['Team'].apply(lambda x: 1 if team in x else 0).sum()

        # ##### Insights Previous 5 Seasons
        insights_5_seasons = [plot_seasons.shape[0], 
                            plot_seasons.sort_values(by=stat_filter, ascending=False)['Season'].values[0],
                            player_team_season,
                            'Season' if player_team_season == 1 else 'Seasons']
            
        return seasons_player_data, seasons_fig, insight_season_comparison, insights_5_seasons
