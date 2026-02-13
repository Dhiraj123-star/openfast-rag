# 🚀 OpenFast-RAG

**OpenFast-RAG** is a high-performance, lightweight Retrieval-Augmented Generation (RAG) engine. It bridges the gap between your private documents and OpenAI’s reasoning capabilities using a modern FastAPI interface.

### ✨ Key Features

* **Instant Document Indexing**: Upload PDFs, TXT, or Docx files directly via API. The system handles local buffering and secure transmission to the cloud.
* **Serverless Vector Management**: Leverages **OpenAI Vector Stores** to handle embeddings, chunking, and storage. No complex database (like Pinecone or Milvus) is required.
* **Context-Aware Querying**: Uses the latest **OpenAI Responses API** with `file_search` tools to provide answers grounded strictly in your uploaded data.
* **Asynchronous Processing**: Built on **FastAPI**, allowing for non-blocking file uploads and high-concurrency query handling.
* **Automatic Cleanup**: Implements a "Zero-Footprint" policy where temporary local files are purged immediately after cloud indexing is confirmed.
* **Auto-Generated Documentation**: Comes with a built-in **Swagger UI** for testing endpoints without writing a single line of frontend code.

---

### 🛠️ Functionality Overview

#### 1. Ingestion Engine (`/upload`)

The system accepts multipart file uploads. It performs a "Handshake" with OpenAI to create a managed Vector Store, uploads the document, and polls the status until the document is fully indexed and searchable.

#### 2. RAG Query Interface (`/ask`)

Once a document is indexed, the system transitions into "Consultant Mode." It takes natural language questions, performs a semantic search across your Vector Store, and returns a response that cites your specific document's context.

#### 3. Managed Knowledge Base

The system is designed to "remember" the active Vector Store ID across requests, ensuring that subsequent questions always point to the correct knowledge silo.

---

### 🚦 Quick Start

1. **Environment Setup**:
Add your API key to a `.env` file:
```bash
OPENAI_API_KEY=sk-proj-xxxx...

```


2. **Install Dependencies**:
```bash
pip install -r requirements.txt

```


3. **Launch the API**:
```bash
uvicorn app.main:app --reload

```


4. **Interactive Testing**:
Navigate to `http://127.0.0.1:8000/docs` to start uploading documents and asking questions through the interactive UI.

---
