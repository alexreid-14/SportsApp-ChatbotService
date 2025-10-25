"""Input schemas for NBA statistics analysis and querying.

This module provides Pydantic models for input validation and type safety.
"""

from typing import Optional, List, Tuple
from pydantic import BaseModel, Field
from .enums import PlayerStatType, PlayerQueryType, TeamStatType, TeamQueryType

class PlayerStatsInput(BaseModel):
    """Input model for player statistics queries."""
    player_name: str = Field(..., description="Full name of the player")
    player_id: int = Field(..., description="Unique identifier for the player")
    game_id: Optional[str] = Field(None, description="Unique identifier for the game")
    stat_type: PlayerStatType = Field(
        default=PlayerStatType.ALL, 
        description="""Type of stat to retrieve. Common mappings:
        - Points related: points
        - Rebounds related: rebounds
        - Assists related: assists
        - Three pointers related: threes
        - Steals related: steals
        - Blocks related: blocks
        - Shot locationrelated: shooting
        - Free throws related: free_throws
        - General performance: all"""
    )
    opp_team_id: Optional[int] = Field(None, description="Team ID of the opposing team, ONLY include if query is about a player against a specific opponent")
    teammate_filter: Optional[str] = Field(
        None,
        description="Filter stats based on teammate presence/absence (e.g., when teammate is injured)"
    )
    game_location: Optional[str] = Field(
        None,
        description="Filter stats by game location ('home' or 'away')"
    )
    num_games: Optional[int] = Field(
        None,
        description="Number of games for trend analysis (default: 3 for ambiguous queries like 'recently')"
    )
    query_type: PlayerQueryType = Field(
        ...,
        description="""Type of query to execute. Choose based on these rules:
        1. STAT_OVERVIEW: Use ONLY when:
           - Question is about an upcoming game
           - Question wants to know about how a player will perform in an upcoming game
           - Must include game_id
           
        2. SPECIFIC_STAT: Use when ANY of these are true:
           - Question mentions a specific opponent
           - Question includes a time period (last X games)
           - Question mentions home/away games
           - Question mentions teammate presence/absence
           
        3. SEASON_STAT: Use ONLY when:
           - Question is about overall season performance
           - No specific filters are mentioned
           - No opponent, location, or time period is specified"""
    )

class TeamStatsInput(BaseModel):
    """Input model for team statistics queries."""
    team_name: str = Field(..., description="Name of the team")
    team_id: int = Field(..., description="Unique identifier for the team")
    game_id: Optional[str] = Field(None, description="Unique identifier for the game")
    stat_type: TeamStatType = Field(
        default=TeamStatType.ALL, 
        description="""Type of stat to retrieve. Common mappings:
        - Points related: points
        - Rebounds related: rebounds
        - Assists related: assists
        - Three pointers related: threes
        - Steals related: steals
        - Blocks related: blocks
        - Turnovers related: turnovers
        - Fouls related: fouls
        - Shooting percentages: fg_percentage, three_point_percentage, free_throw_percentage
        - General performance: all"""
    )
    opp_team_id: Optional[int] = Field(None, description="Team ID of the opposing team, ONLY include if query is about a team against a specific opponent")
    game_location: Optional[str] = Field(
        None,
        description="Filter stats by game location ('home' or 'away')"
    )
    num_games: Optional[int] = Field(
        None,
        description="Number of games for trend analysis (default: 3 for ambiguous queries like 'recently')"
    )
    query_type: TeamQueryType = Field(
        ...,
        description="""Type of query to execute. Choose based on these rules:
        1. STAT_OVERVIEW: Use ONLY when:
           - Question is about an upcoming game
           - Question wants to know about how a team will perform in an upcoming game
           - Must include game_id
           
        2. SPECIFIC_STAT: Use when ANY of these are true:
           - Question mentions a specific opponent
           - Question includes a time period (last X games)
           - Question mentions home/away games
           
        3. SEASON_STAT: Use ONLY when:
           - Question is about overall season performance
           - No specific filters are mentioned
           - No opponent, location, or time period is specified
           
        4. STRENGTHS_WEAKNESSES: Use ONLY when:
           - Question is about a team's strengths or weaknesses
           - No specific filters are mentioned
           - No opponent, location, or time period is specified
        """
    )

class GameStatsInput(BaseModel):
    """Input model for game statistics queries."""
    game_id: str = Field(..., description="Unique identifier for the game")
    stat_type: Optional[str] = Field(None, description="Type of stat to retrieve")
