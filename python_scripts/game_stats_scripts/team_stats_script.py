import pandas as pd
import numpy as np
import streamlit as st
import streamlit as st
import plotly.express as px
from scipy.stats import ttest_ind
from mplsoccer import Radar, grid
import matplotlib.pyplot as plt
from python_scripts.game_stats_scripts.game_stats_utils import config_teams_images, config_previous_seasons, config_season_filter, config_importance_stats, config_team_stats, filter_season_data, style_metric_cards, config_comparison_stats, radar_mosaic
import warnings

#suppress warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

def most_important_stats(data:pd.DataFrame, 
                         data_all:pd.DataFrame, 
                         current_season:str, 
                         previous_seasons:dict, 
                         team:str) -> tuple[list, 
                                            list]:

    season_data = data.copy()
    # ##### Current Season Avg Stats
    season_important_stats = list(season_data[season_data['Team'] == team][config_importance_stats.team_important_stats[:4]].mean().round(2).values)

    # ##### Current Season Sum Stats
    season_data['Win'] = np.where(season_data['Result'] == 'Win', 1, 0)
    season_data['Draw'] = np.where(season_data['Result'] == 'Draw', 1, 0)
    season_important_stats.append((season_data[season_data['Team'] == team]['Win'] * 3 + season_data[season_data['Team'] == team]['Draw']).sum())
    season_important_stats.append(season_data[season_data['Team'] == team][config_importance_stats.team_important_stats[4]].sum())
    season_important_stats.append(season_data[season_data['Team'] == team][config_importance_stats.team_important_stats[5]].sum())
    current_season_match_day = season_data['Week_No'].max()

    # ##### Last Season Stats
    season_previous = previous_seasons[current_season]
    previous_data_season = data_all[(data_all['Season Id'] == season_previous) & (data_all['Week_No'] <= current_season_match_day)].reset_index(drop=True)
    if previous_data_season.shape[0] > 0:
        previous_season_important_stats = list(previous_data_season[previous_data_season['Team'] == team][config_importance_stats.team_important_stats[:4]].mean().round(2).values)
        previous_data_season['Win'] = np.where(previous_data_season['Result'] == 'Win', 1, 0)
        previous_data_season['Draw'] = np.where(previous_data_season['Result'] == 'Draw', 1, 0)
        previous_season_important_stats.append((previous_data_season[previous_data_season['Team'] == team]['Win'] * 3 + previous_data_season[previous_data_season['Team'] == team]['Draw']).sum())
        previous_season_important_stats.append(previous_data_season[previous_data_season['Team'] == team][config_importance_stats.team_important_stats[4]].sum())
        previous_season_important_stats.append(previous_data_season[previous_data_season['Team'] == team][config_importance_stats.team_important_stats[5]].sum())
        diff_important_stats = list(pd.Series(season_important_stats) - pd.Series(previous_season_important_stats))
        diff_important_stats[:4] = np.round(diff_important_stats[:4],2)
    else:
        diff_important_stats = ["", "", "", "", "", "", ""]

    return season_important_stats, diff_important_stats

