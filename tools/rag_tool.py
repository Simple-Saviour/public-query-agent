import os
from supabase import create_client
from core.llm import embeddings
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase Client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def query_vector_store(query: str, category_filter: str = None) -> str:
    """
    Embeds the user query and searches Supabase for matching documents.
    """
    try:
        # 1. Generate Embedding for the query
        query_vec = embeddings.embed_query(query)
        
        # 2. Call Supabase RPC function (ensure 'match_documents' exists in your SQL)
        params = {
            "query_embedding": query_vec,
            "match_threshold": 0.5,
            "match_count": 3
        }
        result = supabase.rpc("match_documents", params).execute()
        
        # 3. Format results
        context_text = ""
        for record in result.data:
            meta = record.get('metadata', {})
            # Optional: Filter by category if strictly required
            if category_filter and meta.get('category') != category_filter:
                continue
            context_text += f"\n[Source: {meta.get('source')}]: {record['content']}\n"
        
        return context_text if context_text else "No specific documents found in the database."
        
    except Exception as e:
        return f"Error querying knowledge base: {str(e)}"