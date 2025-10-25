"""Enums for NBA statistics analysis and querying.

This module provides enums for stat types and query types used throughout the application.
"""

from enum import Enum

class PlayerStatType(str, Enum):
    """Valid stat types for queries."""
    POINTS = "points"
    THREES = "threes"
    REBOUNDS = "rebounds"
    ASSISTS = "assists"
    BLOCKS = "blocks"
    STEALS = "steals"
    MINUTES = "minutes"
    SHOOTING = "shooting"
    ALL = "all"


class PlayerQueryType(str, Enum):
    """Valid query types for player stats."""
    STAT_OVERVIEW = "stat_overview"  # Detailed analysis of a specific stat category
    SPECIFIC_STAT = "specific_stat"  # Raw numbers for specific stats
    SEASON_STAT = "season_stat"  # Season-long stats


class TeamStatType(str, Enum):
    """Valid stat types for team stats."""
    OFFENSE = "offense"
    DEFENSE = "defense"
    ALL = "all"

class TeamQueryType(str, Enum):
    """Valid query types for team stats."""
    STAT_OVERVIEW = "stat_overview"  # Detailed analysis of a specific stat category
    SPECIFIC_STAT = "specific_stat"  # Raw numbers for specific stats
    SEASON_STAT = "season_stat"  # Season-long stats
    TEAM_STRENGTHS_WEAKNESSES = "team_strengths_and_weaknesses"  # Analysis of team strengths and weaknesses



