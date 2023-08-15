import pandas as pd
import numpy as np
import streamlit as st
import streamlit as st
import plotly.express as px
from scipy.stats import ttest_ind
from python_scripts.game_stats_scripts.game_stats_utils import team_logos_config, previous_seasons, season_filter, team_most_important_stats, stats_team, stats_count_calculations, stats_perc_calculations, filter_season_data, style_metric_cards


def most_important_stats(data, data_all, current_season, previous_seasons, team):

    season_data = data.copy()
    # ##### Current Season Avg Stats
    season_important_stats = list(season_data[season_data['Team'] == team][team_most_important_stats[:4]].mean().round(2).values)

    # ##### Current Season Sum Stats
    season_data['Win'] = np.where(season_data['Result'] == 'Win', 1, 0)
    season_data['Draw'] = np.where(season_data['Result'] == 'Draw', 1, 0)
    season_important_stats.append((season_data[season_data['Team'] == team]['Win'] * 3 + season_data[season_data['Team'] == team]['Draw']).sum())
    season_important_stats.append(season_data[season_data['Team'] == team][team_most_important_stats[4]].sum())
    season_important_stats.append(season_data[season_data['Team'] == team][team_most_important_stats[5]].sum())
    current_season_match_day = season_data['Week_No'].max()

    # ##### Last Season Stats
    try:
        season_previous = previous_seasons[current_season]
    except:
        season_previous = ""

    if len(season_previous) > 0:
        previous_data_season = data_all[(data_all['Season'] == season_previous) & (data_all['Week_No'] <= current_season_match_day)].reset_index(drop=True)
        if previous_data_season.shape[0] > 0:
            previous_season_important_stats = list(previous_data_season[previous_data_season['Team'] == team][team_most_important_stats[:4]].mean().round(2).values)
            previous_data_season['Win'] = np.where(previous_data_season['Result'] == 'Win', 1, 0)
            previous_data_season['Draw'] = np.where(previous_data_season['Result'] == 'Draw', 1, 0)
            previous_season_important_stats.append((previous_data_season[previous_data_season['Team'] == team]['Win'] * 3 + previous_data_season[previous_data_season['Team'] == team]['Draw']).sum())
            previous_season_important_stats.append(previous_data_season[previous_data_season['Team'] == team][team_most_important_stats[4]].sum())
            previous_season_important_stats.append(previous_data_season[previous_data_season['Team'] == team][team_most_important_stats[5]].sum())
            diff_important_stats = list(pd.Series(season_important_stats) - pd.Series(previous_season_important_stats))
            diff_important_stats[:4] = np.round(diff_important_stats[:4],2)
        else:
            diff_important_stats = ["", "", "", "", "", "", ""]
        
    else:
        diff_important_stats = ["", "", "", "", "", "", ""]

    return season_important_stats, diff_important_stats
    

def teams_day_analysis(data, team, stat_name):

    # ##### Rename Stats to Orginal Name
    df_match_day = data.copy()
    df_match_day.rename(columns={"Dribbles %":"Dribbles Completed %", 
                                  'Pass %':"Passes Completed %", 
                                  'Pass Short %':"Passes Short Completed %", 
                                  'Pass Medium %':"Passes Medium Completed %", 
                                  'Pass Long %':"Passes Long Completed %", 
                                  'Final Third':"Passes Final Third"}, inplace=True)
    
    # ##### Create Aerial Duel Total Stat
    df_match_day['Duel Aerial'] = df_match_day['Duel Aerial Won'] + df_match_day['Duel Aerial Lost']

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
                 hover_name='Team',
                 )
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
    match_day_fig.update_yaxes(title_text=stat_name)

    # #### Insight Statistics
    if stat_name in stats_perc_calculations.keys():
        stats_agg = stats_perc_calculations[stat_name]
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

    return match_day_fig, avg_team, avg_opp, better, stat_sig_name



