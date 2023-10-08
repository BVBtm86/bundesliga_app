import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from python_scripts.game_stats_app_scripts.game_stats_app_utils import config_previous_seasons, config_player_stats, config_teams_images, config_season_filter

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

def player_page(data:str,
                favourite_team:str,
                page_season:str) -> st:
    config = {'displayModeBar': False}

    # ##### Player Statistics Page Options
    st.sidebar.subheader("Options")

    # #### Select Player
    season_data = data.copy()
    team_players = list(set(season_data[(season_data['Team'] == favourite_team) & (season_data['Position'] != 'GK')]['Name'].unique()))
    team_players.sort()
    analysis_player = st.sidebar.selectbox(label='Select Player',
                                           options=team_players)

    # #### Player Statistics Type
    player_stats_options = ["Season", "Player vs Player", "Last 5 Seasons"]
    if config_previous_seasons.season_id.keys()[-1] != page_season:
        player_stats_options.remove("Last 5 Seasons")
    
    stats_type = st.sidebar.selectbox(label="Season Stats", 
                                      options=player_stats_options)
    
    # ##### Player Team Statistics
    if stats_type == "Season":

        # ##### Team Stat
        filter_stat = st.sidebar.selectbox(label="Select Stat", 
                                            options=config_player_stats.stats_player)
    
        # ##### Player Match Day Stats
        logo_col, player_day_stats_col = st.columns([0.5,10])
        with logo_col:
             st.image(config_teams_images['config_teams_logo'][favourite_team])
        with player_day_stats_col:
            st.markdown(f'<h4>{analysis_player}<font color = #d20614> {page_season}</font> Match Day Stats</h4>', unsafe_allow_html=True)

        match_day_fig = player_day_analysis(data=season_data, 
                                            team=favourite_team, 
                                            player=analysis_player,
                                            stat_name=filter_stat)
        
        if match_day_fig is not None:
            st.plotly_chart(match_day_fig, config=config, use_container_width=True)
        else:
            st.markdown(f'<b><font color = #d20614> {analysis_player} </font></b> has <b>0</b> {filter_stat} during the Season {page_season}', unsafe_allow_html=True)

        # ##### Player Season Filter Statistics
        season_player_stats = player_season_stats(data=season_data,
                            team=favourite_team,
                            player=analysis_player)
        st.markdown(f'<h4>{analysis_player} <font color = #d20614>{page_season}</font> Season Filter Stats</h4>', unsafe_allow_html=True)
        
        insights_col, type_chart_col = st.columns([2, 8])
        with type_chart_col:
            fig_type_player, period_venue, period_venue_1, period_venue_2, period_insights, \
                period_insights_1, period_insights_2 = player_season_filter(data_player_agg=season_player_stats, 
                                                                            player=analysis_player, 
                                                                            stat_name=filter_stat)
            if match_day_fig is not None:
                st.plotly_chart(fig_type_player, config=config, use_container_width=True)

                with insights_col:
                    st.title("")
                    if period_venue != "":
                        st.markdown(
                            f"<b><font color = #d20614>{analysis_player}</font></b> performs better at <b><font color = #d20614>"
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