from langgraph.graph import StateGraph, END
from core.state import AgentState
from core.llm import llm

# Import Agents
from agents.supervisor import supervisor_node
from agents.tax_agent import tax_agent_node
from agents.permit_agent import permit_agent_node
from agents.social_agent import social_agent_node

def general_agent_node(state: AgentState):
    query = state['messages'][-1].content
    response = llm.invoke(f"You are a helpful assistant. Provide a polite general response to: {query}")
    return {"final_response": response.content, "next_step": "qa_agent"}

def qa_agent_node(state: AgentState):
    """Review and polish the answer"""
    draft = state['final_response']
    response = llm.invoke(f"Review this government response for clarity and tone. Keep facts identical. Draft: {draft}")
    return {"final_response": response.content, "next_step": END}

# Initialize Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("tax_agent", tax_agent_node)
workflow.add_node("permit_agent", permit_agent_node)
workflow.add_node("social_agent", social_agent_node)
workflow.add_node("general_agent", general_agent_node)
workflow.add_node("qa_agent", qa_agent_node)

# Set Entry
workflow.set_entry_point("supervisor")

# Conditional Routing
workflow.add_conditional_edges(
    "supervisor",
    lambda state: state['next_step'],
    {
        "tax_agent": "tax_agent",
        "permit_agent": "permit_agent",
        "social_agent": "social_agent",
        "general_agent": "general_agent"
    }
)

# Static Edges to QA
workflow.add_edge("tax_agent", "qa_agent")
workflow.add_edge("permit_agent", "qa_agent")
workflow.add_edge("social_agent", "qa_agent")
workflow.add_edge("general_agent", "qa_agent")
workflow.add_edge("qa_agent", END)

# Compile
app_graph = workflow.compile()