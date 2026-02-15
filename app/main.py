import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models import QueryRequest, QueryResponse, UploadResponse
from app.openai_utils import get_or_create_vector_store, upload_and_index_file, generate_rag_response

app = FastAPI(title="OpenFast-RAG")

# In-memory storage for the ID (Keep it simple for now)
# In production, move this to a database or config file
CURRENT_VECTOR_STORE_ID = None

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    global CURRENT_VECTOR_STORE_ID
    
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{file.filename}"
    
    # Save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Get or create vector store
        if not CURRENT_VECTOR_STORE_ID:
            CURRENT_VECTOR_STORE_ID = get_or_create_vector_store()

        # Index file
        batch = upload_and_index_file(CURRENT_VECTOR_STORE_ID, file_path)
        
        # Cleanup local file
        os.remove(file_path)

        return {
            "message": "File processed and indexed",
            "vector_store_id": CURRENT_VECTOR_STORE_ID,
            "file_id": "batch_upload_successful"
        }
    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    if not CURRENT_VECTOR_STORE_ID:
        raise HTTPException(status_code=400, detail="Please upload a document first.")

    try:
        answer = generate_rag_response(CURRENT_VECTOR_STORE_ID, request.question)
        return {
            "answer": answer,
            "vector_store_id": CURRENT_VECTOR_STORE_ID
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)