def team_season_filter(data_team_agg, data_opp_agg, data_raw, team, stat_name):

    # ##### Season Filter Stats
    team_stat = data_team_agg[data_team_agg['Stat'] == stat_name]
    opponent_stat = data_opp_agg[data_opp_agg['Stat'] == stat_name]
    data_agg = pd.concat([team_stat.drop(columns='Stat'), opponent_stat.drop(columns='Stat')], axis=1).T
    data_agg.reset_index(drop=False, inplace=True)
    data_agg.loc[:int(len(data_agg) / 2), 'Team'] = team
    data_agg.loc[int(len(data_agg) / 2):, 'Team'] = 'Opponent'
    data_agg.columns = ['Season Filter', stat_name, 'Team']

    # ##### Plot Min and Max Values
    data_season_type=data_raw.copy()
    min_value = np.min(data_season_type[stat_name]) * 0.8
    if min_value < 10:
        min_value = 0
    max_value = np.max(data_season_type[stat_name]) * 1.1

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
                           title=f"{team} {stat_name} per Game")
    team_stat_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value])
    team_stat_fig.update_yaxes(title_text=stat_name)

    # ##### Season Filter Insights Home vs Away
    team_insight_data = data_agg[data_agg['Team'] == team]
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
    if "2nd Half" in team_insight_data['Season Filter'].values:
        if team_insight_data[team_insight_data['Season Filter'] == '1st Half'][stat_name].values[0] > team_insight_data[team_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]:
            period_insights = ['1st Half', '2nd Half']
            period_insights_1 = team_insight_data[team_insight_data['Season Filter'] == '1st Half'][stat_name].values[0]
            period_insights_2 = team_insight_data[team_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]
        else:
            period_insights = ['2nd Half', '1st Half']
            period_insights_1 = team_insight_data[team_insight_data['Season Filter'] == '2nd Half'][stat_name].values[0]
            period_insights_2 = team_insight_data[team_insight_data['Season Filter'] == '1st Half'][stat_name].values[0]

    return team_stat_fig, period_venue, period_venue_1, period_venue_2, period_insights, period_insights_1, period_insights_2


st.cache_data(ttl=3600)
def team_season_stats(data, team):

    team_season_data = data.copy()
    team_season_data.rename(columns={'Final Third':'Passes Final Third'}, inplace=True)

    # ##### Filter Data Based on Team
    team_data_stats = team_season_data[team_season_data['Team'] == team].reset_index(drop=True)
    opponent_data_stats = team_season_data[team_season_data['Opponent'] == team].reset_index(drop=True)
    final_team_data = pd.concat([team_data_stats, opponent_data_stats]).reset_index(drop=True)

    # ##### Stats Aggregation based on Season Filter
    filter_agg_data = filter_season_data(data=final_team_data)

    team_filter_count = filter_season_data(data=team_data_stats)[season_filter].sum()
    opponent_filter_count = filter_season_data(data=opponent_data_stats)[season_filter].sum()


    season_team_stats = []
    season_opponent_stats = []
    for filter in season_filter:
        season_team_stats.append(list(filter_agg_data[(filter_agg_data['Team'] == team) & (filter_agg_data[filter] == 1)][stats_count_calculations].sum().values))
        season_opponent_stats.append(list(filter_agg_data[(filter_agg_data['Opponent'] == team) & (filter_agg_data[filter] == 1)][stats_count_calculations].sum().values))
    season_team_stats = pd.DataFrame(season_team_stats, columns=stats_count_calculations, index=season_filter)
    season_opponent_stats = pd.DataFrame(season_opponent_stats, columns=stats_count_calculations, index=season_filter)
    season_team_stats['Duel Aerial'] = season_team_stats['Duel Aerial Won'] + season_team_stats['Duel Aerial Lost']
    season_opponent_stats['Duel Aerial'] = season_opponent_stats['Duel Aerial Won'] + season_opponent_stats['Duel Aerial Lost']

    # ##### Aggregate % Stats
    for stat in stats_perc_calculations.keys():
        season_team_stats[stat] = season_team_stats[stats_perc_calculations[stat][1]] / season_team_stats[stats_perc_calculations[stat][0]] * 100
        season_opponent_stats[stat] = season_opponent_stats[stats_perc_calculations[stat][1]] / season_opponent_stats[stats_perc_calculations[stat][0]] * 100

    # ##### Final Processing for Team Statistics
    season_team_stats.drop(columns=['Duel Aerial'], inplace=True)
    season_team_stats[stats_count_calculations] = np.array(season_team_stats[stats_count_calculations]) / np.array(team_filter_count).reshape(-1,1)
    season_team_stats = season_team_stats.T
    season_team_stats = season_team_stats.reindex(stats_team)
    season_team_stats = season_team_stats.reset_index(drop=False)
    season_team_stats.rename(columns={'index':'Stat'}, inplace=True)
    season_team_stats.loc[season_team_stats['Stat'] == 'Final Third', 'Stat'] = 'Passes Final 3rd'

    # ##### Final Processing for Opponent Statistics
    season_opponent_stats.drop(columns=['Duel Aerial'], inplace=True)
    season_opponent_stats[stats_count_calculations] = np.array(season_opponent_stats[stats_count_calculations]) / np.array(opponent_filter_count).reshape(-1,1)
    season_opponent_stats = season_opponent_stats.T
    season_opponent_stats = season_opponent_stats.reindex(stats_team)
    season_opponent_stats = season_opponent_stats.reset_index(drop=False)
    season_opponent_stats.rename(columns={'index':'Stat'}, inplace=True)
    season_opponent_stats.loc[season_opponent_stats['Stat'] == 'Final Third', 'Stat'] = 'Passes Final 3rd'

    season_team_stats = season_team_stats.round(2)
    return season_team_stats, season_opponent_stats


