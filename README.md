# 🚀 OpenFast-RAG

**OpenFast-RAG** is a high-performance, lightweight Retrieval-Augmented Generation (RAG) engine. It bridges the gap between your private documents and OpenAI’s reasoning capabilities using a modern FastAPI interface, persistent local storage, and a **real-time interactive dashboard.**

### ✨ Key Features

* **Interactive Chat Dashboard**: A modern, front-end interface built with **Jinja2 templates** for seamless document interaction.
* **Real-Time SSE Streaming**: Leverages **Server-Sent Events (SSE)** to stream RAG responses token-by-token.
* **Automated CI/CD**: Integrated with **GitHub Actions** for automated builds and pushes to Docker Hub.
* **Kubernetes Ready**: Now includes modular **K8s manifests** for deployment on clusters like **Minikube**, featuring persistent storage and secret management.
* **Ultra-Slim Docker Image**: Optimized using **multi-stage builds** (~100MB) for rapid deployment.
* **Persistent Knowledge Base**: Uses a local **SQLite** database and K8s **Persistent Volume Claims (PVC)** to ensure data continuity.

---

### 🛠️ Functionality Overview

#### 1. Kubernetes Migration (`/k8s`)

The project has shifted from simple Docker Compose to a production-ready Kubernetes structure:

* **`deployment.yaml`**: Manages app scaling and lifecycle.
* **`service.yaml`**: Exposes the app via NodePort for local access.
* **`pvc.yaml`**: Ensures the SQLite database survives pod restarts.
* **`secrets.yaml`**: Securely handles sensitive API keys (excluded from source control).

#### 2. Real-Time Streaming (`/chat/stream`)

Uses asynchronous generators to push data chunks to the UI as they are generated, providing an instant feedback loop.

---

### 🚦 Quick Start (Kubernetes/Minikube)

1. **Secret Setup**:
Create your secret locally (or use a `secrets.yaml` and add to `.gitignore`):

```bash
kubectl create secret generic rag-secrets --from-literal=OPENAI_API_KEY='your-key-here'

```

2. **Deploy to Cluster**:

```bash
kubectl apply -f k8s/

```

3. **Access the Dashboard**:

```bash
minikube service openfast-rag-service --url

```

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

### 📦 Infrastructure Info

* **Docker Hub**: `dhiraj918106/openfast_rag_container`
* **Orchestration**: Kubernetes (Minikube compatible)
* **Storage**: Persistent Volume Claim (1Gi)

---
