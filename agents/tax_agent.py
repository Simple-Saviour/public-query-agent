from core.llm import llm
from core.state import AgentState
from tools.rag_tool import query_vector_store

def tax_agent_node(state: AgentState):
    query = state['messages'][-1].content
    # Fetch specific Tax knowledge
    context = query_vector_store(query, "Tax")
    
    prompt = f"""You are a Tax Expert for the city. 
    Use the following context to answer the citizen's question.
    Context: {context}
    Question: {query}"""
    
    response = llm.invoke(prompt)
    return {"final_response": response.content, "next_step": "qa_agent"}