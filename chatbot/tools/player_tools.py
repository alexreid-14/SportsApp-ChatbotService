"""Player statistics tools for NBA analysis.

This module provides tools for querying player statistics and performance metrics.
"""

from typing import Dict, Optional, Type, Any, List, Tuple, Set
from pydantic import BaseModel, Field
from time import time
from .base import BaseStatsTool
from ..models.schemas import PlayerStatsInput
from ..models.enums import PlayerStatType, PlayerQueryType
from ..database.templates import get_common_params, get_player_specific_stat_template, get_player_stat_overview_template, get_player_season_stat_template
from ..formatters.player_formatter import PlayerFormatter
import logging

# Configure logging
logger = logging.getLogger(__name__)

class PlayerStatsTool(BaseStatsTool):
    """Tool for querying player statistics."""
    
    name: str = "player_stats"
    description: str = "Get player statistics and performance metrics including overviews on points, threes, rebounds, assists, and betting odds. Any questions related to a specific player should be routed to this tool."
    args_schema: Type[BaseModel] = PlayerStatsInput
    formatter: PlayerFormatter = PlayerFormatter()
    
    def _run(self, player_id: int, player_name: str, query_type: PlayerQueryType, stat_type: PlayerStatType = PlayerStatType.ALL, **kwargs) -> Dict:
        """Execute player statistics query."""
        
        try:
            if query_type == PlayerQueryType.STAT_OVERVIEW:
                result = self._handle_stat_overview(player_id=player_id, stat_type=stat_type, **kwargs)
            elif query_type == PlayerQueryType.SPECIFIC_STAT:
                result = self._handle_specific_stat(player_id=player_id, **kwargs)
            elif query_type == PlayerQueryType.SEASON_STAT:
                result = self._handle_season_stat(player_id=player_id, stat_type=stat_type)

                
            # Format the response using the formatter
            return self.formatter.format_response(
                result,
                stat_type=stat_type,
                query_type=query_type,
                player_name=player_name,
                player_id=player_id
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
    


    def _handle_stat_overview(self, player_id: int, stat_type: PlayerStatType, **kwargs) -> Dict:
        """Handle general player statistics overview queries."""
        try:
            logger.debug("=== Starting _handle_stat_overview ===")
            
            game_id = kwargs.get("game_id")

            logger.debug(f"stat_type: {stat_type}")
            logger.debug(f"player_id: {player_id}")
            logger.debug(f"game_id: {game_id}")
            logger.debug(f"kwargs: {kwargs}")

            template = get_player_stat_overview_template(stat_type)
            logger.debug(f"Got template: {template}")
            if not template:
                return self._handle_error(ValueError("Invalid stat type"))
            
            params = get_common_params()
            params.update({
                "player_id": player_id,
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

            template = get_player_specific_stat_template()
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
    
    def _handle_season_stat(self, player_id: int, stat_type: PlayerStatType) -> Dict:
        """Handle season stat queries."""
        try:
            logger.debug("=== Starting _handle_season_stat ===")
            
            logger.debug(f"stat_type: {stat_type}")
            logger.debug(f"player_id: {player_id}")

            template = get_player_season_stat_template(stat_type)
            logger.debug(f"Got template: {template}")
            if not template:
                return self._handle_error(ValueError("Invalid stat type"))
            
            params = get_common_params()
            params.update({
                "player_id": player_id,
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
