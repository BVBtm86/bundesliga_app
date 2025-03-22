import pandas as pd
import streamlit as st
from python_scripts.game_stats_app_scripts.game_stats_utils import GameStatsStyle, TeamStatsAnalysis

# ##### Team Stats Analysis Page
def team_page(data:pd.DataFrame, 
              data_all:pd.DataFrame, 
              games_schedule:pd.DataFrame,
              page_season:str, 
              favourite_team:str,
              season_teams:list) -> st:
    
    # ##### Initialize Team Game Stats Analysis
    team_analysis = TeamStatsAnalysis()
    config = {'displayModeBar': False}

    # ##### Team Statistics Page Options
    st.sidebar.subheader("Options")

    # #### Team Statistics Type
    team_stats_options = ["Season", "Team vs Team", "Last 5 Seasons"]
    if team_analysis.season_info.season_id.keys()[-1] != page_season:
        team_stats_options.remove("Last 5 Seasons")
    stats_type = st.sidebar.selectbox(label="Stats", 
                                      options=team_stats_options)

    # ##### Select Season Filter
    possible_season_filters = pd.DataFrame(data[data['Team'] == favourite_team][team_analysis.season_filter.season_filter].sum() > 0)
    season_filters = possible_season_filters[possible_season_filters[0]].index.to_list()
    if stats_type == 'Team vs Team':
        filter_season = st.sidebar.selectbox(label="Season Filter", 
                                                options=season_filters)
    elif stats_type == 'Last 5 Seasons':
        season_filters.remove("Form")
        filter_season = st.sidebar.selectbox(label="Season Filter", 
                                                options=season_filters)
    # ##### Season Team Statistics
    if stats_type == "Season":

        # ##### Team Stat
        filter_stat = st.sidebar.selectbox(label="Select Stat", 
                                            options=team_analysis.team_stats.stats_team)

        # ##### Extract Most Important Season Stats and comparison to last years stats
        season_important_stats, diff_important_stats = team_analysis.most_important_stats(data=data, 
                                                                                          data_all=data_all,
                                                                                          current_season=page_season,
                                                                                          previous_seasons=team_analysis.season_info.season_id,
                                                                                          team=favourite_team)

        # ##### Most Important Season Stats
        st.markdown(f'<h4>{favourite_team}</b> <b><font color = #d20614>{page_season}</font> Season Stats</h4>', unsafe_allow_html=True)
        logo_col, metric_col_1, metric_col_2, metric_col_3, metric_col_4, metric_col_5, metric_col_6, metric_col_7  = st.columns([1,1.25,1.25,1.25,1.25,1.25,1.25, 1.25])
        with logo_col:
             st.image(team_analysis.teams_info['config_teams_logo'][favourite_team])

        metric_col_1.metric(label="Goals", value=f"{season_important_stats[5]}", delta=f"{diff_important_stats[5]}")
        metric_col_2.metric(label="Goals Ag", value=f"{season_important_stats[6]}", delta=f"{diff_important_stats[6]}", delta_color="inverse")
        metric_col_3.metric(label='xG', value=f"{season_important_stats[0]}", delta=f"{diff_important_stats[0]}")
        metric_col_4.metric(label="Possession", value=f"{season_important_stats[1]}%", delta=f"{diff_important_stats[1]}")
        metric_col_5.metric(label="Distance Covered", value=f"{season_important_stats[2]}", delta=f"{diff_important_stats[2]}")
        metric_col_6.metric(label="Shots", value=f"{season_important_stats[3]}", delta=f"{diff_important_stats[3]}")
        metric_col_7.metric(label="Points", value=f"{season_important_stats[4]}", delta=f"{diff_important_stats[4]}")
        GameStatsStyle().style_metric_cards()

        if diff_important_stats[0] != "":
            st.markdown(
                f"<b>Note:</b> <b><font color = #43C673>{page_season}</font></b> vs <b><font color = #d20614> "
                f"{team_analysis.season_info.season_comparison[page_season]}</font></b> Season comparison after "
                f"<b>Match Day <font color = #d20614>{data['Week No'].max()}</font></b> ", unsafe_allow_html=True)

        # ##### Team Match Day Stats
        st.markdown(f'<h4>{favourite_team} <font color = #d20614>{page_season}</font> Match Day Stats</h4>', unsafe_allow_html=True)

        match_day_fig, avg_team, avg_opp, better, stat_sig_name = team_analysis.teams_day_analysis(data=data,
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
        season_team_stats, season_opponent_stats = team_analysis.team_season_stats(data=data,
                                                                                   team=favourite_team)
        st.markdown(f'<h4>{favourite_team} <font color = #d20614>{page_season}</font> Season Filter Stats</h4>', unsafe_allow_html=True)

        insights_col, type_chart_col = st.columns([2, 8])
        with type_chart_col:
            fig_type_team, period_venue, period_venue_1, period_venue_2, period_insights, \
                period_insights_1, period_insights_2 = team_analysis.team_season_filter(data_team_agg=season_team_stats,
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
        show_team = st.sidebar.selectbox(label="Show",
                                         options=[f"{favourite_team} Stats", "Opponents Stats"])
        
        pos_stat = team_analysis.team_stats.stats_team.index(filter_stat)
        if show_team == f"{favourite_team} Stats":
            season_filter_data = season_team_stats.copy()
        else:
            season_filter_data = season_opponent_stats.copy()
        
        st.dataframe(season_filter_data.style.format({stat: '{:.2f}' for stat in team_analysis.season_filter.season_filter}).apply(lambda x: [
            'background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
            lambda x: ['color: #d20614' if i == pos_stat else 'color: #000000' for i in range(len(x))], axis=0), 
                        use_container_width=True, 
                        hide_index=True,
                        column_config={
                        "Stat": st.column_config.Column(
                            width="medium")})
            
    # ##### Season Team vs Team Statistics
    elif stats_type == "Team vs Team":
        
        # ##### Get Current Match Day Week
        current_match_day = data['Week No'].max()
        if current_match_day < 34:
            next_game = current_match_day + 1
        else:
            next_game = 34

        # ##### Extract Next Opponent
        week_games_schedule = games_schedule[games_schedule['Week No'] == next_game]
        if favourite_team in week_games_schedule['Home Team'].to_list():
            next_opponent = week_games_schedule[week_games_schedule['Home Team'] == favourite_team]['Away Team'].values[0]
        else:
            next_opponent = week_games_schedule[week_games_schedule['Away Team'] == favourite_team]['Home Team'].values[0]

        # ##### Select Opponent
        opponent_teams = season_teams.copy()
        opponent_teams.remove(favourite_team)
        opponent_team = st.sidebar.selectbox(label="Opponent", 
                                             options=opponent_teams,
                                             index=opponent_teams.index(next_opponent))
        
        # ##### Select Statistics
        filter_stats = st.sidebar.selectbox(label="Statistics", 
                                           options=team_analysis.comparison_stats.team_stats_name)
        
        # ##### Latest Games Results
        latest_results = team_analysis.last_games_results(data=data_all,
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

        
        # ##### Team vs Opponent Table Position
        st.markdown(f'<h4>Standings <font color = #d20614>{favourite_team}</font> vs {opponent_team}', unsafe_allow_html=True)
        week_rank_plot = team_analysis.team_week_rank(data=data,
                                                      team=favourite_team,
                                                      opponent=opponent_team,
                                                      season=page_season)
        st.pyplot(week_rank_plot)

        # ##### Team vs Opponent Stats Type Comparison
        st.markdown(f'<h4><font color = #d20614>{favourite_team}</font> vs {opponent_team} <font color = #d20614>{filter_season}</font> Statistics - '
                    f'<font color = #d20614>{page_season}</font></h4>', unsafe_allow_html=True)

        team_radar, opponent_radar, stat_comparison, comparison_insight = team_analysis.team_stats_comparison(data=data,
                                                                                                              team=favourite_team,
                                                                                                              opponent=opponent_team,
                                                                                                              filter_stats=filter_stats,
                                                                                                              filter_season=filter_season)
        _, team_img_col, _, opp_img_col, _ = st.columns([1.75,2,2.35,2,0.55])
        with team_img_col:
            st.image(team_analysis.teams_info['config_teams_logo'][favourite_team], width=100)

        with opp_img_col:
            st.image(team_analysis.teams_info['config_teams_logo'][opponent_team], width=100)

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
        filter_stat = st.sidebar.selectbox(label="Game Stat", 
                                            options=team_analysis.team_stats.stats_team)
        
        last_seasons_stats, last_seasons_plot, season_comparison_insights, insights_last_seasons = team_analysis.team_last_seasons_stats(
            data=data_all,
            season_filter=filter_season,
            stat_filter=filter_stat)
        
        insight_col, plot_col  = st.columns([2,8])
        with insight_col:
            st.image(team_analysis.teams_info['config_teams_logo'][favourite_team], width=150)

            # ##### Insight Last 5 Seasons
            if insights_last_seasons[0] == 1:
                st.markdown(f"During the last <b><font color = #d20614>5</font></b> Seasons <b><font color = #d20614>{favourite_team}"
                            f"</font></b> had only <b><font color = #d20614>1</font></b> Season in the <b><font color = #d20614>"
                            f"Bundesliga</font></b>.", unsafe_allow_html=True)
            else:
                st.markdown(f"During the last <b><font color = #d20614>5</font></b> Seasons <b><font color = #d20614>{favourite_team}"
                            f"</font></b> had <b><font color = #d20614>{insights_last_seasons[0]}</font></b> Seasons in the <b><font color = #d20614>"
                            f"Bundesliga</font></b>. Season <b><font color = #d20614>{insights_last_seasons[1]}</font></b> has the highest <b><font color = #d20614>"
                            f"{filter_stat}</font></b> stats per <b><font color = #d20614>{filter_season}</font></b> games.", unsafe_allow_html=True)
        
        with plot_col:
            st.plotly_chart(last_seasons_plot, config=config, use_container_width=True)

        # ##### Season by Season All Stats Table
        pos_stat = team_analysis.team_stats.stats_team.index(filter_stat)
        st.dataframe(data=last_seasons_stats.style.format({stat: '{:.2f}' for stat in last_seasons_stats.columns[1:-1]}).apply(
            lambda x: ['background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
                lambda x: ['color: #d20614' if i == pos_stat else 'color: #000000' for i in range(len(x))], axis=0),
                     use_container_width=True,
                     hide_index=True)
        
        ###### Current Season vs Previous Season Insights
        if insights_last_seasons[0] > 1:
            st.markdown(f"Season <b><font color = #d20614>{season_comparison_insights[0]}</font></b> has <b><font color = #d20614>{season_comparison_insights[2]}</font></b> <b>Significant Higher</b> "
                f"game average stats then Season <b><font color = #d20614>{season_comparison_insights[1]}</font></b> for <b><font color = #d20614>{filter_season}</font></b> Games and "
                f"<b><font color = #d20614>{season_comparison_insights[3]}</font></b> <b>Significant Lower</b> game average stats", unsafe_allow_html=True)
