from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import PlanAndExecute
from langchain.tools import BaseTool
from ..database.connection import DatabaseManager
from ..database.queries import SQLChain
from ..tools import BaseStatsTool, PlayerStatsTool, TeamStatsTool, GameStatsTool
from .planning_agent import PlanningAgent
from .executor_agent import ExecutorAgent


class PlanAndExecuteChatbot:
    def __init__(self, db_params: dict, openai_api_key: str):        
        # Initialize components
        self.db_manager = DatabaseManager(db_params)
        
        # Initialize LLM with GPT-4-turbo
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4-1106-preview",  # GPT-4-turbo
            openai_api_key=openai_api_key
        )
        
        # Initialize SQLChain
        self.sql_chain = SQLChain(self.db_manager, self.llm)
        
        # Initialize tools
        self.tools = [
            PlayerStatsTool(sql_chain=self.sql_chain),
            TeamStatsTool(sql_chain=self.sql_chain),
            GameStatsTool(sql_chain=self.sql_chain)
        ]
        
        # Initialize planning and executor agents
        self.planner = PlanningAgent(self.llm, self.tools)
        self.executor = ExecutorAgent(self.llm, self.tools)
        
        # Create the PlanAndExecute agent
        self.agent = PlanAndExecute(
            planner=self.planner,
            executor=self.executor,
            verbose=True
        )
    
    async def process_query(self, query: str, chat_history: Optional[List] = None, game_context: Optional[Dict] = None) -> Dict:
        try:
            
            # Set context for all tools
            for tool in self.tools:
                if isinstance(tool, BaseStatsTool):
                    tool.set_game_context(game_context)
                    tool.set_user_query(query)
            
            # Let PlanAndExecute handle the planning and execution
            result = await self.agent.ainvoke({
                "input": query,
                "chat_history": chat_history or [],
                "game_context": game_context
            })
            
            return {
                "success": True,
                "output": result,  # The final response from the executor
                "intermediate_steps": getattr(self.agent, "intermediate_steps", [])  # Get steps from PlanAndExecute
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def close(self):
        """Clean up resources."""
        self.db_manager.close() 