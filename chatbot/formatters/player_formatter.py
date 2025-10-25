"""Player statistics formatter for NBA analysis.

This module provides formatting utilities for player statistics and performance metrics.
"""

from typing import Dict, Any, Optional
from ..models.enums import PlayerStatType, PlayerQueryType

class PlayerFormatter:
    """Formatter for player statistics and performance metrics."""
    
    def __init__(self):
        """Initialize the player formatter."""
        self.base_fields = {
            "player_name": str,
            "player_id": str,
            "stat_type": str,
            "query_type": str
        }
    
    def format_response(self, data: Dict[str, Any], stat_type: PlayerStatType, 
                       query_type: PlayerQueryType, player_name: str, player_id: str) -> Dict[str, Any]:
        """Format the response based on query type and stat type."""

        if not data or "error" in data:
            return data
            
        # Extract the first result from the results list if present
        if 'results' in data and data['results']:
            data = data['results'][0]
            
        # Create base response with required fields
        formatted = {
            "player_name": player_name,
            "player_id": player_id,
            "stat_type": stat_type,
            "query_type": query_type
        }
        
        # Format based on query type
        if query_type == PlayerQueryType.STAT_OVERVIEW:
            formatted.update(self._format_stat_overview(data, stat_type))
        elif query_type == PlayerQueryType.SPECIFIC_STAT:
            formatted.update(self._format_specific_stat(data))
        elif query_type == PlayerQueryType.SEASON_STAT:
            formatted.update(self._format_season_stat(data, stat_type))
            
        return formatted
    
    def _format_stat_overview(self, data: Dict[str, Any], stat_type: PlayerStatType) -> Dict[str, Any]:
        """Format stat overview data with hardcoded structure."""
        if stat_type == PlayerStatType.POINTS or stat_type == PlayerStatType.ALL:
            return {
                "betting_info": {
                    "points_over_line": float(data.get("points_over_line", 0)),
                    "points_under_line": float(data.get("points_under_line", 0)),
                    "points_over_odds": float(data.get("points_over_odds", 0)),
                    "points_under_odds": float(data.get("points_under_odds", 0))
                },
                "averages_and_trends": {
                    "season_average": float(data.get("average_points", 0)),
                    "last_5_games": float(data.get("points_last_5_games", 0)),
                    "vs_opponent_avg": float(data.get("points_vs_opp_avg", 0))
                },
                "shot_profile": {
                    "frequency_of_shots_in_mid_range": round(float(data.get("player_mid_range_freq", 0)) * 100, 1),
                    "frequency_of_shots_above_the_break_3": round(float(data.get("player_above_the_break_3_freq", 0)) * 100, 1),
                    "frequency_of_shots_in_corner_3": round(float(data.get("player_corner_3_freq", 0)) * 100, 1),
                    "frequency_of_shots_in_the_restricted_area": round(float(data.get("player_restricted_area_freq", 0)) * 100, 1),
                    "frequency_of_shots_in_the_paint": round(float(data.get("player_in_the_paint_freq", 0)) * 100, 1)
                },
                "opponent_defense": {
                    "opp_defensive_rating_rank": int(data.get("opp_defensive_rating_rank", 0)),
                    "opp_defense_2_pointers_plus_minus": float(data.get("opp_defense_2_pointers_plus_minus", 0)),
                    "opp_defense_2_pointers_frequency_rank": int(data.get("opp_defense_2_pointers_frequency_rank", 0)),
                    "opp_defense_3_pointers_plus_minus": float(data.get("opp_defense_3_pointers_plus_minus", 0)),
                    "opp_defense_3_pointers_frequency_rank": int(data.get("opp_defense_3_pointers_frequency_rank", 0)),
                    "opp_defense_less_than_6_feet_plus_minus": float(data.get("opp_defense_less_than_6_feet_plus_minus", 0)),
                    "opp_defense_less_than_6_feet_frequency_rank": int(data.get("opp_defense_less_than_6_feet_frequency_rank", 0)),
                    "opp_defense_less_than_10_feet_plus_minus": float(data.get("opp_defense_less_than_10_feet_plus_minus", 0)),
                    "opp_defense_less_than_10_feet_frequency_rank": int(data.get("opp_defense_less_than_10_feet_frequency_rank", 0)),
                    "opp_defense_greater_than_15_feet_plus_minus": float(data.get("opp_defense_greater_than_15_feet_plus_minus", 0)),
                    "opp_defense_greater_than_15_feet_frequency_rank": int(data.get("opp_defense_greater_than_15_feet_frequency_rank", 0))
                },
                "summary": """This is a summary of the player's betting info, points stats, shot profile, and the opponent's defense. 
                - Opponent Defense:
                    - Frequency Rank: Indicates how often opposing teams attempt that shot type against the player's team. A lower rank means opponents take fewer shots of that type against them.
                    - Plus-Minus: Represents the difference between the opponent's field goal percentage allowed for that shot type and the league average. A negative plus-minus indicates the opposing defense performs better than average at limiting shots or making them difficult for that shot type"""
            }
        elif stat_type == PlayerStatType.THREES:
            return {
                "betting_info": {
                    "threes_over_line": float(data.get("threes_over_line", 0)),
                    "threes_under_line": float(data.get("threes_under_line", 0)),
                    "threes_over_odds": float(data.get("threes_over_odds", 0)),
                    "threes_under_odds": float(data.get("threes_under_odds", 0))
                },
                "averages_and_trends": {
                    "season_average": float(data.get("average_threes", 0)),
                    "last_5_games": float(data.get("threes_last_5_games", 0)),
                    "vs_opponent_avg": float(data.get("threes_vs_opp_avg", 0))
                },
                "shot_profile": {
                    "frequency_of_shots_above_the_break_3": round(float(data.get("player_above_the_break_3_freq", 0)) * 100, 1),
                    "frequency_of_shots_in_corner_3": round(float(data.get("player_corner_3_freq", 0)) * 100, 1),
                },
                "opponent_defense": {
                    "opp_defensive_rating_rank": int(data.get("opp_defensive_rating_rank", 0)),
                    "opp_defense_3_pointers_plus_minus": float(data.get("opp_defense_3_pointers_plus_minus", 0)),
                    "opp_defense_3_pointers_frequency_rank": int(data.get("opp_defense_3_pointers_frequency_rank", 0)),
                    "opp_defense_greater_than_15_feet_plus_minus": float(data.get("opp_defense_greater_than_15_feet_plus_minus", 0)),
                    "opp_defense_greater_than_15_feet_frequency_rank": int(data.get("opp_defense_greater_than_15_feet_frequency_rank", 0))
                },
                "summary": """This is a summary of the player's three-point shooting performance and betting information.
                - Shot Profile:
                    - Above the Break 3s: Three-pointers taken from above the break (non-corner)
                    - Corner 3s: Three-pointers taken from the corners
                - Opponent Defense:
                    - Frequency Rank: How often opponents attempt threes against this team
                    - Plus-Minus: Difference between opponent's 3P% allowed and league average"""
            }
        elif stat_type == PlayerStatType.REBOUNDS:
            return {
                "betting_info": {
                    "rebounds_over_line": float(data.get("rebounds_over_line", 0)),
                    "rebounds_under_line": float(data.get("rebounds_under_line", 0)),
                    "rebounds_over_odds": float(data.get("rebounds_over_odds", 0)),
                    "rebounds_under_odds": float(data.get("rebounds_under_odds", 0))
                },
                "averages_and_trends": {
                    "season_average": float(data.get("rebounds_per_game", 0)),
                    "last_5_games": float(data.get("rebounds_last_5_games", 0)),
                    "vs_opponent_avg": float(data.get("rebounds_vs_opp_avg", 0))
                },
                "matchup_info": {
                    "opp_rebounds_rank": int(data.get("opp_rebounds_rank", 0))
                },
                "summary": """This is a summary of the player's rebounding performance, including betting information and matchup analysis.
                - Rebounding Analysis:
                    - Season Average: The player's average rebounds per game for the season
                    - Last 5 Games: Recent rebounding performance trend
                    - vs Opponent Average: How the player typically performs against this opponent
                    - Opponent Rebounding Rank: Where the opponent ranks in rebounding defense"""
            }
        elif stat_type == PlayerStatType.ASSISTS:
            return {
                "betting_info": {
                    "assists_over_line": float(data.get("assists_over_line", 0)),
                    "assists_under_line": float(data.get("assists_under_line", 0)),
                    "assists_over_odds": float(data.get("assists_over_odds", 0)),
                    "assists_under_odds": float(data.get("assists_under_odds", 0))
                },
                "averages_and_trends": {
                    "season_average": float(data.get("assists_per_game", 0)),
                    "last_5_games": float(data.get("assists_last_5_games", 0)),
                    "vs_opponent_avg": float(data.get("assists_vs_opp_avg", 0))
                },
                "summary": """This is a summary of the player's assist performance, including betting information and recent trends.
                - Assist Analysis:
                    - Season Average: The player's average assists per game for the season
                    - Last 5 Games: Recent assist performance trend
                    - vs Opponent Average: How the player typically performs against this opponent
                    - Betting Lines: Current over/under lines and odds for assists"""
            }
        elif stat_type == PlayerStatType.STEALS:
            return {
                "betting_info": {
                    "steals_over_line": float(data.get("steals_over_line", 0)),
                    "steals_under_line": float(data.get("steals_under_line", 0)),
                    "steals_over_odds": float(data.get("steals_over_odds", 0)),
                    "steals_under_odds": float(data.get("steals_under_odds", 0))
                },
                "averages_and_trends": {
                    "season_average": float(data.get("steals_per_game", 0)),
                    "last_5_games": float(data.get("steals_last_5_games", 0)),
                    "vs_opponent_avg": float(data.get("steals_vs_opp_avg", 0))
                },
                "summary": """This is a summary of the player's steal performance, including betting information and recent trends.
                - Steal Analysis:
                    - Season Average: The player's average steals per game for the season
                    - Last 5 Games: Recent steal performance trend
                    - vs Opponent Average: How the player typically performs against this opponent"""
            }
        elif stat_type == PlayerStatType.BLOCKS:
            return {
                "betting_info": {
                    "blocks_over_line": float(data.get("blocks_over_line", 0)),
                    "blocks_under_line": float(data.get("blocks_under_line", 0)),
                    "blocks_over_odds": float(data.get("blocks_over_odds", 0)),
                    "blocks_under_odds": float(data.get("blocks_under_odds", 0))
                },
                "averages_and_trends": {
                    "season_average": float(data.get("blocks_per_game", 0)),
                    "last_5_games": float(data.get("blocks_last_5_games", 0)),
                    "vs_opponent_avg": float(data.get("blocks_vs_opp_avg", 0))
                },
                "summary": """This is a summary of the player's block performance, including betting information and recent trends.
                - Block Analysis:
                    - Season Average: The player's average blocks per game for the season
                    - Last 5 Games: Recent block performance trend
                    - vs Opponent Average: How the player typically performs against this opponent"""
            }
        return {}
    
    def _format_specific_stat(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format box score data, attempting to populate all sections with available data."""
        
        formatted = {
            "data": {
                "games": [],
                "aggregates": {},
                "summary": {
                    "total_games": None,
                    "date_range": {
                        "first_game": None,
                        "last_game": None
                    }
                }
            }
        }
        
        # Try to populate games section
        formatted["data"]["games"] = [
            {
                "game_date": data.get("game_date", None),
                "stats": {
                    k: float(v) if isinstance(v, (int, float)) else v
                    for k, v in data.items()
                    if k not in ["game_date", "game_id", "player_id", "player_name", 
                                "number_of_games", "first_game", "last_game"] and
                    not any(prefix in k.lower() for prefix in ["avg_", "total_"])
                },
                "metadata": {
                    "game_number": data.get("game_number", None),
                    "opponent_id": data.get("opp_team_id", None)
                }
            }
        ]
        
        # Try to populate aggregates section
        # Look for any aggregated fields (those with avg_, sum_, etc.)
        formatted["data"]["aggregates"] = {
            k: float(v) if isinstance(v, (int, float)) else v
            for k, v in data.items()
            if any(prefix in k.lower() for prefix in ["avg_", "total_"])
        }
        
        # Try to populate summary section
        formatted["data"]["summary"].update({
            "total_games": data.get("number_of_games", None),
            "date_range": {
                "first_game": data.get("first_game", None),
                "last_game": data.get("last_game", None)
            }
        })
        
        return formatted

    def _format_season_stat(self, data: Dict[str, Any], stat_type: PlayerStatType) -> Dict[str, Any]:
        """Format season statistics data based on stat type."""            
        if stat_type == PlayerStatType.SHOOTING:
            return {
                "shot_zones": {
                    "restricted_area": {
                        "fg_pct": round(float(data.get("restricted_area_fg_pct", 0)) * 100, 1),
                        "frequency": round(float(data.get("restricted_area_freq", 0)) * 100, 1),
                        "rank": int(data.get("restricted_area_rank", 0))
                    },
                    "in_the_paint": {
                        "fg_pct": round(float(data.get("in_the_paint_fg_pct", 0)) * 100, 1),
                        "frequency": round(float(data.get("in_the_paint_freq", 0)) * 100, 1),
                        "rank": int(data.get("in_the_paint_rank", 0))
                    },
                    "mid_range": {
                        "fg_pct": round(float(data.get("mid_range_fg_pct", 0)) * 100, 1),
                        "frequency": round(float(data.get("mid_range_freq", 0)) * 100, 1),
                        "rank": int(data.get("mid_range_rank", 0))
                    },
                    "left_corner_3": {
                        "fg_pct": round(float(data.get("left_corner_3_fg_pct", 0)) * 100, 1),
                        "frequency": round(float(data.get("left_corner_3_freq", 0)) * 100, 1),
                        "rank": int(data.get("left_corner_3_rank", 0))
                    },
                    "right_corner_3": {
                        "fg_pct": round(float(data.get("right_corner_3_fg_pct", 0)) * 100, 1),
                        "frequency": round(float(data.get("right_corner_3_freq", 0)) * 100, 1),
                        "rank": int(data.get("right_corner_3_rank", 0))
                    },
                    "above_break_3": {
                        "fg_pct": round(float(data.get("above_break_3_fg_pct", 0)) * 100, 1),
                        "frequency": round(float(data.get("above_break_3_freq", 0)) * 100, 1),
                        "rank": int(data.get("above_break_3_rank", 0))
                    },
                    "corner_3": {
                        "fg_pct": round(float(data.get("corner_3_fg_pct", 0)) * 100, 1),
                        "frequency": round(float(data.get("corner_3_freq", 0)) * 100, 1),
                        "rank": int(data.get("corner_3_rank", 0))
                    },
                    "back_court": {
                        "fg_pct": round(float(data.get("back_court_fg_pct", 0)) * 100, 1),
                        "frequency": round(float(data.get("back_court_freq", 0)) * 100, 1),
                        "rank": int(data.get("back_court_rank", 0))
                    }
                },
                "summary": """This is a summary of the player's shooting performance, including shooting percentages and frequency of shots in different zones.
                - Metrics:
                    - Fg_pct: Field goal percentage
                    - Frequency: Frequency of shots in the zone
                    - Rank: Rank of frequency of shots compared to other players in that zone
                - Shooting Performance:
                    - Restricted Area: The player's shooting percentage and frequency of shots in the restricted area
                    - In the Paint: The player's shooting percentage and frequency of shots in the paint
                    - Mid-Range: The player's shooting percentage and frequency of shots in the mid-range
                    - Left Corner 3: The player's shooting percentage and frequency of shots in the left corner 3
                    - Right Corner 3: The player's shooting percentage and frequency of shots in the right corner 3
                    - Above the Break 3: The player's shooting percentage and frequency of shots above the break 3
                    - Corner 3: The player's shooting percentage and frequency of shots in the corner 3
                    - Back Court: The player's shooting percentage and frequency of shots in the back court"""
            }
        else:
            return {
                "per_game": {
                    "minutes": round(float(data.get("minutes_per_game", 0)), 1),
                    "points": round(float(data.get("points_per_game", 0)), 1),
                    "threes": round(float(data.get("threes_per_game", 0)), 1),
                    "assists": round(float(data.get("assists_per_game", 0)), 1),
                    "rebounds": round(float(data.get("rebounds_per_game", 0)), 1),
                    "blocks": round(float(data.get("blocks_per_game", 0)), 1),
                    "steals": round(float(data.get("steals_per_game", 0)), 1),
                    "turnovers": round(float(data.get("turnovers_per_game", 0)), 1),
                    "fouls": round(float(data.get("fouls_per_game", 0)), 1)
                },
                "shooting_percentages": {
                    "three_point": round(float(data.get("three_point_pct", 0)) * 100, 1),
                    "field_goal": round(float(data.get("field_goal_pct", 0)) * 100, 1),
                    "free_throw": round(float(data.get("free_throw_pct", 0)) * 100, 1)
                },
                "double_doubles": int(data.get("double_doubles", 0)),
                "triple_doubles": int(data.get("triple_doubles", 0)),
                "summary": "This is a summary of the player's season statistics, including per-game averages, shooting percentages, and double/triple-doubles."
            } 