def teams_day_analysis(data:pd.DataFrame, 
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
    df_team['Game'] = df_team['Week_No']
    df_opp['Game'] = df_opp['Week_No']
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
        if stat_name in config_team_stats.stats_perc_calculations.keys():
            stats_agg = config_team_stats.stats_perc_calculations[stat_name]
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

st.cache_data
def team_season_stats(data:pd.DataFrame, 
                      team:str) -> tuple[pd.DataFrame, 
                                         pd.DataFrame]:

    team_season_data = data.copy()

    # ##### Filter Data Based on Team
    team_data_stats = team_season_data[team_season_data['Team'] == team].reset_index(drop=True)
    opponent_data_stats = team_season_data[team_season_data['Opponent'] == team].reset_index(drop=True)

    # ##### Stats Aggregation based on Season Filter
    possible_season_filters = pd.concat([team_data_stats, opponent_data_stats])[config_season_filter.season_filter].sum() > 0
    season_filters = pd.concat([team_data_stats, opponent_data_stats])[config_season_filter.season_filter].sum()[possible_season_filters].index.to_list()

    # ##### Create Team / Opponent Count Stats
    season_team_stats = []
    season_opponent_stats = []
    for filter in season_filters:
        season_team_stats.append(list(team_data_stats[team_data_stats[filter] == 1][config_team_stats.stats_count_calculations].mean().values))
        season_opponent_stats.append(list(opponent_data_stats[opponent_data_stats[filter] == 1][config_team_stats.stats_count_calculations].mean().values))
    season_team_stats = pd.DataFrame(season_team_stats, columns=config_team_stats.stats_count_calculations, index=season_filters)
    season_opponent_stats = pd.DataFrame(season_opponent_stats, columns=config_team_stats.stats_count_calculations, index=season_filters)
    season_team_stats['Aerial Duel'] = season_team_stats['Aerial Duel Won'] + season_team_stats['Aerial Duel Lost']
    season_opponent_stats['Aerial Duel'] = season_opponent_stats['Aerial Duel Won'] + season_opponent_stats['Aerial Duel Lost']

    # ##### Aggregate % Stats
    for stat in config_team_stats.stats_perc_calculations.keys():
        season_team_stats[stat] = season_team_stats[config_team_stats.stats_perc_calculations[stat][1]] / season_team_stats[
            config_team_stats.stats_perc_calculations[stat][0]] * 100
        season_opponent_stats[stat] = season_opponent_stats[config_team_stats.stats_perc_calculations[stat][1]] / season_opponent_stats[
            config_team_stats.stats_perc_calculations[stat][0]] * 100

    # ##### Final Processing for Team Statistics
    season_team_stats.drop(columns=['Aerial Duel'], inplace=True)
    season_team_stats = season_team_stats.T
    season_team_stats = season_team_stats.reindex(config_team_stats.stats_team)
    season_team_stats = season_team_stats.reset_index(drop=False)
    season_team_stats.rename(columns={'index':'Stat'}, inplace=True)

    # ##### Final Processing for Opponent Statistics
    season_opponent_stats.drop(columns=['Aerial Duel'], inplace=True)
    season_opponent_stats = season_opponent_stats.T
    season_opponent_stats = season_opponent_stats.reindex(config_team_stats.stats_team)
    season_opponent_stats = season_opponent_stats.reset_index(drop=False)
    season_opponent_stats.rename(columns={'index':'Stat'}, inplace=True)

    return season_team_stats, season_opponent_stats

def team_season_filter(data_team_agg:pd.DataFrame, 
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

def last_games_results(data:pd.DataFrame,
                       team_opponent:str,
                       season_filter:str) -> pd.DataFrame:
    seasons_data = data.copy()
    # ##### Filter Only Team and Opponent Games
    games_opponent = seasons_data[(seasons_data['Opponent'] == team_opponent) & 
                                  (seasons_data['Season Id'] <= config_previous_seasons.season_id[season_filter] + 1)].sort_values(by=['Season Id', 'Week_No'], ascending=[False, False])

    # ##### Get Last 5 Games Played
    last_5_games_df = games_opponent.iloc[:5,:][['Season Id', 'Week_No', 'Venue', 'Team', 'Opponent', 'Goals', 'Goals Ag']]

    # ##### Create Last 5 Games
    change_opponent = last_5_games_df.loc[last_5_games_df['Venue'] == 'Away',['Opponent','Team']]
    last_5_games_df.loc[last_5_games_df['Venue'] == 'Away','Team'] = change_opponent['Opponent']
    last_5_games_df.loc[last_5_games_df['Venue'] == 'Away','Opponent'] = change_opponent['Team']
    change_goals = last_5_games_df.loc[last_5_games_df['Venue'] == 'Away',['Goals','Goals Ag']]
    last_5_games_df.loc[last_5_games_df['Venue'] == 'Away', 'Goals'] = change_goals['Goals Ag']
    last_5_games_df.loc[last_5_games_df['Venue'] == 'Away', 'Goals Ag'] = change_goals['Goals']
    last_5_games_df['Result'] = last_5_games_df['Goals'].astype(str) + '-' + last_5_games_df['Goals Ag'].astype(str)
    last_5_games_df = last_5_games_df[['Season Id', 'Week_No', 'Team', 'Result', 'Opponent']]
    last_5_games_df['Season Id'] = last_5_games_df['Season Id'].map(dict((int(value+1), key) for key, value in config_previous_seasons.season_id.items()))

    last_5_games_df.rename(columns={'Season Id':'Season', 'Week_No':'Week No', 'Team':'Home Team', 'Opponent':'Away Team'}, inplace=True)
    
    return last_5_games_df

def radar_plot(stats:list,
               comparison_stats:list,
               min_stats:list,
               max_stats:list) -> plt:
    
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
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#e5e5e6', edgecolor='#ffffff')
    radar_output = radar.draw_radar(stats, ax=axs['radar'],
                                    kwargs_radar={'facecolor': '#d20614', 'alpha': 0.25},
                                    kwargs_rings={'facecolor': '#ffffff', 'alpha': 0.25})

    radar_poly, rings_outer, vertices = radar_output
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=10, color='#000000', font="Sans serif")
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=12.5, color='#000000', font="Sans serif")
    axs['radar'].scatter(vertices[:, 0], vertices[:, 1],  c='#d20614', edgecolors='#000000', marker='o', s=100)

    return radar_fig