def team_page(data, data_all, page_season, favourite_team):
    config = {'displayModeBar': False}

    # #### Team Statistics Type
    stats_type = st.sidebar.selectbox(label="Season Stats", 
                                      options=["Season", "Team vs Team", "Last 5 Seasons"])
    # ##### Select Stat
    filter_stat = st.sidebar.selectbox(label="Select Stat", 
                                         options=stats_team)

    if stats_type == "Season":

        # ##### Extract Most Important Season Stats and comparison to last years stats
        season_important_stats, diff_important_stats = most_important_stats(data=data, 
                                                                            data_all=data_all,
                                                                            current_season=page_season,
                                                                            previous_seasons=previous_seasons,
                                                                            team=favourite_team)

        # ##### Most Important Season Stats
        st.markdown(f'<h4>{favourite_team}</b> <b><font color = #d20614>{page_season}</font> Season Stats</h4>', unsafe_allow_html=True)
        logo_col, metric_col_1, metric_col_2, metric_col_3, metric_col_4, metric_col_5, metric_col_6, metric_col_7  = st.columns([1,1.25,1.25,1.25,1.25,1.25,1.25, 1.25])
        with logo_col:
             st.image(team_logos_config[favourite_team])
        
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
                f"<b>Note:</b> <b><font color = #d20614>{page_season}</font></b> vs <b><font color = #d20614>{previous_seasons[page_season]}</font></b> Season comparison", unsafe_allow_html=True)

        # ##### Team Match Day Stats
        st.markdown(f'<h4>{favourite_team}</b> <b><font color = #d20614>{page_season}</font> Match Day Stats</h4>', unsafe_allow_html=True)

        match_day_fig, avg_team, avg_opp, better, stat_sig_name = teams_day_analysis(data=data,
                                           team=favourite_team,
                                           stat_name=filter_stat)
        st.plotly_chart(match_day_fig, config=config, use_container_width=True)

        # ##### Match Day Insights
        if stat_sig_name == "":
            st.markdown(
                f"In <b><font color = #d20614>{better}%</font></b> of the <b><font color = #d20614>{page_season}"
                f"</font></b> Season games {favourite_team} had more <b><font color = green>{filter_stat}</font></b> "
                f"then her opponent. {favourite_team} had an average of <b><font color = #d20614>{avg_team}</font></b> "
                f"<b><font color = green>{filter_stat}</font></b> per game while her opponents had an average of "
                f"<b><font color = #d20614>{avg_opp}</font></b> <b><font color = green>{filter_stat}</font></b> per "
                f"game.", unsafe_allow_html=True)
        else:
            st.markdown(
                f"In <b><font color = #d20614>{better}%</font></b> of the <b><font color = #d20614>{page_season}"
                f"</font></b> Season games {favourite_team} had more <b><font color = green>{filter_stat}</font></b> then"
                f" her opponent. {favourite_team} had an average of <b><font color = #d20614>{avg_team}</font></b> <b>"
                f"<font color = green>{filter_stat}</font></b> per game while her opponents had an average of "
                f"<b><font color = #d20614>{avg_opp}</font></b> <b><font color = green>{filter_stat}</font></b> per "
                f"game, which is <b><font color = #d20614>{stat_sig_name}</font></b>.", unsafe_allow_html=True)

        # ##### Team Season Filter Statistics
        season_team_stats, season_opponent_stats = team_season_stats(data=data,
                                                                     team=favourite_team)
        st.markdown(f'<h4>{favourite_team}</b> <b><font color = #d20614>{page_season}</font> Season Filter Stats</h4>', unsafe_allow_html=True)
    
        insights_col, type_chart_col = st.columns([3, 9])
        with type_chart_col:
            fig_type_team, period_venue, period_venue_1, period_venue_2, period_insights, \
                period_insights_1, period_insights_2 = team_season_filter(data_team_agg=season_team_stats, 
                                            data_opp_agg=season_opponent_stats, 
                                            data_raw=data, 
                                            team=favourite_team, 
                                            stat_name=filter_stat)
            st.plotly_chart(fig_type_team, config=config, use_container_width=True)

        with insights_col:
            st.title("")
            st.markdown(
                f"<b><font color = #d20614>{favourite_team}</font></b> performs much better at <b><font color = #d20614>"
                f"{period_venue[0]}</font></b> Games with <b><font color = #d20614>{period_venue_1:.2f}</font></b> <b>"
                f"<font color = green>{filter_stat}</font></b> per Game on average in comparison to <b><font color = "
                f"#d20614>{period_venue[1]}</font></b> Games where they had  <b><font color = #d20614>{period_venue_2:.2f}"
                f"</font></b> <b><font color = green>{filter_stat}</font></b> per Game on average.",
                unsafe_allow_html=True)

            if period_insights != "":
                st.markdown(
                    f"It also performs much better in the <b><font color = #d20614>{period_insights[0]}</font></b> "
                    f"Season Games with <b><font color = #d20614>{period_insights_1:.2f}</font></b> <b><font color = green>"
                    f"{filter_stat}</font></b> per Game on average in comparison to the <b><font color = #d20614>"
                    f"{period_insights[1]}</font></b> Season Games where they had  <b><font color = #d20614>"
                    f"{period_insights_2:.2f}</font></b> <b><font color = green>{filter_stat}</font></b> per Game on average.",
                    unsafe_allow_html=True)
        
        # ##### Show Team or Opponent Stats
        col_show_team, _ = st.columns([2,6])
        with col_show_team:
            show_team = st.selectbox(label="Show",
                                    options=[f"{favourite_team} Stats", "Opponents Stats"])
        
        pos_stat = season_team_stats[season_team_stats['Stat'] == filter_stat].index.values[0]
        if show_team == f"{favourite_team} Stats":
            st.dataframe(season_team_stats.style.format({stat: '{:.2f}' for stat in ['Season' ,'Form' ,'Home' ,'Away' ,'1st Half' ,'2nd Half' ,'Win' ,'Draw' ,'Defeat']}).apply(lambda x: ['background-color: #ffffff' if i % 2 == 0 
                                                                           else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
                lambda x: ['color: #d20614' if i == pos_stat else 'color: #000000' for i in range(len(x))], axis=0), 
                            use_container_width=True, 
                            hide_index=True,
                            column_config={
                            "Stat": st.column_config.Column(
                                width="medium")})
        else:
            st.dataframe(data=season_opponent_stats.style.format("{:.2f}").apply(lambda x: ['background-color: #ffffff' if i % 2 == 0 
                                                                           else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
                lambda x: ['color: #d20614' if i == pos_stat else 'color: #000000' for i in range(len(x))], axis=0), 
                            use_container_width=True, 
                            hide_index=True,
                            column_config={
                            "Stat": st.column_config.Column(
                                width="medium")})
            