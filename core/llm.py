import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# --- Configuration Variables ---
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("OPENAI_MODEL_NAME")

# 1. Initialize the Chat Model (Brain)
llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model_name,
    temperature=0
)

# 2. Initialize Embeddings (for Vector Search)
# Note: This model produces 1536-dimensional vectors. 
# Ensure your Supabase table is set to vector(1536).
embeddings = OpenAIEmbeddings(
    api_key=api_key,
    base_url=base_url, # Uncomment this line ONLY if your custom provider supports embeddings
    model="azure/genailab-maas-text-embedding-3-large"
)