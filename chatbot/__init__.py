"""
Chatbot package for NBA statistics analysis and querying.

This package provides tools and agents for analyzing NBA statistics, including:
- Player statistics and performance metrics
- Team statistics and matchup analysis
- Game statistics and betting information
"""

__version__ = "0.1"

# Import main components to expose them at package level
from .agents.stats_agent import Chatbot, StatsAgent
from .tools.player_tools import PlayerStatsTool
from .tools.team_tools import TeamStatsTool
from .tools.game_tools import GameStatsTool

# Define what should be exposed when using "from chatbot import *"
__all__ = [
    'Chatbot',
    'StatsAgent',
    'PlayerStatsTool',
    'TeamStatsTool',
    'GameStatsTool',
] 