def comparison_all_stats(data:pd.DataFrame,
                         team:str,
                         opponent:str,
                         filter_season:str) -> pd.DataFrame:

    season_data = data.copy()
    team_season_data = season_data[(season_data['Team'].isin([team, opponent])) & (season_data[filter_season] == 1)].copy()

    # ##### Aggregate Team Count Stats
    season_team_data = team_season_data.groupby('Team')[config_team_stats.stats_count_calculations].mean().T

    # ##### Aggregate % Stats
    for stat in config_team_stats.stats_perc_calculations.keys():
        stat_perc = pd.DataFrame(team_season_data.groupby('Team')[config_team_stats.stats_perc_calculations[stat][1]].sum() / 
              team_season_data.groupby('Team')[config_team_stats.stats_perc_calculations[stat][0]].sum() * 100).T
        stat_perc.index = [stat]
        season_team_data = pd.concat([season_team_data, stat_perc])
    
    # ##### Merge Team Comparison Stats
    season_team_data = season_team_data.reindex(config_team_stats.stats_team)
    if team not in season_team_data.columns:
        season_team_data[team] = np.nan
    if opponent not in season_team_data.columns:
        season_team_data[opponent] = np.nan

    # ##### Calculate Significance Level
    sig_comparison_test = []
    for stat in config_team_stats.stats_team:
        sig_comparison_test.append(ttest_ind(a=team_season_data[team_season_data['Team'] == team][stat].values, 
                                              b=team_season_data[team_season_data['Team'] == opponent][stat].values, equal_var=True).pvalue)
    season_team_data['Sig'] = sig_comparison_test
    season_team_data['Sig'] = season_team_data.apply(lambda x: "🟢" if x['Sig'] <=0.05 and x[team] > x[opponent] else (
        "🔴" if x['Sig'] <=0.05 and x[team] < x[opponent] else np.nan), axis=1)
        
    season_team_data = season_team_data[[team, opponent, "Sig"]].reset_index(drop=False)
    season_team_data.rename(columns={"index": "Statistics"}, inplace=True)

    # ##### Insight Significance Level
    insight_df = season_team_data['Sig'].value_counts().reset_index(drop=False)
    insight_data = []
    try: 
        insight_data.append(insight_df[insight_df['Sig'] == "🟢"]['count'].values[0]),
    except:
        insight_data.append(0)
    try: 
        insight_data.append(insight_df[insight_df['Sig'] == "🔴"]['count'].values[0]),
    except:
        insight_data.append(0)

    return season_team_data, insight_data

