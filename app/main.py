import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models import QueryRequest, QueryResponse, UploadResponse
from app.openai_utils import (
    init_db,
    get_or_create_vector_store,
    upload_and_index_file,
    generate_rag_response,
    list_indexed_files,
    list_all_vector_stores,
    delete_vector_store,
    delete_specific_vector_store,
    remove_file_from_store
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

@app.get("/admin/status")
async def get_admin_status():
    """Returns details of the current store and all stores in the account. """
    current_vs_id = get_or_create_vector_store()
    try:
        current_files = list_indexed_files(current_vs_id)
        all_stores = list_all_vector_stores()

        return {
            "active_store":{
                "id":current_vs_id,
                "files":current_files,
                "file_count":len(current_files)
            },
            "account_overview":{
                "total_vector_stores":len(all_stores),
                "all_stores":all_stores
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.delete("/admin/reset")
async def reset_system():
    """Deletes the current vector store and resets the local database."""
    current_vs_id = get_or_create_vector_store()
    try:
        delete_vector_store(current_vs_id)
        return {"message":f"Vector Store {current_vs_id} deleted and local database reset."}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Reset failed: {str(e)}")

@app.delete("/admin/delete{vector_id}")
async def delete_vector_id(vector_id: str):
    """Deletes a specific Vector Store ID from OpenAI and resets local DB if it was active."""
    try:
        delete_specific_vector_store(vector_id)
        return {"message":f"Vector Store {vector_id} has been permanently deleted."}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Deletion failed: {str(e)}")

@app.delete("/admin/files/{file_id}")
async def delete_file(file_id: str):
    vs_id = get_or_create_vector_store()
    try:
        remove_file_from_store(vs_id,file_id)
        return {"message":f"File {file_id} removed from store {vs_id}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))