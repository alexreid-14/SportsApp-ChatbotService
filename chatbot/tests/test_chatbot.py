"""Tests for the chatbot functionality."""

import unittest
import asyncio
import os
from dotenv import load_dotenv
from ..agents.stats_agent import Chatbot
from ..database.connection import get_game_info

# Load environment variables
load_dotenv()

class TestChatbot(unittest.TestCase):
    def setUp(self):       
        # Get game information from database
        self.game_id = "5e3b869b9c20aeb27c069111f69bb825"
        self.game_info = get_game_info(self.game_id)
        
        # Initialize the chatbot
        self.chatbot = Chatbot(
            db_params={"database_url": os.getenv("DATABASE_URL")},
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize empty chat history
        self.chat_history = []
        
    def tearDown(self):
        """Clean up resources after each test."""
        if hasattr(self, 'chatbot'):
            self.chatbot.close()

    async def async_test_basic_player_query(self):
        """Async implementation of the basic player query test."""
        # Test query
        query = "How many poitns has Shai scored against the Nuggets in the last 3 games?" 
        
        # Get response
        response = await self.chatbot.process_query(query, game_context=self.game_info)
        
        # Add assertions
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertTrue(response["success"])
        self.assertGreater(len(response["output"]), 0)

    def test_basic_player_query(self):
        """Synchronous wrapper for the async test."""
        asyncio.run(self.async_test_basic_player_query())

if __name__ == '__main__':
    unittest.main() 