def team_stats_comparison(data:pd.DataFrame,
                          team:str,
                          opponent:str,
                          filter_stats:str,
                          filter_season:str):
    
    season_data = data.copy()
    season_data['Aerial Duel'] = season_data['Aerial Duel Won'] + season_data['Aerial Duel Lost']

    # ##### Stats Filter
    comparison_stats = config_comparison_stats.stats_list[filter_stats]

    # ##### Team Statistics
    team_data = season_data[(season_data['Team'] == team) & (season_data[filter_season] == 1)].reset_index()
    season_team_stats = []
    for stat in comparison_stats:
        if stat in config_team_stats.stats_count_calculations:
            season_team_stats.append(team_data[stat].mean())
        else:
            season_team_stats.append(team_data[config_team_stats.stats_perc_calculations[stat][1]].sum() / team_data[
                config_team_stats.stats_perc_calculations[stat][0]].sum() * 100)

    # ##### Opponent Data
    opponent_data = season_data[(season_data['Team'] == opponent) & (season_data[filter_season] == 1)].reset_index()
    season_opponent_stats = []
    for stat in comparison_stats:
        if stat in config_team_stats.stats_count_calculations:
            season_opponent_stats.append(opponent_data[stat].mean())
        else:
            season_opponent_stats.append(opponent_data[config_team_stats.stats_perc_calculations[stat][1]].sum() / opponent_data[
                config_team_stats.stats_perc_calculations[stat][0]].sum() * 100)

    # ##### Radar Ranges
    min_stats = []
    max_stats = []
    for stat in comparison_stats:
        min_stats.append(season_data[stat].min())
        max_stats.append(season_data[stat].max())
        
    # ##### Team Radar Plot
    team_plot = radar_plot(stats=season_team_stats,
                           comparison_stats=comparison_stats,
                           min_stats=min_stats,
                           max_stats=max_stats)
    
    # ##### Team Radar Plot
    opponent_plot = radar_plot(stats=season_opponent_stats,
                           comparison_stats=comparison_stats,
                           min_stats=min_stats,
                           max_stats=max_stats)
    
    # ##### All Stats Comparison
    stats_comparison, comparison_insights = comparison_all_stats(data=season_data, 
                                                                 team=team, 
                                                                 opponent=opponent,
                                                                 filter_season=filter_season)
    
    return team_plot, opponent_plot, stats_comparison, comparison_insights

