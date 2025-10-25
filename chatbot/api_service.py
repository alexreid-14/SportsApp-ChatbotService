from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the chatbot directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.stats_agent import Chatbot, StatsAgent
from tools.player_tools import PlayerStatsTool
from tools.team_tools import TeamStatsTool
from tools.game_tools import GameStatsTool

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the chatbot
chatbot = Chatbot()
stats_agent = StatsAgent()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'service': 'Sports Analytics Chatbot',
        'version': '0.1'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process the message using your chatbot
        response = chatbot.process_message(message, context)
        
        return jsonify({
            'success': True,
            'response': response,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/player/stats', methods=['GET'])
def get_player_stats():
    """Get player statistics"""
    try:
        player_name = request.args.get('name')
        if not player_name:
            return jsonify({'error': 'Player name is required'}), 400
        
        # Use your player tools
        player_tool = PlayerStatsTool()
        stats = player_tool.get_player_stats(player_name)
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/team/stats', methods=['GET'])
def get_team_stats():
    """Get team statistics"""
    try:
        team_name = request.args.get('name')
        if not team_name:
            return jsonify({'error': 'Team name is required'}), 400
        
        # Use your team tools
        team_tool = TeamStatsTool()
        stats = team_tool.get_team_stats(team_name)
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/game/stats', methods=['GET'])
def get_game_stats():
    """Get game statistics"""
    try:
        game_id = request.args.get('id')
        if not game_id:
            return jsonify({'error': 'Game ID is required'}), 400
        
        # Use your game tools
        game_tool = GameStatsTool()
        stats = game_tool.get_game_stats(game_id)
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Sports Analytics Chatbot API Service...")
    print("Available endpoints:")
    print("- GET  /health")
    print("- POST /chat")
    print("- GET  /player/stats")
    print("- GET  /team/stats")
    print("- GET  /game/stats")
    app.run(host='0.0.0.0', port=5000, debug=True) 