"""Base tools for NBA statistics analysis and querying.

This module provides the base class for all statistics tools.
"""

from typing import Dict, Optional, Any
from pydantic import Field
from langchain_core.tools import BaseTool
from ..database.queries import SQLChain
from ..database.connection import DatabaseManager

class BaseStatsTool(BaseTool):
    """Base class for all statistics tools."""
    
    sql_chain: SQLChain = Field(..., description="SQLChain instance for executing queries")
    database_manager: DatabaseManager = Field(..., description="DatabaseManager instance for executing queries")
    DEFAULT_NUM_GAMES: int = 3
    game_context: Optional[Dict] = None
    user_query: Optional[str] = None
    
    def __init__(self, sql_chain: SQLChain, database_manager: DatabaseManager, **kwargs):
        super().__init__(sql_chain=sql_chain, database_manager=database_manager, **kwargs)
    
    def set_game_context(self, game_context: Dict):
        """Set the game context for the tool."""
        self.game_context = game_context
    
    def set_user_query(self, user_query: str):
        """Set the user query for the tool."""
        self.user_query = user_query
    
    def _execute_query(self, template: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a query using the provided template and parameters."""
        try:    
            # Use DatabaseManager's execute_query method
            results = self.sql_chain.run_sql_query(template, params)
            return {"results": results}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _handle_error(self, error: Exception) -> Dict:
        """Handle errors using natural language fallback."""
        try:
            # Use stored user query and game context
            return self.sql_chain.run_nl_query(self.user_query, self.game_context)
        except Exception as e:
            return {"error": str(e)}
