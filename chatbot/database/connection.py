# db.py
import os
from sqlalchemy import create_engine, text, pool
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from typing import Dict, Optional, List, Any, Generator
from sqlalchemy import inspect
from .schema import TABLE_DESCRIPTIONS, TABLE_RELATIONSHIPS
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseManager:
    def __init__(self, db_params: Dict[str, str]):
        """Initialize database connection with parameters and connection pooling.
        
        Args:
            db_params: Dictionary containing database connection parameters
                - database_url: The database connection URL
                - pool_size: (Optional) Size of the connection pool (default: 5)
                - max_overflow: (Optional) Maximum number of connections that can be created beyond pool_size (default: 10)
                - pool_timeout: (Optional) Seconds to wait before giving up on getting a connection from the pool (default: 30)
                - pool_recycle: (Optional) Seconds after which a connection is automatically recycled (default: 3600)
        """
        try:
            # Extract pool configuration with defaults
            pool_size = int(db_params.get("pool_size", 5))
            max_overflow = int(db_params.get("max_overflow", 10))
            pool_timeout = int(db_params.get("pool_timeout", 30))
            pool_recycle = int(db_params.get("pool_recycle", 3600))
            
            # Create engine with connection pooling
            self.engine = create_engine(
                db_params["database_url"],
                poolclass=pool.QueuePool,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_recycle=pool_recycle,
                pool_pre_ping=True  # Enable connection health checks
            )
            
            # Create thread-safe session factory
            self.SessionFactory = scoped_session(sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False
            ))
            
            logger.info(f"Database connection pool initialized with size {pool_size}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {str(e)}")
            raise
    
    @contextmanager
    def get_session(self) -> Generator:
        """Get a database session from the pool.
        
        Yields:
            A database session that will be automatically returned to the pool
            when the context manager exits.
        """
        session = self.SessionFactory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def close(self):
        """Close all database connections and dispose of the engine."""
        try:
            self.SessionFactory.remove()
            self.engine.dispose()
            logger.info("Database connections closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connections: {str(e)}")
            raise

    def get_table_info(self) -> str:
        """Get information about database tables and their columns.
        
        Returns:
            String containing table schema information with descriptions
        """
        try:
            inspector = inspect(self.engine)
            schema_info = []
            
            for table_name in inspector.get_table_names():
                # Get table description
                table_desc = TABLE_DESCRIPTIONS.get(table_name, '')
                
                # Get columns with their types
                columns = inspector.get_columns(table_name)
                column_info = [f"{col['name']} ({col['type']})" for col in columns]
                
                # Get table relationships
                relationships = TABLE_RELATIONSHIPS.get(table_name, {})
                relationship_info = [f"{col} references {ref}" for col, ref in relationships.items()]
                
                # Build table info with description and relationships
                table_info = f"Table: {table_name}"
                if table_desc:
                    table_info += f"\nDescription: {table_desc}"
                table_info += f"\nColumns: {', '.join(column_info)}"
                if relationship_info:
                    table_info += f"\nRelationships: {', '.join(relationship_info)}"
                
                schema_info.append(table_info)
            
            return "\n\n".join(schema_info)
        except Exception as e:
            logger.error(f"Error retrieving table information: {str(e)}")
            return "Error retrieving table information"

def get_game_info(game_id: str) -> Dict[str, Any]:
    """Get comprehensive game statistics and information."""
    query = text("""
        WITH game_players AS (
            SELECT 
                g.game_id,
                g.game_date,
                g.home_team_id,
                g.away_team_id,
                g.home_team_points_line,
                g.home_team_points_odds,
                g.away_team_points_line,
                g.away_team_points_odds,
                g.over_line, 
                g.over_odds,
                g.under_line,
                g.under_odds,
                pt.player_id,
                pt.full_name,
                CASE 
                    WHEN pt.team_id = g.home_team_id THEN 'home'
                    ELSE 'away'
                END as team_side,
                ht.full_name as home_team_name,
                at.full_name as away_team_name
            FROM game_odds g
            LEFT JOIN player_teams pt ON pt.team_id IN (g.home_team_id, g.away_team_id)
            LEFT JOIN teams ht ON ht.team_id = g.home_team_id
            LEFT JOIN teams at ON at.team_id = g.away_team_id
            WHERE g.game_id = :game_id
        )
        SELECT 
            game_id,
            game_date,
            home_team_id,
            away_team_id,
            home_team_name,
            away_team_name,
            home_team_points_line,
            home_team_points_odds,
            away_team_points_line,
            away_team_points_odds,
            over_line, 
            over_odds,
            under_line,
            under_odds,
            json_agg(
                json_build_object(
                    'player_id', player_id,
                    'player_name', full_name
                )
            ) FILTER (WHERE team_side = 'home') as home_players,
            json_agg(
                json_build_object(
                    'player_id', player_id,
                    'player_name', full_name
                )
            ) FILTER (WHERE team_side = 'away') as away_players
        FROM game_players
        GROUP BY 
            game_id,
            game_date,
            home_team_id,
            away_team_id,
            home_team_name,
            away_team_name,
            home_team_points_line,
            home_team_points_odds,
            away_team_points_line,
            away_team_points_odds,
            over_line, 
            over_odds,
            under_line,
            under_odds
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"game_id": game_id})
            row = result.fetchone()
            
            if not row:
                logger.warning(f"No game found with ID {game_id}")
                return {"error": f"No game found with ID {game_id}"}
                
            return {
                "game_id": row.game_id,
                "game_date": row.game_date,
                "betting_info": {
                    "home_team_points_line": row.home_team_points_line,
                    "home_team_points_odds": row.home_team_points_odds,
                    "away_team_points_line": row.away_team_points_line,
                    "away_team_points_odds": row.away_team_points_odds,
                    "over_line": row.over_line,
                    "over_odds": row.over_odds,
                    "under_line": row.under_line,
                    "under_odds": row.under_odds
                },
                "teams": {
                    "home": {
                        "team_id": row.home_team_id,
                        "team_name": row.home_team_name,
                        "players": row.home_players or []
                    },
                    "away": {
                        "team_id": row.away_team_id,
                        "team_name": row.away_team_name,
                        "players": row.away_players or []
                    }
                }
            }
    except Exception as e:
        logger.error(f"Error retrieving game info: {str(e)}")
        return {"error": "Failed to retrieve game information"}