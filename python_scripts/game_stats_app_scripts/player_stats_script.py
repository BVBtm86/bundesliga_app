import pandas as pd
import streamlit as st
from python_scripts.data_script import BundesligaGameData
from python_scripts.game_stats_app_scripts.game_stats_utils import GameStatsConfiguration, GameStatsProcessing, PlayerStatsAnalysis

# ##### Player Stats Analysis Page
def player_page(data:pd.DataFrame,
                favourite_team:str,
                page_season:str,
                season_teams:list,
                last_5_seasons:list) -> st:
    
    # ##### Initialize Player Game Stats Analysis
    player_analysis = PlayerStatsAnalysis()
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
    player_stats_options = player_analysis.analysis_options
    if player_analysis.season_info.season_id.keys()[-1] != page_season:
        player_stats_options.remove("Last 5 Seasons")
    
    stats_type = st.sidebar.selectbox(label="Stats", 
                                      options=player_stats_options)
    
    # ##### Select Season Filter
    possible_season_filters = pd.DataFrame(season_data[season_data['Team'] == favourite_team][player_analysis.season_filter.season_filter].sum() > 0)
    season_filters = possible_season_filters[possible_season_filters[0]].index.to_list()
    if stats_type == 'Player vs Player':
        filter_season = st.sidebar.selectbox(label="Season Filter", 
                                             options=season_filters)
    elif stats_type == 'Last 5 Seasons':
        season_filters.remove("Form")
        filter_season = st.sidebar.selectbox(label="Season Filter", 
                                             options=season_filters)

    # ##### Player Season Statistics
    if stats_type == "Season":

        # ##### Team Stat
        filter_stat = st.sidebar.selectbox(label="Game Stat", 
                                            options=player_analysis.player_stats.stats_player)
    
        # ##### Player Match Day Stats
        logo_col, player_day_stats_col = st.columns([0.5,10])
        with logo_col:
             st.image(player_analysis.teams_info['config_teams_logo'][favourite_team])
        with player_day_stats_col:
            st.markdown(f'<h4>{team_player_analysis}<font color = #d20614> {page_season}</font> Match Day Stats</h4>', unsafe_allow_html=True)

        match_day_fig = player_analysis.player_day_analysis(data=season_data, 
                                                            team=favourite_team, 
                                                            player=team_player_analysis,
                                                            stat_name=filter_stat)
        
        if match_day_fig is not None:
            st.plotly_chart(match_day_fig, config=config, use_container_width=True)
        else:
            st.markdown(f'<b><font color = #d20614> {team_player_analysis} </font></b> has <b>0</b> {filter_stat} during the Season {page_season}', unsafe_allow_html=True)

        # ##### Player Season Filter Statistics
        season_player_stats = player_analysis.player_season_stats(data=season_data, 
                                                                  team=favourite_team, 
                                                                  player=team_player_analysis)
        st.markdown(f'<h4>{team_player_analysis} <font color = #d20614>{page_season}</font> Season Filter Stats</h4>', unsafe_allow_html=True)
        
        insights_col, type_chart_col = st.columns([2, 8])
        with type_chart_col:
            fig_type_player, period_venue, period_venue_1, period_venue_2, period_insights, \
                period_insights_1, period_insights_2 = player_analysis.player_season_filter(data_player_agg=season_player_stats, 
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

        pos_stat = player_analysis.player_stats.stats_player.index(filter_stat)
        st.dataframe(season_player_stats.style.format({stat: '{:.2f}' for stat in player_analysis.season_filter.season_filter}).apply(lambda x: [
            'background-color: #ffffff' if i % 2 == 0 else 'background-color: #e5e5e6' for i in range(len(x))], axis=0).apply(
            lambda x: ['color: #d20614' if i == pos_stat else 'color: #000000' for i in range(len(x))], axis=0), 
                        use_container_width=True, 
                        hide_index=True,
                        column_config={
                        "Stat": st.column_config.Column(
                            width="medium")})

    # ##### Player vs Player Statistics
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
                                            options=player_analysis.comparison_stats.player_stats_name)

        team_player_radar, opponent_player_radar, stat_comparison, comparison_insight = player_analysis.player_stats_comparison(
            data=season_data, 
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
            st.image(player_analysis.teams_info['config_teams_logo'][favourite_team], width=100)

        with opp_img_col:
            st.image(player_analysis.teams_info['config_teams_logo'][opponent_team], width=100)

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
        
    # ##### Player Last 5 Seasons Statistics
    elif stats_type == "Last 5 Seasons":

        all_seasons_player_data = GameStatsProcessing().filter_season_data(
            data=BundesligaGameData().retrieve_all_seasons_player_data(table=GameStatsConfiguration().get_tab_info().player_stats_tab,
                                                                       player_name=team_player_analysis,
                                                                       seasons=last_5_seasons))
        
        st.markdown(f'<h4>{team_player_analysis}<font color = #d20614> Last 5</font> Season Stats</h4>', unsafe_allow_html=True)

        # ##### Team Stat
        filter_stat = st.sidebar.selectbox(label="Game Stat",
                                           options=player_analysis.player_stats.stats_player)
        
        last_seasons_stats, last_seasons_plot, season_comparison_insights, insights_last_seasons = player_analysis.player_last_seasons_stats(
            data=all_seasons_player_data,
            season_filter=filter_season,
            stat_filter=filter_stat,
            team=favourite_team)
        
        insight_col, plot_col  = st.columns([2,8])
        with insight_col:
            st.image(player_analysis.teams_info['config_teams_logo'][favourite_team], width=150)

            # ##### Insight Last 5 Seasons
            if insights_last_seasons[0] == 1:
                st.markdown(f"During the last <b><font color = #d20614>5</font></b> Seasons <b><font color = #d20614>{team_player_analysis}"
                            f"</font></b> had only <b><font color = #d20614>1</font></b> Season in the <b><font color = #d20614>"
                            f"Bundesliga</font></b> with <b><font color = #d20614>{insights_last_seasons[2]}</font></b> {insights_last_seasons[3]} playing for "
                            f"<b><font color = #d20614>{favourite_team}</font></b>.", unsafe_allow_html=True)
            else:
                st.markdown(f"During the last <b><font color = #d20614>5</font></b> Seasons <b><font color = #d20614>{team_player_analysis}"
                            f"</font></b> had <b><font color = #d20614>{insights_last_seasons[0]}</font></b> Seasons in the <b><font color = #d20614>"
                            f"Bundesliga</font></b> with <b><font color = #d20614>{insights_last_seasons[2]}</font></b> {insights_last_seasons[3]} playing for "
                            f"<b><font color = #d20614>{favourite_team}</font></b>. Season <b><font color = #d20614>{insights_last_seasons[1]}</font></b> "
                            f"has the highest <b><font color = #d20614>{filter_stat}</font></b> stats per <b><font color = #d20614>{filter_season}</font></b> "
                            f"games.", unsafe_allow_html=True)
        
        with plot_col:
            st.plotly_chart(last_seasons_plot, config=config, use_container_width=True)

        # ##### Season by Season All Stats Table
        pos_stat = player_analysis.player_stats.stats_player.index(filter_stat)
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
