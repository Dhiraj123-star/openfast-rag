from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    vector_store_id: Optional[str] = None

class UploadResponse(BaseModel):
    message: str
    vector_store_id: str
    file_id: str