import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi import Request
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
    remove_file_from_store,
    generate_rag_response_stream
)

# Setup Templates
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="OpenFast-RAG", lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Serves the chat dashboard"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/chat/stream")
async def chat_stream(question: str):
    # Added await here
    vs_id = await get_or_create_vector_store()

    async def event_generator():
        try:
            async for chunk in generate_rag_response_stream(vs_id, question):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            # Send the error to the frontend so it doesn't just hang
            error_msg = "Request timed out. Please try again in a moment." if "timeout" in str(e).lower() else str(e)
            yield f"data: ⚠️ Error: {error_msg}\n\n"
        yield "data: [DONE]\n\n"
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"
    
    # Save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Added await here
        vs_id = await get_or_create_vector_store()

        # Index file
        await upload_and_index_file(vs_id, file_path)
        
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
    # Added await here
    vs_id = await get_or_create_vector_store()
    try:
        answer = await generate_rag_response(vs_id, request.question)
        return {
            "answer": answer,
            "vector_store_id": vs_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/status")
async def get_admin_status():
    """Returns details of the current store and all stores in the account. """
    # Added await here
    current_vs_id = await get_or_create_vector_store()
    try:
        # Added await to both list helper functions
        current_files = await list_indexed_files(current_vs_id)
        all_stores = await list_all_vector_stores()

        return {
            "active_store": {
                "id": current_vs_id,
                "files": current_files,
                "file_count": len(current_files)
            },
            "account_overview": {
                "total_vector_stores": len(all_stores),
                "all_stores": all_stores
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/reset")
async def reset_system():
    """Deletes the current vector store and resets the local database."""
    # Added await here
    current_vs_id = await get_or_create_vector_store()
    try:
        # Added await here
        await delete_vector_store(current_vs_id)
        return {"message": f"Vector Store {current_vs_id} deleted and local database reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@app.delete("/admin/delete/{vector_id}")
async def delete_vector_id(vector_id: str):
    """Deletes a specific Vector Store ID from OpenAI and resets local DB if it was active."""
    try:
        # Added await here
        await delete_specific_vector_store(vector_id)
        return {"message": f"Vector Store {vector_id} has been permanently deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

@app.delete("/admin/files/{file_id}")
async def delete_file(file_id: str):
    # Added await here
    vs_id = await get_or_create_vector_store()
    try:
        # Added await here
        await remove_file_from_store(vs_id, file_id)
        return {"message": f"File {file_id} removed from store {vs_id}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/chat")
async def upload_chat_document(file: UploadFile = File(...)):
    """Special upload endpoint for the Chat UI that returns clean JSON. """
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        # Added await here
        vs_id = await get_or_create_vector_store()
        await upload_and_index_file(vs_id, file_path)
        os.remove(file_path)
        return {"filename": file.filename, "status": "success"}
    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        return {"status": "error", "detail": str(e)}
    