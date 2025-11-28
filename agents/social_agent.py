from core.llm import llm
from core.state import AgentState
from tools.rag_tool import query_vector_store

def social_agent_node(state: AgentState):
    query = state['messages'][-1].content
    context = query_vector_store(query, "Social Services")
    
    prompt = f"""You are a Social Welfare Expert. 
    Use the following context to answer the citizen's question.
    Context: {context}
    Question: {query}"""
    
    response = llm.invoke(prompt)
    return {"final_response": response.content, "next_step": "qa_agent"}