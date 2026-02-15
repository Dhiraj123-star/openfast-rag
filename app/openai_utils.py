import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_or_create_vector_store(name: str = "OpenFast-RAG-Store"):
    """Check for existing store or create a new one."""
    # For simplicity, we create one. In a real app, you'd list and find by name.
    vector_store = client.vector_stores.create(name=name)
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