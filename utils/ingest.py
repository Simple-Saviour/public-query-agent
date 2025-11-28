import os
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from supabase import create_client
from dotenv import load_dotenv

# Add parent dir to path so we can import from core/llm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.llm import embeddings

load_dotenv()

# Initialize Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def ingest_pdf_file(file_path: str, category: str):
    """
    Reads a PDF, splits it into chunks, embeds them, and uploads to Supabase.
    """
    try:
        print(f"📄 Processing: {file_path}")
        
        # 1. Load PDF
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        # 2. Split Text (Chunking)
        # We split text so the AI can find specific paragraphs easily
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(pages)
        
        print(f"✂️ Split into {len(docs)} chunks.")
        
        # 3. Embed and Upload to Supabase
        for i, doc in enumerate(docs):
            # Generate Embedding using the model defined in core/llm.py
            vector = embeddings.embed_query(doc.page_content)
            
            # Prepare Data Payload
            data = {
                "content": doc.page_content,
                "metadata": {
                    "category": category, 
                    "source": os.path.basename(file_path),
                    "chunk_id": i
                },
                "embedding": vector
            }
            
            # Insert into 'documents' table
            supabase.table("documents").insert(data).execute()
            
        print("✅ Ingestion Complete!")
        return True, f"Successfully uploaded and processed {len(docs)} chunks."

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, str(e)