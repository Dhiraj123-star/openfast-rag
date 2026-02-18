# 🚀 OpenFast-RAG

**OpenFast-RAG** is a high-performance, lightweight Retrieval-Augmented Generation (RAG) engine. It bridges the gap between your private documents and OpenAI’s reasoning capabilities using a modern FastAPI interface, persistent local storage, and a **real-time interactive dashboard.**

### ✨ Key Features

* **Interactive Chat Dashboard**: A modern, front-end interface built with **Jinja2 templates** for seamless document interaction.
* **Real-Time SSE Streaming**: Leverages **Server-Sent Events (SSE)** to stream RAG responses token-by-token.
* **Automated CI/CD**: Fully integrated with **GitHub Actions** to build and push the production-ready Docker image to Docker Hub automatically on every push.
* **Ultra-Slim Docker Image**: Optimized using **multi-stage builds** to ensure a minimal footprint (~100MB) and fast deployment.
* **Persistent Knowledge Base**: Uses a local **SQLite** database to remember your Vector Store ID across server restarts.
* **Context-Aware Reasoning**: Uses the latest **OpenAI Responses API** with `file_search` for accurate, grounded answers.

---

### 🛠️ Functionality Overview

#### 1. CI/CD & Automation

The project includes a GitHub Actions workflow that automates the deployment lifecycle:

* **Multi-Stage Build**: Compiles dependencies in a build stage and copies only the essentials to the runtime image.
* **Push**: Tags and pushes the image to `dhiraj918106/openfast_rag_container`.
* **Pull Policy**: Configured to always fetch the `latest` image from the registry during deployment.

#### 2. Real-Time Streaming (`/chat/stream`)

Uses asynchronous generators to push data chunks to the UI as they are generated, providing an instant feedback loop for the user.

---

### 🚦 Quick Start (Docker - Recommended)

1. **Environment Setup**:
Add your API key to a `.env` file in the root:
```bash
OPENAI_API_KEY=sk-proj-xxxx...

```


2. **Launch with Docker**:
The system is configured to always pull the latest optimized image:
```bash
docker-compose pull && docker-compose up -d

```


3. **Access the Dashboard**:
Navigate to `http://localhost:8000/` for the Chat UI.

---

### 📂 API Endpoints Summary

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | **Interactive Chat Dashboard (UI)** |
| `GET` | `/chat/stream` | **SSE Stream for real-time responses** |
| `POST` | `/upload` | Upload and index a new document |
| `GET` | `/admin/status` | View current store and all account stores |
| `DELETE` | `/admin/reset` | Wipe active store and clear local DB |

---

### 📦 CI/CD Deployment Info

**Docker Hub Repository**: `dhiraj918106/openfast_rag_container`

**Image Optimization**: Multi-stage Python 3.11-slim

**Pull Policy**: `always`

---
