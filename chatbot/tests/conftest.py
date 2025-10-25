"""Test configuration and fixtures."""

import pytest
import logging
import sys

@pytest.fixture(autouse=True)
def setup_logging(request):
    """Configure logging for all tests."""
    # Disable pytest's output capture for logging
    request.config.option.capture_log = False
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remove all existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Create file handler
    file_handler = logging.FileHandler('test_debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Configure the chatbot package logger
    chatbot_logger = logging.getLogger('chatbot')
    chatbot_logger.setLevel(logging.DEBUG)
    
    # Configure specific loggers
    loggers = [
        'chatbot.tools.player_tools',
        'chatbot.database.queries',
        'chatbot.agents.stats_agent'
    ]
    
    # Set higher log level for API-related loggers to filter out request/response logs
    api_loggers = [
        'httpx',
        'httpcore',
        'openai',
        'langchain',
        'urllib3',
        'langsmith.client'
    ]
    
    for logger_name in api_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)  # Only show warnings and errors
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        # Prevent propagation to avoid duplicate messages
        logger.propagate = False
        # Add handlers directly to each logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler) 