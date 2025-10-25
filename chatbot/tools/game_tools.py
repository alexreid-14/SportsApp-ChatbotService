"""Game statistics tools for NBA analysis.

This module provides tools for querying game statistics and performance metrics.
"""

from typing import Dict, Optional, Type
from pydantic import BaseModel, Field
from time import time
from .base import BaseStatsTool
from ..models.schemas import GameStatsInput
from ..database.templates import get_stat_overview_template, get_common_params

class GameStatsTool(BaseStatsTool):
    """Tool for querying game statistics."""
    
    name: str = "game_stats"
    description: str = "Get game statistics and performance metrics"
    args_schema: Type[BaseModel] = GameStatsInput
    
    def _run(self, game_id: str, stat_type: Optional[str] = None) -> Dict:
        """Execute game statistics query."""
        start_time = time()
        try:
            # Get template and parameters
            template = get_stat_overview_template("game_stats.basic")
            params = get_common_params()
            params.update({"game_id": game_id})
            
            # Execute query
            result = self._execute_query(template, params)
            
            return result
            
        except Exception as e:
            return self._handle_error(e)
