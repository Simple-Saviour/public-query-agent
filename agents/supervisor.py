from langchain_core.messages import SystemMessage, HumanMessage
from core.llm import llm
from core.state import AgentState
from tools.analytics_tool import log_query_category

def supervisor_node(state: AgentState):
    """
    Analyzes intent and routes to the correct specialist.
    """
    last_user_message = state['messages'][-1].content
    
    system_prompt = (
        "You are the Supervisor for a Government Public Service Portal. "
        "Classify the user query into one of these intents: 'TAX', 'PERMIT', 'SOCIAL', or 'GENERAL'. "
        "Return ONLY the intent word."
    )
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=last_user_message)])
    intent = response.content.strip().upper()
    
    # Log for analytics
    log_query_category(intent)

    # Routing Logic
    if "TAX" in intent: return {"next_step": "tax_agent"}
    if "PERMIT" in intent: return {"next_step": "permit_agent"}
    if "SOCIAL" in intent: return {"next_step": "social_agent"}
    
    return {"next_step": "general_agent"}