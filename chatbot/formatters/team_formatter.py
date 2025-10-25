"""Team statistics formatter for NBA analysis.

This module provides formatting utilities for team statistics and performance metrics.
"""

from typing import Dict, Any
from ..models.enums import TeamStatType, TeamQueryType
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TeamFormatter:
    """Formatter for team statistics responses."""
    
    def format_response(self, result: Dict[str, Any], stat_type: TeamStatType, 
                       query_type: TeamQueryType, team_name: str, team_id: int) -> Dict[str, Any]:
        """Format the response based on query type and stat type."""
        try:
            if query_type == TeamQueryType.STAT_OVERVIEW:
                return self._format_stat_overview(result, stat_type, team_name)
            elif query_type == TeamQueryType.SPECIFIC_STAT:
                return self._format_specific_stat(result, stat_type, team_name)
            elif query_type == TeamQueryType.SEASON_STAT:
                return self._format_season_stat(result, stat_type, team_name)
            elif query_type == TeamQueryType.TEAM_STRENGTHS_WEAKNESSES:
                return self._format_strengths_weaknesses(result, team_name)

        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            return self._format_error(str(e))
    
    def _format_stat_overview(self, result: Dict[str, Any], stat_type: TeamStatType, team_name: str) -> Dict[str, Any]:
        """Format stat overview response."""
        try:
            if not result or "error" in result:
                return result
                
            formatted = {
                "team_name": team_name,
                "stat_type": stat_type,
                "stats": {}
            }
            
            # Add relevant stats based on stat_type
            if stat_type == TeamStatType.ALL:
                formatted["stats"] = {
                    "points": result.get("points", 0),
                    "rebounds": result.get("rebounds", 0),
                    "assists": result.get("assists", 0),
                    "threes": result.get("threes", 0),
                    "blocks": result.get("blocks", 0),
                    "steals": result.get("steals", 0),
                    "turnovers": result.get("turnovers", 0),
                    "fouls": result.get("fouls", 0),
                    "fg_percentage": result.get("fg_percentage", 0),
                    "three_point_percentage": result.get("three_point_percentage", 0),
                    "free_throw_percentage": result.get("free_throw_percentage", 0)
                }
            else:
                formatted["stats"][stat_type] = result.get(stat_type, 0)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting stat overview: {str(e)}")
            return self._format_error(str(e))
    
    def _format_specific_stat(self, result: Dict[str, Any], stat_type: TeamStatType, team_name: str) -> Dict[str, Any]:
        """Format specific stat response."""
        try:
            if not result or "error" in result:
                return result
                
            formatted = {
                "team_name": team_name,
                "stat_type": stat_type,
                "stats": result
            }
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting specific stat: {str(e)}")
            return self._format_error(str(e))
    
    def _format_season_stat(self, result: Dict[str, Any], stat_type: TeamStatType, team_name: str) -> Dict[str, Any]:
        """Format season stat response."""
        try:
            if not result or "error" in result:
                return result
                
            formatted = {
                "team_name": team_name,
                "stat_type": stat_type,
                "season_stats": result
            }
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting season stat: {str(e)}")
            return self._format_error(str(e))

    def _format_offense_stats(self, result: Dict[str, Any], team_name: str) -> Dict[str, Any]:
        """Format offensive statistics response."""
        try:
            if not result or "error" in result:
                return result
                
            formatted = {
                "team_name": team_name,
                "offensive_stats": {
                    "points_per_game": result.get("points_per_game", 0),
                    "field_goal_percentage": result.get("fg_percentage", 0),
                    "three_point_percentage": result.get("three_point_percentage", 0),
                    "free_throw_percentage": result.get("free_throw_percentage", 0),
                    "assists_per_game": result.get("assists_per_game", 0),
                    "turnovers_per_game": result.get("turnovers_per_game", 0),
                    "offensive_rating": result.get("offensive_rating", 0),
                    "pace": result.get("pace", 0),
                    "true_shooting_percentage": result.get("true_shooting_percentage", 0),
                    "effective_field_goal_percentage": result.get("efg_percentage", 0)
                }
            }
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting offense stats: {str(e)}")
            return self._format_error(str(e))

    def _format_defense_stats(self, result: Dict[str, Any], team_name: str) -> Dict[str, Any]:
        """Format defensive statistics response."""
        try:
            if not result or "error" in result:
                return result
                
            formatted = {
                "team_name": team_name,
                "defensive_stats": {
                    "points_allowed_per_game": result.get("points_allowed_per_game", 0),
                    "defensive_rating": result.get("defensive_rating", 0),
                    "opponent_fg_percentage": result.get("opponent_fg_percentage", 0),
                    "opponent_three_point_percentage": result.get("opponent_three_point_percentage", 0),
                    "blocks_per_game": result.get("blocks_per_game", 0),
                    "steals_per_game": result.get("steals_per_game", 0),
                    "defensive_rebounds_per_game": result.get("defensive_rebounds_per_game", 0),
                    "opponent_turnovers_per_game": result.get("opponent_turnovers_per_game", 0)
                }
            }
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting defense stats: {str(e)}")
            return self._format_error(str(e))

    def _format_strengths_weaknesses(self, result: Dict[str, Any], team_name: str) -> Dict[str, Any]:
        """Format team strengths and weaknesses analysis."""
        try:
            if not result or "error" in result:
                return result
                
            formatted = {
                "team_name": team_name,
                "analysis": {
                    "strengths": result.get("strengths", []),
                    "weaknesses": result.get("weaknesses", []),
                    "league_rankings": result.get("league_rankings", {}),
                    "key_metrics": result.get("key_metrics", {})
                }
            }
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting strengths and weaknesses: {str(e)}")
            return self._format_error(str(e))

    def _format_shooting_breakdown(self, result: Dict[str, Any], team_name: str) -> Dict[str, Any]:
        """Format shooting statistics breakdown."""
        try:
            if not result or "error" in result:
                return result
                
            formatted = {
                "team_name": team_name,
                "shooting_stats": {
                    "overall": {
                        "fg_percentage": result.get("fg_percentage", 0),
                        "three_point_percentage": result.get("three_point_percentage", 0),
                        "free_throw_percentage": result.get("free_throw_percentage", 0)
                    },
                    "by_distance": {
                        "0_3_feet": result.get("shooting_0_3_feet", {}),
                        "3_10_feet": result.get("shooting_3_10_feet", {}),
                        "10_16_feet": result.get("shooting_10_16_feet", {}),
                        "16_3p": result.get("shooting_16_3p", {}),
                        "three_point": result.get("shooting_three_point", {})
                    },
                    "shot_distribution": result.get("shot_distribution", {}),
                    "shot_quality": result.get("shot_quality", {})
                }
            }
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting shooting breakdown: {str(e)}")
            return self._format_error(str(e))
    
    def _format_error(self, error_message: str) -> Dict[str, Any]:
        """Format error response."""
        return {
            "error": error_message,
            "error_type": "formatting_error"
        } 