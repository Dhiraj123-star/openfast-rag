import os
import sqlite3
from openai import AsyncOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
# Using beta features requires the beta namespace in newer SDKs
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=120.0)

app = FastAPI(title="OpenFast-RAG")

# Get the absolute path to directory of this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "data", "storage.db")

def init_db():
    """Initialise SQLite database to store"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key='vector_store_id'")
    row = cursor.fetchone()          
    conn.close()
    return row[0] if row else None

def save_vector_id(vs_id: str):
    """Save the ID to the local database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)",
                    ('vector_store_id', vs_id))
    conn.commit()
    conn.close()

async def get_or_create_vector_store(name: str = "OpenFast-RAG-Store"):
    """Check for existing store or create a new one."""
    existing_id = get_persistent_vector_id()
    if existing_id:
        return existing_id
    
    # Path: client.beta.vector_stores
    vector_store = await client.beta.vector_stores.create(name=name)
    save_vector_id(vector_store.id)
    return vector_store.id

async def upload_and_index_file(vector_store_id: str, file_path: str):
    """Uploads a file to OpenAI and attaches it to the vector store."""
    with open(file_path, "rb") as f:
        # Path: client.beta.vector_stores.file_batches
        file_batch = await client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id, files=[f]
        )
    return file_batch

async def generate_rag_response(vector_store_id: str, query: str):
    """Uses the Responses API to search the vector store and answer (Sync version)."""
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        tools=[{"type": "file_search"}],
        tool_choice="auto"
    )
    return response.choices[0].message.content

async def generate_rag_response_stream(vector_store_id: str, query: str):
    """Streams the RAG response chunk by chunk."""
    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        tools=[{"type": "file_search"}],
        stream=True
    ) 
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

async def list_indexed_files(vector_store_id: str):
    """List all files. Fixed AsyncPaginator error and namespace."""
    files = []
    # Correct Path: client.beta.vector_stores.files.list
    async for f in client.beta.vector_stores.files.list(vector_store_id=vector_store_id):
        files.append({"id": f.id, "status": f.status})
    return files

async def list_all_vector_stores():
    """List all stores. Fixed AsyncPaginator error and namespace.""" 
    stores = []
    # Correct Path: client.beta.vector_stores.list
    async for s in client.beta.vector_stores.list():
        stores.append({"id": s.id, "name": s.name, "created_at": s.created_at})
    return stores

async def delete_vector_store(vector_store_id: str):
    """Delete the store."""
    await client.beta.vector_stores.delete(vector_store_id=vector_store_id)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM settings WHERE key='vector_store_id'")
    conn.commit()
    conn.close()
    return True

async def delete_specific_vector_store(vector_store_id: str):
    """Delete specific store."""
    await client.beta.vector_stores.delete(vector_store_id=vector_store_id)
    if get_persistent_vector_id() == vector_store_id:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM settings WHERE key='vector_store_id'")
        conn.commit()
        conn.close()
    return True

async def remove_file_from_store(vector_store_id: str, file_id: str):
    """Removes a file from the vector store."""
    return await client.beta.vector_stores.files.delete(
        vector_store_id=vector_store_id,
        file_id=file_id
    )