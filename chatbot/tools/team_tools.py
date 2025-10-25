"""Team statistics tools for NBA analysis.

This module provides tools for querying team statistics and performance metrics.
"""

from typing import Dict, Optional, Type, Any
from pydantic import BaseModel, Field
from time import time
from .base import BaseStatsTool
from ..models.schemas import TeamStatsInput
from ..models.enums import TeamStatType, TeamQueryType
from ..database.templates import get_common_params, get_team_specific_stat_template, get_team_stat_overview_template, get_team_season_stat_template, get_team_strengths_weaknesses_template
from ..formatters.team_formatter import TeamFormatter
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TeamStatsTool(BaseStatsTool):
    """Tool for querying team statistics."""
    
    name: str = "team_stats"
    description: str = "Get team statistics and performance metrics including overviews on points, threes, rebounds, assists, and betting odds. Any questions related to a specific team should be routed to this tool."
    args_schema: Type[BaseModel] = TeamStatsInput
    formatter: TeamFormatter = TeamFormatter()
    
    def _run(self, team_id: int, team_name: str, query_type: TeamQueryType, stat_type: TeamStatType = TeamStatType.ALL, **kwargs) -> Dict:
        """Execute team statistics query."""
        
        try:
            if query_type == TeamQueryType.STAT_OVERVIEW:
                result = self._handle_stat_overview(team_id=team_id, stat_type=stat_type, **kwargs)
            elif query_type == TeamQueryType.SEASON_STAT:
                result = self._handle_season_stat(team_id=team_id, stat_type=stat_type)
            elif query_type == TeamQueryType.SPECIFIC_STAT:
                result = self._handle_specific_stat(team_id=team_id, **kwargs)
            elif query_type == TeamQueryType.TEAM_STRENGTHS_WEAKNESSES:
                result = self._handle_strengths_weaknesses(team_id=team_id, **kwargs)

                
            # Format the response using the formatter
            return self.formatter.format_response(
                result,
                stat_type=stat_type,
                query_type=query_type,
                team_name=team_name,
                team_id=team_id
            )
        
        except ValueError as ve:
            # Handle validation errors specifically
            return {
                "error": str(ve),
                "error_type": "validation_error",
                "suggestion": "Please try again with a different query type or parameters"
            }
        except Exception as e:
            return self._handle_error(e)
    
    def _handle_stat_overview(self, team_id: int, stat_type: TeamStatType, **kwargs) -> Dict:
        """Handle general team statistics overview queries."""
        try:
            logger.debug("=== Starting _handle_stat_overview ===")
            
            game_id = kwargs.get("game_id")

            logger.debug(f"stat_type: {stat_type}")
            logger.debug(f"team_id: {team_id}")
            logger.debug(f"game_id: {game_id}")
            logger.debug(f"kwargs: {kwargs}")

            template = get_team_stat_overview_template(stat_type)
            logger.debug(f"Got template: {template}")
            if not template:
                return self._handle_error(ValueError("Invalid stat type"))
            
            params = get_common_params()
            params.update({
                "team_id": team_id,
                "game_id": game_id
            })
            
            # Get raw data from query
            logger.debug("Executing query...")
            result = self._execute_query(template, params)
            logger.debug(f"Query result: {result}")
            return result

        except Exception as e:
            logger.error(f"Exception in _handle_stat_overview: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            return self._handle_error(e)
    
    def _handle_specific_stat(self, **kwargs) -> Dict:
        """Handle context-rich queries with multiple parameters."""
        try:
            logger.debug("=== Starting _handle_specific_stat ===")
            
            user_query = self.user_query  

            logger.debug(f"user_query: {user_query}")
            logger.debug(f"kwargs: {kwargs}")

            template = get_team_specific_stat_template()
            logger.debug(f"Got template: {template}")

            # Get active parameters
            params = get_common_params()
            active_params = {k: v for k, v in kwargs.items() if v is not None and v != ""}
            params.update(active_params)
            logger.debug(f"Active params: {params}")

            # Generate the SQL query using the NL function
            logger.debug("Calling nl_flexible_matchup_query...")
            sql_query = self.sql_chain.nl_flexible_matchup_query(user_query, template, params)
            logger.debug(f"Generated SQL query: {sql_query}")

            # Execute the query and return raw data
            logger.debug("Executing query...")
            result = self._execute_query(sql_query, params)
            logger.debug(f"Query result: {result}")
            return result

        except Exception as e:
            logger.error(f"Exception in _handle_specific_stat: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            return self._handle_error(e)
    
    def _handle_season_stat(self, team_id: int, stat_type: TeamStatType) -> Dict:
        """Handle season stat queries."""
        try:
            logger.debug("=== Starting _handle_season_stat ===")
            
            logger.debug(f"stat_type: {stat_type}")
            logger.debug(f"team_id: {team_id}")

            template = get_team_season_stat_template(stat_type)
            logger.debug(f"Got template: {template}")
            if not template:
                return self._handle_error(ValueError("Invalid stat type"))
            
            params = get_common_params()
            params.update({
                "team_id": team_id,
            })
            logger.debug(f"Final params: {params}")
            
            # Get raw data from query
            logger.debug("Executing query...")
            result = self._execute_query(template, params)
            logger.debug(f"Query result: {result}")
            return result

        except Exception as e:
            logger.error(f"Exception in _handle_season_stat: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            return self._handle_error(e)


    def _handle_strengths_weaknesses(self, team_id: int, **kwargs) -> Dict:
        """Handle team strengths and weaknesses analysis queries."""
        try:
            logger.debug("=== Starting _handle_strengths_weaknesses ===")
            
            logger.debug(f"team_id: {team_id}")
            logger.debug(f"kwargs: {kwargs}")

            template = get_team_strengths_weaknesses_template(stat_type)
            logger.debug(f"Got template: {template}")
            if not template:
                return self._handle_error(ValueError("Invalid template for strengths and weaknesses analysis"))
            
            params = get_common_params()
            params.update({
                "team_id": team_id,
                **kwargs
            })
            
            # Get raw data from query
            logger.debug("Executing query...")
            result = self._execute_query(template, params)
            logger.debug(f"Query result: {result}")
            return result

        except Exception as e:
            logger.error(f"Exception in _handle_strengths_weaknesses: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            return self._handle_error(e)


