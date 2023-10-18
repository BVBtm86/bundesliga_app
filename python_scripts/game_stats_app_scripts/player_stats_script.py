import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from scipy.stats import ttest_ind
from python_scripts.game_stats_app_scripts.game_stats_app_utils import config_previous_seasons, config_player_stats, config_teams_images, config_season_filter, config_comparison_stats, radar_plot

def player_day_analysis(data:pd.DataFrame, 
                        team:str, 
                        player:str,
                        stat_name:str) -> px:
    
    # ##### Create Aerial Duel Total Stat
    df_match_day = data[(data['Team'] == team) & (data['Name'] == player)].reset_index(drop=False)
    df_match_day['Aerial Duel'] = df_match_day['Aerial Duel Won'] + df_match_day['Aerial Duel Lost']

    # ##### Create Player Chart
    min_value = np.min(df_match_day[stat_name]) * 0.8
    if min_value < 10:
        min_value = 0
    max_value = np.max(df_match_day[stat_name]) * 1.1

    if df_match_day[stat_name].sum() > 0:
        match_day_fig = px.bar(df_match_day, 
                            x="Week_No", 
                            y=stat_name, 
                            color="Result", 
                            color_discrete_map={
                                'Win': "rgb(200,11,1)",
                                'Draw': "rgb(179, 179, 179)",
                                'Defeat': "rgb(78,78,80)"}, 
                            text=stat_name,
                            title=f"{player} {stat_name}")
        match_day_fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
        },
            xaxis1=dict(
                tickmode='array',
                tickvals=[i for i in range(1, len(df_match_day) + 1)],
                ticktext=df_match_day['Week_No'].unique(),
            ), 
            yaxis_range=[min_value, max_value]
        )
    else:
        match_day_fig = None

    return match_day_fig

st.cache_data
def player_season_stats(data:pd.DataFrame, 
                        team:str, 
                        player:str) -> pd.DataFrame:

    # # ##### Filter Data Based on Player
    player_season_data = data[(data['Team'] == team) & (data['Name'] == player)].reset_index(drop=False)

    # ##### Stats Aggregation based on Season Filter
    possible_season_filters = player_season_data[config_season_filter.season_filter].sum() > 0
    season_filters = player_season_data[config_season_filter.season_filter].sum()[possible_season_filters].index.to_list()

    # ##### Create Count Stats
    season_player_stats = []
    for filter in season_filters:
        season_player_stats.append(list(player_season_data[player_season_data[filter] == 1][config_player_stats.stats_count_calculations].mean().values))
    season_player_stats = pd.DataFrame(season_player_stats, columns=config_player_stats.stats_count_calculations, index=season_filters)
    season_player_stats['Aerial Duel'] = season_player_stats['Aerial Duel Won'] + season_player_stats['Aerial Duel Lost']

    # ##### Aggregate % Stats
    for stat in config_player_stats.stats_perc_calculations.keys():
        season_player_stats[stat] = season_player_stats[config_player_stats.stats_perc_calculations[stat][1]] / season_player_stats[
            config_player_stats.stats_perc_calculations[stat][0]] * 100

    # ##### Final Processing for Team Statistics
    season_player_stats.drop(columns=['Aerial Duel'], inplace=True)
    season_player_stats = season_player_stats.T
    season_player_stats = season_player_stats.reindex(config_player_stats.stats_player)
    season_player_stats = season_player_stats.reset_index(drop=False)
    season_player_stats.rename(columns={'index':'Stat'}, inplace=True)

    return season_player_stats

