"""Query execution and natural language processing for NBA statistics.

This module handles the execution of SQL queries and natural language query processing.
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from sqlalchemy import text
import os
from typing import Dict, Optional, Union, Any, List
import pandas as pd
import numpy as np
from .connection import DatabaseManager
from .templates import get_common_params
from langchain.schema import SystemMessage, HumanMessage
import json
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

class SQLChain:
    def __init__(self, db_manager: DatabaseManager, llm: ChatOpenAI):
        """Initialize SQLChain with database manager and LLM.
        
        Args:
            db_manager: DatabaseManager instance for database operations
            llm: ChatOpenAI instance for natural language processing
        """
        self.db_manager = db_manager
        self.llm = llm

    def run_nl_query(self, query: str, game_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute natural language query.
        
        Args:
            query: Natural language query
            game_context: Optional game context containing team and player information
            
        Returns:
            Query results as dictionary
        """
        try:
            # Get schema information using SQLDatabase
            schema = self.db_manager.get_table_info()
            season = get_common_params()["season"]
            
            # Get current date for temporal context
            #current_date = datetime.now().strftime('%Y-%m-%d')
            #System Message: "7. Always check game_date against current date to determine if using historical or future data\n"
            # Human Message: f"Current Date: {current_date}\n\n"
            
            # Create structured messages with enhanced context
            messages = [
                SystemMessage(content=(
                    "You are a SQL query generator specialized in NBA statistics. "
                    "Your task is to convert natural language questions into valid SQL queries. "
                    "Follow these rules:\n"
                    "1. Return ONLY the SQL query, with no explanation or additional text\n"
                    "2. Use the exact table and column names from the schema\n"
                    "3. Include all necessary JOINs and WHERE clauses\n"
                    "4. Consider the game context when provided\n"
                    "5. For questions about a players stats in an upcoming game, use player_scoring, player_rebounds, or player_assists tables instead of box_scores\n"
                    "6. For questions about a players stats in a historical game, use box_scores table\n"
                    "7. Ensure the query is valid and executable\n"
                    "8. For questions about a players stats in a season, use player_stats table\n"
                    "9. For betting-related questions, use the appropriate odds tables"
                )),
                HumanMessage(content=(
                    f"Natural Language Query: {query}\n\n"
                    f"Database Schema:\n{schema}\n\n"
                    f"Game Context:\n{game_context if game_context else 'No game context provided'}\n\n"
                    f"Season: {season}"
                ))
            ]
            
            # Get SQL query from LLM
            response = self.llm.invoke(messages)
            sql_query = response.content.strip()
            
            # Validate and execute the query
            validated_query = self.validate_sql_query(sql_query)
            return self.run_sql_query(validated_query)
            
        except Exception as e:
            return {"error": str(e)}


    def run_sql_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute SQL query with optional parameters using direct SQLAlchemy execution.
        
        Args:
            query: SQL query string
            params: Optional dictionary of query parameters
            
        Returns:
            Query results as dictionary with consistent structure
        """
        try:    
            # Create SQLAlchemy text object
            sql = text(query)
            
            # Execute query using SQLAlchemy
            with self.db_manager.engine.connect() as connection:
                result = connection.execute(sql, params or {})
                
                # Get column names from result
                columns = result.keys()
                
                # Convert to list of dictionaries
                results = [dict(zip(columns, row)) for row in result]
                
                return results
                
        except Exception as e:
            return {"error": str(e)}

    def nl_flexible_matchup_query(self, user_query: str, template: str, active_params: dict) -> str:
        """
        Use the LLM to generate the final SQL statement from the user query, template, and active parameters.
        The LLM should fill in the template with the correct filters and conditions based on the user's intent and the provided parameters.

        Args:
            user_query: The natural language query from the user
            template: The SQL template to be filled
            active_params: Dictionary of parameters that are available for filtering

        Returns:
            str: The final SQL query with all placeholders filled
        """
        try:
            logger.debug("Starting nl_flexible_matchup_query with:")
            logger.debug(f"user_query: {user_query}")
            logger.debug(f"template: {template}")
            logger.debug(f"active_params: {active_params}")

            messages = [
                SystemMessage(content=(
                    "You are an expert SQL assistant specialized in NBA statistics. "
                    "Your task is to fill in a SQL template with the correct filters and conditions. "
                    "Follow these rules:\n"
                    "1. Return ONLY the final, executable SQL query\n"
                    "2. Fill in the template with relevant filters based on the user's intent\n"
                    "3. Only include filters that are relevant to the question and parameters\n"
                    "4. Ensure all placeholders are properly replaced\n"
                    "5. Maintain the query's structure while adding necessary conditions\n"
                    "6. For [BASE_FILTERS], add AND conditions for each relevant parameter\n"
                    "    - opp_team_id: Filter by opponent team. opp_team_id = :opp_team_id\n"
                    "    - game_location: Filter by home/away games. game_location = :game_location\n"
                    "    - teammate_out: Filter games where a specific teammate was out. NOT EXISTS (SELECT 1 FROM box_scores t WHERE t.game_id = player_games.game_id AND t.player_name = :teammate_out)\n"
                    "    - teammate_in: Filter games where a specific teammate was in. EXISTS (SELECT 1 FROM box_scores t WHERE t.game_id = player_games.game_id AND t.player_name = :teammate_in)\n"
                    "    - season: Filter by season. season = :season\n"
                    "    - stat_type: Filter by specific stat type. stat_type = :stat_type\n"
                    "    - player_name: Filter by player name. player_name = :player_name\n"
                    "7. For [SELECT_STATEMENT], add the appropriate columns to be returned\n"
                    "    - For individual game records: Return all rows and fields that correspond to the user's query\n"
                    "    - For aggregate: Return all relevant stats with appropriate aggregation, prefixing the column name with 'avg_' or'total_'\n"
                    "    - For count queries: Return COUNT(*) as number_of_games with appropriate filters\n"
                    "    - For specific stat queries: Return only mentioned stats with appropriate aggregation\n"
                    "    - For general performance: Return all relevant stats with AVG aggregation\n"
                    "8. For [CONDITIONS], add WHERE conditions if num_games is specified: game_number(<, >, =, <=, >=) :num_games\n"
                    "9. For stat-based filters (e.g., 'games where scored more than 15 points'), add appropriate conditions in [BASE_FILTERS]\n"
                    "10. Add number_of_games, first_game, and last_game to the SELECT_STATEMENT during aggregate queries if necessary\n"
                )),
                HumanMessage(content=(
                    f"User Query: {user_query}\n\n"
                    f"SQL Template:\n{template}\n\n"
                    f"Available Parameters:\n{active_params}"
                ))
            ]
            
            logger.debug("Calling LLM to generate SQL query...")
            response = self.llm.invoke(messages)
            sql_query = response.content.strip()
            logger.debug(f"LLM generated SQL query: {sql_query}")
            
            logger.debug("Validating SQL query...")
            validated_query = self.validate_sql_query(sql_query)
            logger.debug(f"Validated SQL query: {validated_query}")
            
            return validated_query
            
        except Exception as e:
            logger.error(f"Exception in nl_flexible_matchup_query: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def validate_sql_query(self, query: str) -> str:
        """Validate and clean SQL query before execution.
        
        Args:
            query: Raw SQL query string that may contain additional text
            
        Returns:
            Cleaned and validated SQL query string
            
        Raises:
            ValueError: If query cannot be validated or contains invalid SQL
        """
        try:
            # Remove any markdown code block markers
            query = query.replace('```sql', '').replace('```', '')
            
            # Remove any leading/trailing whitespace and newlines
            query = query.strip()
            
            # Normalize query for consistent checking
            normalized_query = query.lower()
            
            # Only allow SELECT and WITH statements
            if not normalized_query.startswith(('select', 'with')):
                raise ValueError("Only SELECT and WITH statements are allowed")
            
            # Check for common SQL injection patterns with improved detection
            dangerous_patterns = [
                # Destructive commands
                'drop', 'truncate', 'delete', 'update', 'insert', 'alter', 'create',
                # SQL injection patterns
                '--', '/*', '*/', 'xp_', 'exec', 'execute', 'sp_',
                # System functions
                'system', 'shell', 'cmd', 'eval', 'exec'
            ]
            
            # Check for dangerous patterns with word boundaries
            for pattern in dangerous_patterns:
                if f" {pattern} " in f" {normalized_query} " or \
                   normalized_query.startswith(f"{pattern} ") or \
                   normalized_query.endswith(f" {pattern}"):
                    raise ValueError(f"Query contains potentially dangerous pattern: {pattern}")
            
            # Validate query syntax using SQLAlchemy
            try:
                text(query)  # This will raise an error if the SQL is invalid
            except Exception as e:
                raise ValueError(f"Invalid SQL syntax: {str(e)}")
            
            # Additional security: Ensure the query is read-only
            if any(keyword in normalized_query for keyword in ['insert', 'update', 'delete', 'drop', 'alter', 'create']):
                raise ValueError("Only read-only queries are allowed")
            
            return query
            
        except Exception as e:
            raise ValueError(f"SQL validation failed: {str(e)}")
