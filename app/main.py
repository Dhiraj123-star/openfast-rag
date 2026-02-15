import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models import QueryRequest, QueryResponse, UploadResponse
from app.openai_utils import (
    init_db,
    get_or_create_vector_store,
    upload_and_index_file,
    generate_rag_response
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="OpenFast-RAG",lifespan=lifespan)


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    file_path= f"data/{file.filename}"
    
    # Save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # This will now check the DB first automatically
        vs_id = get_or_create_vector_store()

        # Index file
        batch = upload_and_index_file(vs_id, file_path)
        
        # Cleanup local file
        os.remove(file_path)

        return {
            "message": "File processed and indexed",
            "vector_store_id": vs_id,
            "file_id": "batch_upload_successful"
        }
    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    # check if a store exists in our DB
    vs_id = get_or_create_vector_store()
    try:
        answer = generate_rag_response(vs_id, request.question)
        return {
            "answer": answer,
            "vector_store_id": vs_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
