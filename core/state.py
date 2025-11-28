from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Defines the memory passed between agents.
    """
    messages: List[BaseMessage]  # Chat history
    next_step: str               # The next agent to call (e.g., 'tax_agent')
    final_response: str          # The final answer to show the user