def team_last_seasons_stats(data:pd.DataFrame,
                           season_filter:str,
                           stat_filter:str,
                           team:str):

    all_seasons_data = data.copy()
    all_seasons_data['Aerial Duel'] = all_seasons_data['Aerial Duel Won'] + all_seasons_data['Aerial Duel Lost']

    # ##### Filter Data by Season Filter
    all_seasons_data = all_seasons_data[all_seasons_data[season_filter] == 1].reset_index(drop=True)
    
    # ##### Map Season Id
    all_seasons_data['Season Id'] = all_seasons_data['Season Id'].map(dict((value + 1, key) for key, value in config_previous_seasons.season_id.items()))
    
    # ##### Create Team Count Stats
    seasons_team_data = all_seasons_data.groupby('Season Id')[config_team_stats.stats_count_calculations].mean().T

    # ##### Aggregate % Stats
    for stat in config_team_stats.stats_perc_calculations.keys():
        stat_perc = pd.DataFrame(all_seasons_data.groupby('Season Id')[config_team_stats.stats_perc_calculations[stat][1]].sum() / 
                                 all_seasons_data.groupby('Season Id')[config_team_stats.stats_perc_calculations[stat][0]].sum() * 100).T
        stat_perc.index = [stat]
        seasons_team_data = pd.concat([seasons_team_data, stat_perc])

    # ##### Calculate Significance Level
    sig_comparison_test = []
    for stat in config_team_stats.stats_team:
        sig_comparison_test.append(ttest_ind(a=all_seasons_data[all_seasons_data['Season Id'] == config_previous_seasons.season_id.keys()[-1]][stat].values, 
                                             b=all_seasons_data[all_seasons_data['Season Id'] == config_previous_seasons.season_id.keys()[-2]][stat].values, equal_var=True).pvalue)
    seasons_team_data['Sig'] = sig_comparison_test
    seasons_team_data['Sig'] = seasons_team_data.apply(
        lambda x: "🟢" if x['Sig'] <=0.05 and x[config_previous_seasons.season_id.keys()[-1]] > 
        x[config_previous_seasons.season_id.keys()[-2]] else (
        "🔴" if x['Sig'] <=0.05 and x[config_previous_seasons.season_id.keys()[-1]] < x[config_previous_seasons.season_id.keys()[-2]] else np.nan), axis=1)
    seasons_team_data.reset_index(drop=False, inplace=True)
    seasons_team_data.rename(columns = {'index':'Statistics'}, inplace=True)

    # ##### Plot Min and Max Values
    min_value = np.min(all_seasons_data[stat_filter]) * 0.8
    if min_value < 10:
        min_value = 0
    max_value = np.max(all_seasons_data[stat_filter]) * 1.1

    # ##### Plot Data
    plot_data = seasons_team_data[seasons_team_data['Statistics'] == stat_filter]
    seasons = list(seasons_team_data.columns[1:-1])
    plot_seasons = pd.pivot_table(plot_data, 
                                  values=seasons, 
                                  columns=[stat_filter]).reset_index(drop=False)
    plot_seasons.rename(columns={'Season Id':'Season'}, inplace=True)
    seasons_fig = px.bar(plot_seasons, 
                         x='Season', 
                         y=stat_filter, 
                         color="Season", 
                         color_discrete_map={
                             config_previous_seasons.season_id.keys()[-5]: "#000000",
                             config_previous_seasons.season_id.keys()[-4]: "#A0A0A0",
                             config_previous_seasons.season_id.keys()[-3]: "#e5e5e6",
                             config_previous_seasons.season_id.keys()[-2]: "#FFA0A0",
                             config_previous_seasons.season_id.keys()[-1]: "#d20614"},
                         height=400, 
                         text=stat_filter, 
                         text_auto='.2f', 
                         title=f"{team} Last 5 Seasons {stat_filter} per Game")
    seasons_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"}, 
        yaxis_range=[min_value, max_value])
    
    return seasons_team_data, seasons_fig


