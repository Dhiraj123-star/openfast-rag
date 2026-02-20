# 🚀 OpenFast-RAG

**OpenFast-RAG** is a high-performance, lightweight Retrieval-Augmented Generation (RAG) engine. It bridges the gap between your private documents and OpenAI’s reasoning capabilities using a modern FastAPI interface, persistent local storage, and a **real-time interactive dashboard.**

### ✨ Key Features

* **Interactive Chat Dashboard**: A modern, front-end interface built with **Jinja2 templates** for seamless document interaction.
* **Real-Time SSE Streaming**: Leverages **Server-Sent Events (SSE)** to stream responses token-by-token for a "ChatGPT-like" experience.
* **Production-Grade Kubernetes**: Modular **K8s manifests** optimized for Minikube, featuring Ingress routing, health probes, and resource limits.
* **Secure HTTPS Access**: End-to-end encryption using **TLS/SSL certificates** for the `rag.local` domain.
* **Ultra-Slim Docker Image**: Optimized via **multi-stage builds** (~100MB) to ensure fast pulls and minimal overhead.
* **Persistent Knowledge Base**: Uses **SQLite** and K8s **Persistent Volume Claims (PVC)** to ensure data survives pod restarts.

---

### 🛠️ Functionality Overview

#### 1. Kubernetes Infrastructure (`/k8s`)

The system is architected for scalability and reliability:

* **`ingress.yaml`**: Manages secure HTTPS traffic and routes `rag.local` to the internal service.
* **`deployment.yaml`**: Configures self-healing via liveness/readiness probes and resource quotas.
* **`pvc.yaml`**: Ensures persistent storage for the RAG knowledge base.
* **`secrets.yaml`**: Securely handles sensitive API keys and TLS certificates.

#### 2. Real-Time Streaming (`/chat/stream`)

Uses asynchronous generators to push data chunks to the UI as they are generated, providing an instant feedback loop for the user.

---

### 🚦 Quick Start (Kubernetes / Minikube)

1. **Prepare Minikube**:
```bash
minikube start
minikube addons enable ingress

```


2. **Security & Secret Setup**:
```bash
# Generate self-signed SSL certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout rag-local.key -out rag-local.crt -subj "/CN=rag.local"

# Create TLS Secret
kubectl create secret tls rag-tls-secret --key rag-local.key --cert rag-local.crt

# Create OpenAI Secret
kubectl create secret generic rag-secrets --from-literal=OPENAI_API_KEY='your-key-here'

```


3. **Deploy & Map Domain**:
```bash
kubectl apply -f k8s/

# Map Minikube IP to rag.local
echo "$(minikube ip) rag.local" | sudo tee -a /etc/hosts

```


4. **Access the Dashboard**:
Navigate to **`https://rag.local`** (Accept the self-signed certificate warning).

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
* **Orchestration**: Kubernetes
* **Security**: TLS/SSL Encryption (HTTPS)
* **Storage**: 1Gi Persistent Volume Claim

---

