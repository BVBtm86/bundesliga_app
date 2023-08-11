# import base64
# from pathlib import Path

# # ##### Create and resize image in st.markdown
# def img_to_bytes(img_path):
#     img_bytes = Path(img_path).read_bytes()
#     encoded = base64.b64encode(img_bytes).decode()
#     return encoded


# def img_to_html(img_path):
#     # img_html = "<img src='data:image/png;base64,{}' height='41.65' class='img-fluid'>".format(
#     img_html = "<img src='data:image/png;base64,{}' height='34.5' class='img-fluid'>".format(

#       img_to_bytes(img_path)
#     )
#     return img_html

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
