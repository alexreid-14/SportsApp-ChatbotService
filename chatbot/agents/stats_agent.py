import json
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.tools import BaseTool
from langsmith import traceable
from ..tools import PlayerStatsTool, TeamStatsTool, GameStatsTool, BaseStatsTool
from ..database.connection import DatabaseManager
from ..database.queries import SQLChain

class StatsAgent():
    def __init__(self, tools: List[BaseTool], llm: ChatOpenAI):
        self.tools = tools
        self.llm = llm
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a sports-analytics assistant. Use the provided GAME CONTEXT to answer questions and to fill in function arguments. If information isn't in context, say so.

GAME CONTEXT:
{game_context}

CRITICAL RULES:
1. ALWAYS use the appropriate tool to get real data first
2. For player queries, use the player_stats tool
3. For team queries, use the team_stats tool
4. For game queries, use the game_stats tool

PARAMETER SELECTION RULES:
1. CAREFULLY read and understand each parameter's description before selecting values
2. query_type: ALWAYS validate user intent and parameter combinations to determine the correct query type 
    - for player_stats tool: 
        - STAT_OVERVIEW requires game_id
        - SEASON_STAT cannot have filters (opp_team_id, game_location, teammate_filter, num_games)
        - SPECIFIC_STAT must have at least one filter
    - for team_stats tool:
        - STAT_OVERVIEW requires team_id
        - SEASON_STAT cannot have filters (opp_team_id, game_location, teammate_filter, num_games)
        - SPECIFIC_STAT must have at least one filter
    - for game_stats tool:
        - STAT_OVERVIEW requires game_id
3. stat_type: ALWAYS validate user intent and stat_type description to determine the correct stat type ENUM
    - If no specific stat type is mentioned in the query, use PlayerStatType.ALL as the default
3. If unsure about parameter selection:
   - Review the parameter descriptions carefully
   - Consider the user's intent
   - Check for any implicit requirements
   - Validate against the rules above

When resolving player/team information:
- Use ONLY the game_id from game_context
- For player queries, find the player in game_context['teams']['home']['players'] or game_context['teams']['away']['players']
- For team queries, use game_context['teams']['home']['team_id'] or game_context['teams']['away']['team_id']
- For opponent information, use the other team's information from game_context['teams']

After getting data:
    - If the data provides insight into the question that needs analysis:
        1. Provide context and explain the significance of the statistics
        2. Look for trends and patterns
        3. Compare current performance to historical data when relevant
        4. Consider matchup-specific factors
        5. Highlight any notable anomalies

        Format responses:
            - If the data is simple stat retrieval:
                1. provide the data in a concise manner
            - if the data is complex:
                1. Summary of key findings
                2. Detailed analysis with supporting data
                3. Context and implications
                4. Notable trends or anomalies
                5. Recommendations if appropriate

NEVER provide responses without using the tools to get real data first.
NEVER provide a response before getting the data."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            prompt=prompt,
            tools=self.tools
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    #@traceable(name="nba_stats_query")
    async def process_query(self, query: str, chat_history: Optional[List] = None, game_context: Optional[Dict] = None) -> Dict:
        try:
            
            # Validate game context
            if game_context and 'game_id' not in game_context:
                raise ValueError("Game context must contain a game_id")
            
            # Set game context and user query for all tools
            if game_context:
                for tool in self.tools:
                    if isinstance(tool, BaseStatsTool):
                        tool.set_game_context(game_context)
                        tool.set_user_query(query)
                    
            # Add game context to the input
            input_data = {
                "input": query,
                "chat_history": chat_history or [],
                "game_context": game_context
            }
    
            result = await self.agent.ainvoke(input_data)
            
            return {
                "success": True,
                "output": result["output"],
                "intermediate_steps": result.get("intermediate_steps", [])
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

class Chatbot:
    def __init__(self, db_params: dict, openai_api_key: str):
        # Initialize components
        self.db_manager = DatabaseManager(db_params)
        
        # Initialize LLM with function calling enabled
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4o",
            openai_api_key=openai_api_key
        )
        
        # Initialize SQLChain with both required arguments
        self.sql_chain = SQLChain(self.db_manager, self.llm)
        
        # Initialize tools with named keyword arguments
        self.tools = [
            PlayerStatsTool(sql_chain=self.sql_chain, database_manager=self.db_manager),
            TeamStatsTool(sql_chain=self.sql_chain, database_manager=self.db_manager),
            GameStatsTool(sql_chain=self.sql_chain, database_manager=self.db_manager)
        ]
        
        # Initialize agent
        self.agent = StatsAgent(self.tools, self.llm)
    
    async def process_query(self, query: str, chat_history: Optional[List] = None, game_context: Optional[Dict] = None) -> Dict:
        return await self.agent.process_query(query, chat_history, game_context)
    
    def close(self):
        self.db_manager.close()
