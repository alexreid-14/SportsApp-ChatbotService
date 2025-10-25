"""SQL templates for NBA statistics queries.

This module contains all SQL query templates used throughout the application.
"""

from typing import Dict, Optional, List, Any
from enum import Enum
from ..models.enums import PlayerQueryType 




# Enhanced query templates with more analytical capabilities
QUERY_TEMPLATES = {
    "player": {
        "stat_overview": {
            "scoring": """
                SELECT 
                    player_name,
                    points_over_line,
                    points_over_odds,
                    points_under_line,
                    points_under_odds,
                    threes_over_line,
                    threes_over_odds,
                    threes_under_line,
                    threes_under_odds,
                    average_points,
                    points_last_5_games,
                    average_threes,
                    threes_last_5_games,
                    points_vs_opp_avg,
                    threes_vs_opp_avg,
                    opp_defensive_rating_rank,
                    opp_defense_2_pointers_plus_minus,
                    opp_defense_2_pointers_frequency_rank,
                    opp_defense_3_pointers_plus_minus,
                    opp_defense_3_pointers_frequency_rank,
                    opp_defense_less_than_6_feet_plus_minus,
                    opp_defense_less_than_6_feet_frequency_rank,
                    opp_defense_less_than_10_feet_plus_minus,
                    opp_defense_less_than_10_feet_frequency_rank,
                    opp_defense_greater_than_15_feet_plus_minus,
                    opp_defense_greater_than_15_feet_frequency_rank,
                    player_corner_3_freq,
                    player_restricted_area_freq,
                    player_in_the_paint_freq,
                    player_mid_range_freq,
                    player_above_the_break_3_freq,
                    player_backcourt_freq
                FROM player_scoring
                WHERE 
                    player_id = :player_id
                    AND game_id = :game_id
            """,
            "rebounds": """
                SELECT 
                    rebounds_over_line, 
                    rebounds_over_odds,
                    rebounds_under_line,
                    rebounds_under_odds,
                    rebounds_per_game,
                    rebounds_last_5_games,
                    rebounds_vs_opp_avg,
                    opp_rebounds_rank
                FROM player_rebounds
                WHERE 
                    player_id = :player_id
                    AND game_id = :game_id
            """,
            "assists": """
                SELECT 
                    assists_over_line, 
                    assists_over_odds,
                    assists_under_line,
                    assists_under_odds,
                    assists_per_game,
                    assists_last_5_games,
                    assists_vs_opp_avg
                FROM player_assists
                WHERE 
                    player_id = :player_id
                    AND game_id = :game_id
            """,
            "steals": """
                SELECT 
                    steals_over_line,
                    steals_over_odds,
                    steals_under_line,
                    steals_under_odds,
                    steals_per_game,
                    steals_last_5_games,
                    steals_vs_opp_avg
                FROM player_steals
                WHERE 
                    player_id = :player_id
                    AND game_id = :game_id
            """,
            "blocks": """
                SELECT 
                    blocks_over_line,
                    blocks_over_odds,
                    blocks_under_line,
                    blocks_under_odds,
                    blocks_per_game,
                    blocks_last_5_games,
                    blocks_vs_opp_avg
                FROM player_blocks
                WHERE 
                    player_id = :player_id
                    AND game_id = :game_id
            """,
        },
        "season_stats": {
            "average_stats": """
                SELECT 
                    minutes_per_game, 
                    points_per_game, 
                    threes_per_game, 
                    assists_per_game, 
                    rebounds_per_game,
                    blocks_per_game,
                    steals_per_game,
                    turnovers_per_game,
                    fouls_per_game,
                    three_point_pct, 
                    field_goal_pct, 
                    free_throw_pct,
                    double_doubles,
                    triple_doubles
                FROM player_stats
                WHERE 
                    player_id = :player_id
                    AND season = :season
            """,
            "shooting_stats": """
                SELECT 
                    restricted_area_fg_pct, 
                    restricted_area_freq, 
                    restricted_area_rank, 
                    in_the_paint_fg_pct, 
                    in_the_paint_freq, 
                    in_the_paint_rank, 
                    mid_range_fg_pct, 
                    mid_range_freq, 
                    mid_range_rank, 
                    left_corner_3_fg_pct, 
                    left_corner_3_freq, 
                    left_corner_3_rank, 
                    right_corner_3_fg_pct, 
                    right_corner_3_freq, 
                    right_corner_3_rank,
                    above_break_3_fg_pct,
                    above_break_3_freq,
                    above_break_3_rank,
                    corner_3_fg_pct,
                    corner_3_freq,
                    corner_3_rank,
                    back_court_fg_pct,
                    back_court_freq,
                    back_court_rank
                FROM player_shots
                WHERE 
                    player_id = :player_id
                    AND season = :season
            """,
        },
        "specific_stats": {
            "box_scores_stats": """
                WITH player_games AS (
                    SELECT
                        game_id,
                        game_date,
                        player_id,
                        player_name,
                        opp_team_id,
                        points,
                        rebounds,
                        assists,
                        three_pointers_made,
                        steals,
                        blocks,
                        minutes_played,
                        RANK() OVER (ORDER BY game_date DESC) AS game_number
                    FROM box_scores
                    WHERE player_id = :player_id
                    AND season = :season
                    -- [BASE_FILTERS]
                )
                SELECT
                    -- [SELECT_STATEMENT]
                FROM player_games
                -- [CONDITIONS]
            """
        }
    },
    "team": {
        "stat_overview": {
            "points": """
                SELECT
                    team_id,
                    team_name,
                    points_per_game
                """
            },
        "specific_stats": {
            "team_game_stats": """
                SELECT
                    team_id,
                    team_name,
                    points_per_game
                """
        },
        "season_stats": {
            "offensive_stats": """
                SELECT
                    wins,
                    losses, 
                    points,
                    points_rank,
                    field_goal_pct,
                    field_goal_pct_rank,
                    three_point_field_goals,
                    three_point_field_goals_rank,
                    free_throw_pct,
                    free_throw_pct_rank,
                    rebounds, 
                    rebounds_rank,
                    offensive_rebounds,
                    offensive_rebounds_rank,
                    assists,
                    assists_rank,
                    steals,
                    steals_rank,
                    turnovers,
                    turnovers_rank,
                    field_goals_restricted_area_pct,
                    field_goals_restricted_area_freq,
                    field_goals_restricted_area_rank,
                    field_goals_in_the_paint_pct,
                    field_goals_in_the_paint_freq,
                    field_goals_in_the_paint_rank,
                    field_goals_mid_range_pct,
                    field_goals_mid_range_freq,
                    field_goals_mid_range_rank,
                    field_goals_left_corner_3_pct,
                    field_goals_left_corner_3_freq,
                    field_goals_left_corner_3_rank,
                    field_goals_right_corner_3_pct,
                    field_goals_right_corner_3_freq,
                    field_goals_right_corner_3_rank,
                    field_goals_above_the_break_3_pct,
                    field_goals_above_the_break_3_freq,
                    field_goals_above_the_break_3_rank
                FROM team_stats
                WHERE 
                    team_id = :team_id 
                    AND season = :season
                """,
            "defensive_stats": """
                SELECT 
                    def_rating,
                    def_rating_rank, 
                    dreb as defensive_rebounds,
                    dreb_rank as defensive_rebounds_rank,
                    stl as steals,
                    stl_rank as steals_rank,
                    blk as blocks,
                    blk_rank as blocks_rank,
                    opp_pts_off_tov as points_off_turnovers,
                FROM team_defensive_stats
                """
        },
        "strengths_weaknesses": {
            "team_strengths_weaknesses": """
                SELECT
                    team_id,
                    team_name,
                    points_per_game
                """
        }
    }
}