def team_page(data:pd.DataFrame, 
              data_all:pd.DataFrame, 
              page_season:str, 
              favourite_team:str,
              season_teams:list) -> st:
    config = {'displayModeBar': False}

    # #### Team Statistics Type
    stats_type = st.sidebar.selectbox(label="Season Stats", 
                                      options=["Season", "Team vs Team", "Last 5 Seasons"])

    # ##### Select Season Filter
    possible_season_filters = data[data['Team'] == favourite_team][config_season_filter.season_filter].sum() > 0
    season_filters = data[data['Team'] == favourite_team][config_season_filter.season_filter].sum()[possible_season_filters].index.to_list().copy()
    if stats_type == 'Last 5 Seasons':
        season_filters.remove("Form")
        filter_season = st.sidebar.selectbox(label="Season Filter", 
                                                options=season_filters)
    else:
        filter_season = st.sidebar.selectbox(label="Season Filter", 
                                                options=season_filters)

    # ##### Season Team Statistics
    if stats_type == "Season":

        # ##### Team Stat
        filter_stat = st.sidebar.selectbox(label="Select Stat", 
                                            options=config_team_stats.stats_team)

        # ##### Extract Most Important Season Stats and comparison to last years stats
        season_important_stats, diff_important_stats = most_important_stats(data=data, 
                                                                            data_all=data_all,
                                                                            current_season=page_season,
                                                                            previous_seasons=config_previous_seasons.season_id,
                                                                            team=favourite_team)

        # ##### Most Important Season Stats
        st.markdown(f'<h4>{favourite_team}</b> <b><font color = #d20614>{page_season}</font> Season Stats</h4>', unsafe_allow_html=True)
        logo_col, metric_col_1, metric_col_2, metric_col_3, metric_col_4, metric_col_5, metric_col_6, metric_col_7  = st.columns([1,1.25,1.25,1.25,1.25,1.25,1.25, 1.25])
        with logo_col:
             st.image(config_teams_images['config_teams_logo'][favourite_team])

        metric_col_1.metric(label="Goals", value=f"{season_important_stats[5]}", delta=f"{diff_important_stats[5]}")
        metric_col_2.metric(label="Goals Ag", value=f"{season_important_stats[6]}", delta=f"{diff_important_stats[6]}", delta_color="inverse")
        metric_col_3.metric(label='xG', value=f"{season_important_stats[0]}", delta=f"{diff_important_stats[0]}")
        metric_col_4.metric(label="Possession", value=f"{season_important_stats[1]}%", delta=f"{diff_important_stats[1]}")
        metric_col_5.metric(label="Distance Covered", value=f"{season_important_stats[2]}", delta=f"{diff_important_stats[2]}")
        metric_col_6.metric(label="Shots", value=f"{season_important_stats[3]}", delta=f"{diff_important_stats[3]}")
        metric_col_7.metric(label="Points", value=f"{season_important_stats[4]}", delta=f"{diff_important_stats[4]}")
        style_metric_cards()

        if diff_important_stats[0] != "":
            st.markdown(
                f"<b>Note:</b> <b><font color = #43C673>{page_season}</font></b> vs <b><font color = #d20614> "
                f"{config_previous_seasons.season_comparison[page_season]}</font></b> Season comparison", unsafe_allow_html=True)

        # ##### Team Match Day Stats
        st.markdown(f'<h4>{favourite_team}</b> <b><font color = #d20614>{page_season}</font> Match Day Stats</h4>', unsafe_allow_html=True)

        match_day_fig, avg_team, avg_opp, better, stat_sig_name = teams_day_analysis(data=data, 
                                                                                     team=favourite_team, 
                                                                                     stat_name=filter_stat)
        if match_day_fig is not None:
            st.plotly_chart(match_day_fig, config=config, use_container_width=True)
            # ##### Match Day Insights
            if stat_sig_name == "":
                st.markdown(
                    f"In <b><font color = #d20614>{better}%</font></b> of the <b><font color = #d20614>{page_season}"
                    f"</font></b> Season games {favourite_team} had more <b><font color = #43C673>{filter_stat}</font></b> "
                    f"then her opponent. {favourite_team} had an average of <b><font color = #d20614>{avg_team}</font></b> "
                    f"<b><font color = #43C673>{filter_stat}</font></b> per game while her opponents had an average of "
                    f"<b><font color = #d20614>{avg_opp}</font></b> <b><font color = #43C673>{filter_stat}</font></b> per "
                    f"game.", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"In <b><font color = #d20614>{better}%</font></b> of the <b><font color = #d20614>{page_season}"
                    f"</font></b> Season games {favourite_team} had more <b><font color = #43C673>{filter_stat}</font></b> then"
                    f" her opponent. {favourite_team} had an average of <b><font color = #d20614>{avg_team}</font></b> <b>"
                    f"<font color = #43C673>{filter_stat}</font></b> per game while her opponents had an average of "
                    f"<b><font color = #d20614>{avg_opp}</font></b> <b><font color = #43C673>{filter_stat}</font></b> per "
                    f"game, which is <b><font color = #d20614>{stat_sig_name}</font></b>.", unsafe_allow_html=True)

        else:
            st.markdown(f'<h6><font color = #d20614>{favourite_team}</font> has 0 <font color = #d20614>{filter_stat}</font></h4>', unsafe_allow_html=True)

        # ##### Team Season Filter Statistics
        season_team_stats, season_opponent_stats = team_season_stats(data=data,
                                                                     team=favourite_team)
        st.markdown(f'<h4>{favourite_team}</b> <b><font color = #d20614>{page_season}</font> Season Filter Stats</h4>', unsafe_allow_html=True)
    
        insights_col, type_chart_col = st.columns([2, 8])
        with type_chart_col:
            fig_type_team, period_venue, period_venue_1, period_venue_2, period_insights, \
                period_insights_1, period_insights_2 = team_season_filter(data_team_agg=season_team_stats, 
                                                                          data_opp_agg=season_opponent_stats, 
                                                                          team=favourite_team, 
                                                                          stat_name=filter_stat)
            if match_day_fig is not None:
                st.plotly_chart(fig_type_team, config=config, use_container_width=True)

        with insights_col:
            st.title("")
            if period_venue != "":
                st.markdown(
                    f"<b><font color = #d20614>{favourite_team}</font></b> performs better at <b><font color = #d20614>"
                    f"{period_venue[0]}</font></b> games with <b><font color = #d20614>{period_venue_1:.2f}</font></b> <b>"
                    f"<font color = #43C673>{filter_stat}</font></b> per game on average in comparison to <b><font color = "
                    f"#d20614>{period_venue[1]}</font></b> games where they had  <b><font color = #d20614>{period_venue_2:.2f}"
                    f"</font></b> <b><font color = #43C673>{filter_stat}</font></b> per game on average.",
                    unsafe_allow_html=True)

            if period_insights != "":
                st.markdown(
                    f"It also performs better in the <b><font color = #d20614>{period_insights[0]}</font></b> of the "
                    f"Season with <b><font color = #d20614>{period_insights_1:.2f}</font></b> <b><font color = #43C673>"
                    f"{filter_stat}</font></b> per game on average in comparison to the <b><font color = #d20614>"
                    f"{period_insights[1]}</font></b> of the Season where they had  <b><font color = #d20614>"
                    f"{period_insights_2:.2f}</font></b> <b><font color = #43C673>{filter_stat}</font></b> per game on average.",
                    unsafe_allow_html=True)
        
        # ##### Show Team or Opponent Stats
        col_show_team, _ = st.columns([2,6])
        with col_show_team:
            show_team = st.selectbox(label="Show",
                                    options=[f"{favourite_team} Stats", "Opponents Stats"])
        
        pos_stat = season_team_stats[season_team_stats['Stat'] == filter_stat].index.values[0]
        if show_team == f"{favourite_team} Stats":
            st.dataframe(season_team_stats.style.format({stat: '{:.2f}' for stat in config_season_filter.season_filter}).apply(lambda x: [
                'background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
                lambda x: ['color: #d20614' if i == pos_stat else 'color: #000000' for i in range(len(x))], axis=0), 
                            use_container_width=True, 
                            hide_index=True,
                            column_config={
                            "Stat": st.column_config.Column(
                                width="medium")})
        else:
            st.dataframe(data=season_opponent_stats.style.format({stat: '{:.2f}' for stat in config_season_filter.season_filter}).apply(lambda x: [
                'background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
                lambda x: ['color: #d20614' if i == pos_stat else 'color: #000000' for i in range(len(x))], axis=0), 
                            use_container_width=True, 
                            hide_index=True,
                            column_config={
                            "Stat": st.column_config.Column(
                                width="medium")})
            
    # ##### Season Team vs Team Statistics
    elif stats_type == "Team vs Team":
        
        # ##### Select Opponent
        opponent_teams = season_teams.copy()
        opponent_teams.remove(favourite_team)
        opponent_team = st.sidebar.selectbox(label="Select Opponent", 
                                             options=opponent_teams)
        
        # ##### Select Statistics
        filter_stats = st.sidebar.selectbox(label="Select Statistics", 
                                           options=config_comparison_stats.stats_name)
        
        # ##### Latest Games Results
        latest_results = last_games_results(data=data_all,
                                            team_opponent=opponent_team,
                                            season_filter=page_season)
        if latest_results.shape[0] > 0:
            games_txt = 'Games' if latest_results.shape[0] > 1 else 'Game'
            st.markdown(f'<h4><font color = #d20614>{favourite_team}</font> vs {opponent_team} - Last <b><font color = #d20614>{latest_results.shape[0]}</font> '
                        f'{games_txt} Result</h4>', unsafe_allow_html=True)
            st.dataframe(data=latest_results,
                        use_container_width=True, 
                        hide_index=True,
                        column_config={
                            "Home Team": st.column_config.Column(width="large"), 
                            "Away Team": st.column_config.Column(width="large"),
                            "Season": st.column_config.Column(width="small"), 
                            "Week No": st.column_config.Column(width="small"),                      
                            "Result": st.column_config.Column(width="small"),
                        })
        else:
            st.markdown(f'<h4><font color = #d20614>{favourite_team}</font> vs {opponent_team}</h4>', unsafe_allow_html=True)
            st.markdown("No meeting in the last 3 Seasons")


        # ##### Team vs Opponent Stats Type Comparison
        st.markdown(f'<h4><font color = #d20614>{favourite_team}</font> vs {opponent_team} <font color = #d20614>{filter_season}</font> Statistics - '
                    f'<font color = #d20614>{page_season}</font></h4>', unsafe_allow_html=True)

        team_radar, opponent_radar, stat_comparison, comparison_insight = team_stats_comparison(data=data, 
                                                                                                team=favourite_team, 
                                                                                                opponent=opponent_team, 
                                                                                                filter_stats=filter_stats, 
                                                                                                filter_season=filter_season)
        _, team_img_col, _, opp_img_col, _ = st.columns([1.75,2,2.35,2,0.55])
        with team_img_col:
            st.image(config_teams_images['config_teams_logo'][favourite_team], width=100)

        with opp_img_col:
            st.image(config_teams_images['config_teams_logo'][opponent_team], width=100)

        team_col, opponent_col = st.columns([3,3])
        with team_col:
            st.pyplot(team_radar)

        with opponent_col:
            st.pyplot(opponent_radar)

        
        st.dataframe(data=stat_comparison.style.format({stat: '{:.2f}' for stat in [favourite_team, opponent_team]}).apply(lambda x: [
                'background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0),
                     use_container_width=True,
                     hide_index=True,
                    column_config={
                    "Statistics": st.column_config.Column(
                        width="large",
                    ),
                    f"{favourite_team}": st.column_config.Column(
                        width="medium",
                    ),
                    f"{opponent_team}": st.column_config.Column(
                        width="medium",
                    ),
                    "Sig": st.column_config.Column(
                        width="small"
                    ),
                    })
        st.markdown(f"<b><font color = #d20614>{favourite_team}</font></b> has <b><font color = #d20614>{comparison_insight[0]}</font></b> <b>Significant Higher</b> "
                    f"game average stats then <b><font color = #d20614>{opponent_team}</font></b> for <b><font color = #d20614>{filter_season}</font></b> Games and "
                    f"<b><font color = #d20614>{comparison_insight[1]}</font></b> <b>Significant Lower</b> game average stats", unsafe_allow_html=True)
        
    # ##### Team Last 5 Season Types
    elif stats_type == "Last 5 Seasons":

        st.markdown(f'<h4>{favourite_team}</b> <b><font color = #d20614>Last 5</font> Season Stats</h4>', unsafe_allow_html=True)

        # ##### Team Stat
        filter_stat = st.sidebar.selectbox(label="Select Stat", 
                                            options=config_team_stats.stats_team)
        
        last_seasons_stats, last_seasons_plot = team_last_seasons_stats(data=data_all, 
                                                     season_filter=filter_season, 
                                                       stat_filter=filter_stat,
                                                       team=favourite_team)
        
        st.plotly_chart(last_seasons_plot, config=config, use_container_width=True)
        st.dataframe(data=last_seasons_stats.style.format({stat: '{:.2f}' for stat in last_seasons_stats.columns[1:-1]}).apply(lambda x: [
                'background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0),
                     use_container_width=True,
                     hide_index=True)
