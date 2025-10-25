"""Database schema descriptions for NBA statistics.

This module contains descriptions of tables and their relationships to help the LLM
better understand the database structure.
"""

TABLE_DESCRIPTIONS = {
    'players': 'Core table containing basic player information and biographical data',
    'teams': 'Core table containing team information and location data',
    'games': 'Core table containing game information and scores',
    'box_scores': 'Detailed player statistics for each game that has been played',
    'player_stats': 'Seasonal averages and statistics for each player',
    'team_stats': 'Seasonal team statistics and rankings',
    'game_odds': 'Betting odds and lines for each game',
    'player_shots': 'Detailed shot location and frequency statistics for players',
    'team_defensive_stats': 'Team defensive statistics and rankings',
    'team_game_stats': 'Game-by-game team statistics',
    'player_teams': 'Historical player-team associations',
    'player_trends': 'Recent performance trends for players',
    'player_scoring': 'Detailed scoring statistics and betting lines for players used to analyze player point performance in upcoming games',
    'player_rebounds': 'Rebounding statistics and betting lines for players used to analyze player rebound performance in upcoming games',
    'player_assists': 'Assist statistics and betting lines for players used to analyze player assist performance in upcoming games',
    'player_team_trends': 'Player performance trends against specific teams',
    'player_props': 'Player prop bet lines and odds'
}

# Table relationships to help the LLM understand how tables are connected
TABLE_RELATIONSHIPS = {
    'games': {
        'home_team_id': 'teams.team_id',
        'away_team_id': 'teams.team_id'
    },
    'box_scores': {
        'game_id': 'games.game_id',
        'player_id': 'players.player_id',
        'opp_team_id': 'teams.team_id'
    },
    'player_stats': {
        'player_id': 'players.player_id'
    },
    'team_stats': {
        'team_id': 'teams.team_id'
    },
    'game_odds': {
        'game_id': 'games.game_id',
        'home_team_id': 'teams.team_id',
        'away_team_id': 'teams.team_id'
    },
    'player_shots': {
        'player_id': 'players.player_id'
    },
    'team_defensive_stats': {
        'team_id': 'teams.team_id'
    },
    'team_game_stats': {
        'team_id': 'teams.team_id',
        'game_id': 'games.game_id'
    },
    'player_teams': {
        'player_id': 'players.player_id',
        'team_id': 'teams.team_id'
    },
    'player_trends': {
        'player_id': 'players.player_id',
        'last_game_id': 'games.game_id'
    },
    'player_scoring': {
        'game_id': 'games.game_id',
        'player_id': 'players.player_id'
    },
    'player_rebounds': {
        'game_id': 'games.game_id',
        'player_id': 'players.player_id'
    },
    'player_assists': {
        'game_id': 'games.game_id',
        'player_id': 'players.player_id'
    },
    'player_team_trends': {
        'player_id': 'players.player_id',
        'opp_team_id': 'teams.team_id'
    },
    'player_props': {
        'game_id': 'games.game_id',
        'player_id': 'players.player_id'
    }
} 