def player_season_filter(data_player_agg:pd.DataFrame, 
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

def comparison_all_stats(data:pd.DataFrame,
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
    season_players_data = players_season_data.groupby('Name')[config_player_stats.stats_count_calculations].mean().T

    # ##### Aggregate % Stats
    for stat in config_player_stats.stats_perc_calculations.keys():
        stat_perc = pd.DataFrame(players_season_data.groupby('Name')[config_player_stats.stats_perc_calculations[stat][1]].sum() / 
              players_season_data.groupby('Name')[config_player_stats.stats_perc_calculations[stat][0]].sum() * 100).T
        stat_perc.index = [stat]
        season_players_data = pd.concat([season_players_data, stat_perc])
    
    # ##### Merge Player Comparison Stats
    season_players_data = season_players_data.reindex(config_player_stats.stats_player)
    if team_player not in season_players_data.columns:
        season_players_data[team_player] = np.nan
    if opponent_player not in season_players_data.columns:
        season_players_data[opponent_player] = np.nan

    # ##### Calculate Significance Level
    sig_comparison_test = []
    for stat in config_player_stats.stats_player:
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

def player_stats_comparison(data:pd.DataFrame,
                            team:str,
                            team_player:str,
                            opponent:str,
                            opponent_player:str,
                            filter_stats:str,
                            filter_season:str):
    
    season_data = data.copy()
    season_data['Aerial Duel'] = season_data['Aerial Duel Won'] + season_data['Aerial Duel Lost']

    # ##### Stats Filter
    comparison_stats = config_comparison_stats.player_stats_list[filter_stats]

    # ##### Team Player Statistics
    team_player_data = season_data[(season_data['Team'] == team) & 
                                   (season_data['Name'] == team_player) & 
                                   (season_data[filter_season] == 1)].reset_index()
    team_player_stats = []
    for stat in comparison_stats:
        if stat in config_player_stats.stats_count_calculations:
            team_player_stats.append(team_player_data[stat].mean())
        else:
            team_player_stats.append(team_player_data[config_player_stats.stats_perc_calculations[stat][1]].sum() / team_player_data[
                config_player_stats.stats_perc_calculations[stat][0]].sum() * 100)

    # ##### Opponent Player Statistics
    opponent_player_data = season_data[(season_data['Team'] == opponent) & 
                                       (season_data['Name'] == opponent_player) & 
                                       (season_data[filter_season] == 1)].reset_index()    
    opponent_player_stats = []
    for stat in comparison_stats:
        if stat in config_player_stats.stats_count_calculations:
            opponent_player_stats.append(opponent_player_data[stat].mean())
        else:
            opponent_player_stats.append(opponent_player_data[config_player_stats.stats_perc_calculations[stat][1]].sum() / opponent_player_data[
                config_player_stats.stats_perc_calculations[stat][0]].sum() * 100)

    # ##### Radar Ranges
    min_stats = []
    max_stats = []
    for stat in comparison_stats:
        min_stats.append(season_data[stat].min())
        max_stats.append(season_data[stat].max())
        
    # ##### Player Radar Plot
    team_player_plot = radar_plot(stats=team_player_stats,
                                  comparison_stats=comparison_stats,
                                  min_stats=min_stats,
                                  max_stats=max_stats,
                                  radar_name=True,
                                  player_name=team_player)
    
    # ##### Opponent Radar Plot
    opponent_player_plot = radar_plot(stats=opponent_player_stats,
                                      comparison_stats=comparison_stats,
                                      min_stats=min_stats,
                                      max_stats=max_stats,
                                      radar_name=True,
                                      player_name=opponent_player)
    
    # # ##### All Stats Comparison
    stats_comparison, comparison_insights = comparison_all_stats(data=season_data,
                                                                 team=team,
                                                                 team_player=team_player,
                                                                 opponent=opponent,
                                                                 opponent_player=opponent_player,
                                                                 filter_season=filter_season)
    
    return team_player_plot, opponent_player_plot, stats_comparison, comparison_insights

def player_page(data:str,
                favourite_team:str,
                page_season:str,
                season_teams:list) -> st:
    
    config = {'displayModeBar': False}

    # ##### Player Statistics Page Options
    st.sidebar.subheader("Options")

    # #### Select Player
    season_data = data.copy()
    team_players = list(set(season_data[(season_data['Team'] == favourite_team) & (season_data['Position'] != 'GK')]['Name'].unique()))
    team_players.sort()
    team_player_analysis = st.sidebar.selectbox(label='Player', 
                                                options=team_players)

    # #### Player Statistics Type
    player_stats_options = ["Season", "Player vs Player", "Last 5 Seasons"]
    if config_previous_seasons.season_id.keys()[-1] != page_season:
        player_stats_options.remove("Last 5 Seasons")
    
    stats_type = st.sidebar.selectbox(label="Stats", 
                                      options=player_stats_options)
    
    # ##### Select Season Filter
    possible_season_filters = season_data[season_data['Team'] == favourite_team][config_season_filter.season_filter].sum() > 0
    season_filters = season_data[season_data['Team'] == favourite_team][config_season_filter.season_filter].sum()[possible_season_filters].index.to_list().copy()
    if stats_type == 'Player vs Player':
        filter_season = st.sidebar.selectbox(label="Season Filter", 
                                             options=season_filters)
    elif stats_type == 'Last 5 Seasons':
        season_filters.remove("Form")
        filter_season = st.sidebar.selectbox(label="Season Filter", 
                                             options=season_filters)
    
    # ##### Player Team Statistics
    if stats_type == "Season":

        # ##### Team Stat
        filter_stat = st.sidebar.selectbox(label="Game Stat", 
                                            options=config_player_stats.stats_player)
    
        # ##### Player Match Day Stats
        logo_col, player_day_stats_col = st.columns([0.5,10])
        with logo_col:
             st.image(config_teams_images['config_teams_logo'][favourite_team])
        with player_day_stats_col:
            st.markdown(f'<h4>{team_player_analysis}<font color = #d20614> {page_season}</font> Match Day Stats</h4>', unsafe_allow_html=True)

        match_day_fig = player_day_analysis(data=season_data, 
                                            team=favourite_team, 
                                            player=team_player_analysis,
                                            stat_name=filter_stat)
        
        if match_day_fig is not None:
            st.plotly_chart(match_day_fig, config=config, use_container_width=True)
        else:
            st.markdown(f'<b><font color = #d20614> {team_player_analysis} </font></b> has <b>0</b> {filter_stat} during the Season {page_season}', unsafe_allow_html=True)

        # ##### Player Season Filter Statistics
        season_player_stats = player_season_stats(data=season_data, 
                                                  team=favourite_team, 
                                                  player=team_player_analysis)
        st.markdown(f'<h4>{team_player_analysis} <font color = #d20614>{page_season}</font> Season Filter Stats</h4>', unsafe_allow_html=True)
        
        insights_col, type_chart_col = st.columns([2, 8])
        with type_chart_col:
            fig_type_player, period_venue, period_venue_1, period_venue_2, period_insights, \
                period_insights_1, period_insights_2 = player_season_filter(data_player_agg=season_player_stats, 
                                                                            player=team_player_analysis, 
                                                                            stat_name=filter_stat)
            if match_day_fig is not None:
                st.plotly_chart(fig_type_player, config=config, use_container_width=True)

                with insights_col:
                    st.title("")
                    if period_venue != "":
                        st.markdown(
                            f"<b><font color = #d20614>{team_player_analysis}</font></b> performs better at <b><font color = #d20614>"
                            f"{period_venue[0]}</font></b> games with <b><font color = #d20614>{period_venue_1:.2f}</font></b> <b>"
                            f"<font color = #43C673>{filter_stat}</font></b> per game on average in comparison to <b><font color = "
                            f"#d20614>{period_venue[1]}</font></b> games where he had <b><font color = #d20614>{period_venue_2:.2f}"
                            f"</font></b> <b><font color = #43C673>{filter_stat}</font></b> per game on average.",
                            unsafe_allow_html=True)

                    if period_insights != "":
                        st.markdown(
                            f"He also performs better in the <b><font color = #d20614>{period_insights[0]}</font></b> of the "
                            f"Season with <b><font color = #d20614>{period_insights_1:.2f}</font></b> <b><font color = #43C673>"
                            f"{filter_stat}</font></b> per game on average in comparison to the <b><font color = #d20614>"
                            f"{period_insights[1]}</font></b> of the Season where he had <b><font color = #d20614>"
                            f"{period_insights_2:.2f}</font></b> <b><font color = #43C673>{filter_stat}</font></b> per game on average.",
                            unsafe_allow_html=True)

        pos_stat = config_player_stats.stats_player.index(filter_stat)
        st.dataframe(season_player_stats.style.format({stat: '{:.2f}' for stat in config_season_filter.season_filter}).apply(lambda x: [
            'background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
            lambda x: ['color: #d20614' if i == pos_stat else 'color: #000000' for i in range(len(x))], axis=0), 
                        use_container_width=True, 
                        hide_index=True,
                        column_config={
                        "Stat": st.column_config.Column(
                            width="medium")})

    # ##### Season Player vs Player Statistics
    elif stats_type == "Player vs Player":
        
        # ##### Select Opponent
        opponent_team = st.sidebar.selectbox(label="Opponent Team", 
                                             options=season_teams,
                                             index=season_teams.index(favourite_team))
        opponent_players = list(set(season_data[(season_data['Team'] == opponent_team) & (season_data['Position'] != 'GK')]['Name'].unique()))
        opponent_players.sort()
        if team_player_analysis in opponent_players:
            opponent_players.remove(team_player_analysis)
        opponent_players_analysis = st.sidebar.selectbox(label='Opponent Player', 
                                                        options=opponent_players)
        
        # ##### Select Statistics
        filter_stats = st.sidebar.selectbox(label="Statistics", 
                                            options=config_comparison_stats.player_stats_name)

        team_player_radar, opponent_player_radar, stat_comparison, comparison_insight = player_stats_comparison(data=season_data, 
                                                                                                                team=favourite_team,
                                                                                                                team_player=team_player_analysis,
                                                                                                                opponent=opponent_team,
                                                                                                                opponent_player=opponent_players_analysis,
                                                                                                                filter_stats=filter_stats,
                                                                                                                filter_season=filter_season)
        
        # ##### Player vs Opponent Stats Type Comparison
        st.markdown(f'<h4><font color = #d20614>{team_player_analysis}</font> vs {opponent_players_analysis} <font color = #d20614>{filter_season}</font> '
                    f'Statistics - <font color = #d20614>{page_season}</font></h4>', unsafe_allow_html=True)
        
        _, team_img_col, _, opp_img_col, _ = st.columns([1.75,2,2.35,2,0.55])
        with team_img_col:
            st.image(config_teams_images['config_teams_logo'][favourite_team], width=100)

        with opp_img_col:
            st.image(config_teams_images['config_teams_logo'][opponent_team], width=100)

        team_col, opponent_col = st.columns([3,3])
        with team_col:
            st.pyplot(team_player_radar)

        with opponent_col:
            st.pyplot(opponent_player_radar)

        st.dataframe(data=stat_comparison.style.format({stat: '{:.2f}' for stat in [team_player_analysis, opponent_players_analysis]}).apply(lambda x: [
                'background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0),
                     use_container_width=True,
                     hide_index=True,
                    column_config={
                    "Statistics": st.column_config.Column(
                        width="large",
                    ),
                    f"{team_player_analysis}": st.column_config.Column(
                        width="medium",
                    ),
                    f"{opponent_players_analysis}": st.column_config.Column(
                        width="medium",
                    ),
                    "Sig": st.column_config.Column(
                        width="small"
                    ),
                    })
        st.markdown(f"<b><font color = #d20614>{team_player_analysis}</font></b> has <b><font color = #d20614>{comparison_insight[0]}</font></b> "
                    f"<b>Significant Higher</b> game average stats then <b><font color = #d20614>{opponent_players_analysis}</font></b> for <b><font color = #d20614>"
                    f"{filter_season}</font></b> Games and <b><font color = #d20614>{comparison_insight[1]}</font></b> <b>Significant Lower</b> game average stats", 
                    unsafe_allow_html=True)
