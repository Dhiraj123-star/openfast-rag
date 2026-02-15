import os
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get the absolute path to directory of this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "data", "storage.db")

def init_db():
    """Initialise SQLite database to store"""
    # Ensure directory exists before connecting
    os.makedirs(os.path.dirname(DB_PATH),exist_ok=True)
    conn= sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS settings
        (key TEXT PRIMARY KEY, value TEXT)
    ''')    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at: {DB_PATH}")

def get_persistent_vector_id():
    """Retrieve the stored ID from the local database"""
    conn= sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key='vector_store_id'")
    row= cursor.fetchone()          
    conn.close()
    return row[0] if row else None

def save_vector_id(vs_id:str):
    """Save the ID to the local database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)",
                    ('vector_store_id',vs_id))
    conn.commit()
    conn.close()

def get_or_create_vector_store(name: str = "OpenFast-RAG-Store"):
    """Check for existing store or create a new one."""
    # 1. Try to get from local DB first
    existing_id = get_persistent_vector_id()
    if existing_id:
        return existing_id
    # If not found , create new one at OpenAI
    vector_store = client.vector_stores.create(name=name)
    save_vector_id(vector_store.id)
    return vector_store.id

def upload_and_index_file(vector_store_id: str, file_path: str):
    """Uploads a file to OpenAI and attaches it to the vector store."""
    with open(file_path, "rb") as f:
        file_batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id, files=[f]
        )
    return file_batch

def generate_rag_response(vector_store_id: str, query: str):
    """Uses the Responses API to search the vector store and answer."""
    response = client.responses.create(
        model="gpt-4o",
        input=query,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }]
    )
    return response.output_text