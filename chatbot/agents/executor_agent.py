from typing import Dict, List, Optional, Any
from langchain_openai import ChatOpenAI
from langchain.agents import load_agent_executor
from langchain.tools import BaseTool
from langchain_core.runnables import Runnable



class ExecutorAgent(Runnable):
    """Executor agent that implements the Runnable interface for PlanAndExecute."""
    
    def __init__(self, llm: ChatOpenAI, tools: List[BaseTool]):
        self.llm = llm
        self.tools = tools
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create the executor agent with betting-specific prompt."""
        return load_agent_executor(
            llm=self.llm,
            tools=self.tools,
            system_prompt="""You are a sports betting analysis executor. Your role is to execute the planned steps using the available tools and generate a comprehensive analysis.

EXECUTION RULES:
1. Execute steps in exact order
2. Use tools only when specified
3. Maintain context between steps
4. Validate results at each step
5. Handle errors gracefully
6. Always use the appropriate tools to get real data and maintain context throughout the analysis

CONTEXT MANAGEMENT:
1. Store results from each step
2. Track dependencies
3. Maintain betting context
4. Note any anomalies
5. Keep statistical context

RESPONSE STRUCTURE:
1. Summary of Findings
   - Key statistics
   - Notable patterns
   - Important context

2. Analysis
   - Statistical significance
   - Historical context
   - Current trends

3. Betting Implications
   - Value opportunities
   - Risk factors
   - Recommended actions

4. Supporting Evidence
   - Data points
   - Statistical backing
   - Contextual factors

ALWAYS:
1. Use the appropriate tools to get real data
2. Maintain context throughout the analysis
3. Generate a well-structured, comprehensive response
4. Include specific data points to support your analysis
5. Make clear betting recommendations when appropriate""",
            max_iterations=3
        )
    
    async def ainvoke(self, input_data: Dict[str, Any]) -> str:
        """Execute the given plan using available tools and generate a response. This is the main entry point for PlanAndExecute."""
        try:            
            # Execute the plan and generate response in one step
            result = await self.agent.ainvoke(input_data)
            
            # Return the final response
            return result["output"]
            
        except Exception as e:
            raise  # Let PlanAndExecute handle the error 