# Common query parameters
COMMON_PARAMS = {
    "season": 2024
}


def get_common_params() -> Dict:
    """Get common parameters for queries."""
    return COMMON_PARAMS.copy()

def get_player_stat_overview_template(stat_type: str) -> str:
    """Return the correct stat overview template based on stat_type."""
    if stat_type == "points":
        return QUERY_TEMPLATES["player"]["stat_overview"]["scoring"]
    elif stat_type == "threes":
        return QUERY_TEMPLATES["player"]["stat_overview"]["scoring"]
    elif stat_type == "rebounds":
        return QUERY_TEMPLATES["player"]["stat_overview"]["rebounds"]
    elif stat_type == "assists":
        return QUERY_TEMPLATES["player"]["stat_overview"]["assists"]
    elif stat_type == "all":
        return QUERY_TEMPLATES["player"]["stat_overview"]["scoring"]
    else:
        raise ValueError(f"Unknown stat_type: {stat_type}")

def get_player_specific_stat_template() -> str:
    """Return the flexible matchup template for specific stat queries."""
    return QUERY_TEMPLATES["player"]["specific_stats"]["box_scores_stats"] 
    
def get_player_season_stat_template(stat_type: str) -> str:
    """Return the season stat template for specific stat queries."""
    if stat_type == "shooting":
        return QUERY_TEMPLATES["player"]["season_stats"]["shooting_stats"]
    else:
        return QUERY_TEMPLATES["player"]["season_stats"]["average_stats"]
    
def get_team_stat_overview_template(stat_type: str) -> str:
    """Return the correct stat overview template based on stat_type."""
    if stat_type == "points":
        return QUERY_TEMPLATES["team"]["stat_overview"]["scoring"]
    elif stat_type == "threes":
        return QUERY_TEMPLATES["team"]["stat_overview"]["scoring"]
    elif stat_type == "rebounds":
        return QUERY_TEMPLATES["team"]["stat_overview"]["rebounds"]
    elif stat_type == "assists":
        return QUERY_TEMPLATES["team"]["stat_overview"]["assists"]
    elif stat_type == "all":
        return QUERY_TEMPLATES["team"]["stat_overview"]["scoring"]
    else:
        raise ValueError(f"Unknown stat_type: {stat_type}")

def get_team_specific_stat_template() -> str:
    """Return the flexible matchup template for specific stat queries."""
    return QUERY_TEMPLATES["team"]["specific_stats"]["box_scores_stats"] 
    
def get_team_season_stat_template(stat_type: str) -> str:
    """Return the season stat template for specific stat queries."""
    if stat_type == "shooting":
        return QUERY_TEMPLATES["team"]["season_stats"]["shooting_stats"]
    else:
        return QUERY_TEMPLATES["team"]["season_stats"]["average_stats"]
    
def get_team_strengths_weaknesses_template(stat_type: str) -> str:
    """Return the season stat template for specific stat queries."""
    if stat_type == "shooting":
        return QUERY_TEMPLATES["team"]["season_stats"]["shooting_stats"]
    else:
        return QUERY_TEMPLATES["team"]["season_stats"]["average_stats"]