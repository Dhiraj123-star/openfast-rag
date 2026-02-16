# 🚀 OpenFast-RAG

**OpenFast-RAG** is a high-performance, lightweight Retrieval-Augmented Generation (RAG) engine. It bridges the gap between your private documents and OpenAI’s reasoning capabilities using a modern FastAPI interface and persistent local storage.

### ✨ Key Features

* **Persistent Knowledge Base**: Uses a local **SQLite** database to remember your Vector Store ID. Even if you restart the server or the Docker container, your knowledge base remains connected.
* **Instant Document Indexing**: Upload PDFs, TXT, or Docx files directly via API. The system handles secure transmission to OpenAI's managed infrastructure.
* **Admin Dashboard**: Dedicated endpoints to list all indexed files, view all vector stores in your account, and perform system resets.
* **Dockerized Infrastructure**: Fully containerized with `docker-compose`, including volume mapping for data persistence and environment isolation.
* **Context-Aware Querying**: Leverages **OpenAI Responses API** with `file_search` for grounded, accurate answers based strictly on your data.
* **Zero-Footprint Policy**: Local files are automatically purged after cloud indexing, keeping your storage clean.

---

### 🛠️ Functionality Overview

#### 1. Ingestion & Persistence (`/upload`)

The system saves document metadata to a local `storage.db`. It performs a handshake with OpenAI to ensure a Vector Store exists, then indexes your files.

#### 2. RAG Query Interface (`/ask`)

Questions are processed through a retrieval-augmented loop. The system automatically fetches the persistent Store ID from the database to ensure continuity across sessions.

#### 3. Admin Control Panel (`/admin`)

* **Status**: View active store details, file counts, and all account-wide vector stores.
* **Targeted Deletion**: Remove specific Vector Stores by ID or delete individual files within a store.
* **System Reset**: A "Nuclear Option" to wipe the active store and reset the local database.

---

### 🚦 Quick Start (Docker - Recommended)

1. **Environment Setup**:
Add your API key to a `.env` file in the root:
```bash
OPENAI_API_KEY=sk-proj-xxxx...

```


2. **Launch with Docker**:
```bash
docker-compose up --build

```


3. **Access the API**:
Navigate to `http://localhost:8000/docs` to access the interactive Swagger UI.

---

### 📂 API Endpoints Summary

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/upload` | Upload and index a new document |
| `POST` | `/ask` | Query your documents using RAG |
| `GET` | `/admin/status` | View current store and all account stores |
| `DELETE` | `/admin/delete/{id}` | Permanently delete a specific Vector Store |
| `DELETE` | `/admin/files/{id}` | Remove a specific file from the active store |
| `DELETE` | `/admin/reset` | Wipe active store and clear local DB |

---
