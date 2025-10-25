from typing import Dict, List, Optional, Any
from langchain_openai import ChatOpenAI
from langchain.agents import load_agent_planner
from langchain.tools import BaseTool
from langchain_core.runnables import Runnable

class PlanningAgent(Runnable):
    """Planning agent that implements the Runnable interface for PlanAndExecute."""
    
    def __init__(self, llm: ChatOpenAI, tools: List[BaseTool]):
        self.llm = llm
        self.tools = tools
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create the planning agent with betting-specific prompt."""
        # Create detailed tool descriptions
        tool_descriptions = self._create_tool_descriptions()
        
        return load_agent_planner(
            llm=self.llm,
            system_prompt=f"""You are a sports betting analysis planner. Your role is to break down user queries into logical steps.

AVAILABLE TOOLS:
{tool_descriptions}

PLANNING INSTRUCTIONS:
1. Identify the tool based on the user's query
2. Identify the query type to use based on the tool and the user's query
3. Break down into sequential steps
4. Specify required data for each step
5. Note dependencies between steps
6. Include validation steps
7. Specify which tools will be needed for each step

FORMAT EACH STEP AS:
Step [number]: [Natural language instruction]
- Purpose: [What this step accomplishes]
- Data Needed: [Required information]
- Tools Required: [List of tools needed]
- Tool Parameters: [Required parameters for each tool]
- Dependencies: [Previous steps if any]
- Validation: [How to verify results]

Example Plan:
Step 1: Get player's recent scoring average
- Purpose: Establish baseline performance
- Data Needed: Last 10 games scoring stats
- Tools Required: PlayerStatsTool
- Tool Parameters: 
  * player_id: Required
  * stat_type: "points"
  * games: 10
- Dependencies: None
- Validation: Check for minimum games played

Step 2: Compare to current over/under line
- Purpose: Identify potential value
- Data Needed: Current betting line
- Tools Required: GameStatsTool
- Tool Parameters:
  * game_id: Required
  * stat_type: "over_under"
- Dependencies: Step 1
- Validation: Verify line is current

NEVER include tool calls in the plan - focus on the logical steps needed.""",
            max_iterations=5
        )
    
    def _create_tool_descriptions(self) -> str:
        """Create detailed descriptions of available tools and their parameters."""
        descriptions = []
        for tool in self.tools:
            # Get tool description and args
            tool_info = {
                "name": tool.name,
                "description": tool.description,
                "args": tool.args_schema.model_json_schema()["properties"] if hasattr(tool, "args_schema") else {}
            }
            
            # Format the description
            desc = f"{tool_info['name']}\n"
            desc += f"   Description: {tool_info['description']}\n"
            desc += "   Note: This tool can be used multiple times in a single plan with different query types (STAT_OVERVIEW, ODDS, SPECIFIC_STAT, ALL) to handle different aspects of the same query.\n"
            desc += "   Parameters:\n"
            
            # Add parameter details
            for param_name, param_info in tool_info["args"].items():
                desc += f"   - {param_name}: {param_info.get('description', 'No description')}\n"
                if "required" in param_info:
                    desc += f"     Required: {param_info['required']}\n"
                if "type" in param_info:
                    desc += f"     Type: {param_info['type']}\n"
            
            descriptions.append(desc)
        
        return "\n".join(descriptions)
    
    async def ainvoke(self, input_data: Dict[str, Any]) -> str:
        """Create a plan for the given query. This is the main entry point for PlanAndExecute."""
        try:            
            # Get the plan from the agent
            result = await self.agent.ainvoke(input_data)
            
            # Return just the plan string
            return result["output"]
            
        except Exception as e:
            raise  # Let PlanAndExecute handle the error
    
