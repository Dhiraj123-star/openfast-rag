# 🚀 OpenFast-RAG

**OpenFast-RAG** is a high-performance, lightweight Retrieval-Augmented Generation (RAG) engine. It bridges the gap between your private documents and OpenAI’s reasoning capabilities using a modern FastAPI interface, persistent local storage, and a **real-time interactive dashboard.**

### ✨ Key Features

* **Interactive Chat Dashboard**: A modern, front-end interface built with **Jinja2 templates** for seamless document interaction.
* **Real-Time SSE Streaming**: Leverages **Server-Sent Events (SSE)** to stream responses token-by-token for a "ChatGPT-like" experience.
* **Production-Grade Kubernetes**: Modular **K8s manifests** optimized for Minikube, including Ingress routing and health probes.
* **Custom Domain Routing**: Access your engine locally via `http://rag.local` using Kubernetes Ingress.
* **Ultra-Slim Docker Image**: Optimized via **multi-stage builds** (~100MB) to ensure fast pulls and minimal overhead.
* **Persistent Knowledge Base**: Uses **SQLite** and K8s **Persistent Volume Claims (PVC)** so your data survives pod restarts.

---

### 🛠️ Functionality Overview

#### 1. Kubernetes Infrastructure (`/k8s`)

The system is architected for scalability and reliability:

* **`ingress.yaml`**: Routes traffic from `rag.local` to the internal service.
* **`deployment.yaml`**: Defines resource limits, liveness/readiness probes, and scaling.
* **`pvc.yaml`**: Manages a 1Gi persistent volume for the SQLite database.
* **`secrets.yaml`**: (Git-ignored) Securely injects the `OPENAI_API_KEY`.

#### 2. Real-Time Streaming (`/chat/stream`)

Uses asynchronous generators to push data chunks to the UI as they are generated, providing an instant feedback loop for the user.

---

### 🚦 Quick Start (Kubernetes / Minikube)

1. **Prepare Minikube**:
```bash
minikube start
minikube addons enable ingress

```


2. **Secret Setup**:
Create your secret locally:
```bash
kubectl create secret generic rag-secrets --from-literal=OPENAI_API_KEY='your-key-here'

```


3. **Deploy & Map Domain**:
```bash
kubectl apply -f k8s/

# Add Minikube IP to your hosts file
echo "$(minikube ip) rag.local" | sudo tee -a /etc/hosts

```


4. **Access the Dashboard**:
Navigate to **`http://rag.local`** in your browser.

---

### 📂 API Endpoints Summary

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | **Interactive Chat Dashboard (UI)** |
| `GET` | `/chat/stream` | **SSE Stream for real-time responses** |
| `POST` | `/upload` | Upload and index a new document |
| `GET` | `/admin/status` | View current store and system health |
| `DELETE` | `/admin/reset` | Wipe active store and clear local DB |

---

### 📦 Infrastructure Info

* **Docker Hub**: `dhiraj918106/openfast_rag_container`
* **Orchestration**: Kubernetes / Kustomize
* **Local Domain**: `rag.local`
* **Storage**: 1Gi Persistent Volume Claim

---

