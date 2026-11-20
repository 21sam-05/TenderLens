# TenderLens — AI Tender Intelligence & Bid Readiness Platform

An AI-powered tender intelligence platform that helps small businesses and contractors understand government tenders, evaluate bid eligibility, identify compliance gaps, and make informed bidding decisions using Generative AI and Retrieval-Augmented Generation (RAG).

TenderLens combines document intelligence, semantic search, LLM-powered analysis, and a complete containerized DevOps deployment workflow.

---

## Overview

Government tender documents are often lengthy, complex, and difficult for small businesses to evaluate manually.

TenderLens simplifies this process by allowing users to upload tender documents, extract important requirements, ask contextual questions, and assess their readiness to submit a bid.

The platform uses a Retrieval-Augmented Generation pipeline to retrieve relevant information from tender documents and generate context-aware responses using Google's Gemini API.

## Key Features

- **Tender Document Processing:** Upload and process PDF tender documents.
- **Intelligent Text Extraction:** Extract, clean, and organize information from tender documents using PyMuPDF.
- **Semantic Search:** Generate embeddings and retrieve relevant document sections using PostgreSQL and pgvector.
- **AI-Powered Question Answering:** Ask natural-language questions about uploaded tenders using Gemini.
- **Tender Intelligence:** Extract important tender information into structured outputs.
- **Bid Readiness Analysis:** Evaluate eligibility requirements and identify potential compliance gaps.
- **Tender Management:** Create, view, search, filter, and delete tenders.
- **Company Profiles:** Maintain company information relevant to bid eligibility and readiness assessment.

---

## System Architecture

```text
                       USER
                         |
                         v
                 React + Vite Frontend
                         |
                         v
                  Django REST API
                         |
              +----------+----------+
              |          |          |
              v          v          v
          Document     Gemini    PostgreSQL
          Processing    API       + pgvector
              |          |          |
              v          v          v
          Text       AI Analysis   Vector
          Extraction              Retrieval
              |
              v
         Text Cleaning
              |
              v
       Section-aware Chunking
              |
              v
       Gemini Embeddings
              |
              v
        pgvector Storage
              |
              v
       Semantic Retrieval
              |
              v
        Context Assembly
              |
              v
        Gemini Response
              |
              v
         Frontend UI
```

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, JavaScript, Vite |
| Backend | Python, Django, Django REST Framework |
| Database | PostgreSQL |
| Vector Database | pgvector |
| AI / LLM | Google Gemini API |
| Embeddings | Gemini Embedding API |
| Document Processing | PyMuPDF |
| Backend Server | Gunicorn |
| Frontend Server | Nginx |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Container Registry | GitHub Container Registry (GHCR) |
| Orchestration | Kubernetes |
| Development Environment | Windows, Git Bash |

---

# DevOps & Deployment Architecture

TenderLens includes a containerized deployment workflow with automated CI checks, container image publishing, and Kubernetes orchestration.

## 1. Docker & Docker Compose

The application is containerized using separate backend and frontend Docker images.

Docker Compose integrates:

- React frontend served through Nginx.
- Django backend served through Gunicorn.
- PostgreSQL with pgvector.
- Environment-based configuration.
- Container health checks.
- Persistent PostgreSQL storage.

The database uses a persistent Docker volume to preserve data across container restarts.

## 2. CI/CD with GitHub Actions

GitHub Actions automates the application validation and container image publishing workflow.

The CI pipeline performs:

1. Backend environment setup and Django validation.
2. Frontend dependency installation.
3. Frontend production build.
4. Docker image publishing to GitHub Container Registry.

The container images are published to GHCR:

```text
ghcr.io/21sam-05/tenderlens-backend:latest

ghcr.io/21sam-05/tenderlens-frontend:latest
```

## 3. Kubernetes Deployment

TenderLens is deployed locally on Kubernetes using Docker Desktop.

Kubernetes manages the frontend and backend application workloads independently.

### Kubernetes Resources

| Resource | Purpose |
|---|---|
| Namespace | Isolates TenderLens resources |
| ConfigMap | Stores non-sensitive configuration |
| Secret | Stores application credentials |
| Backend Deployment | Manages Django application Pods |
| Backend Service | Internal backend communication |
| Frontend Deployment | Manages React/Nginx Pods |
| Frontend Service | Exposes frontend internally |

### Kubernetes Architecture

```text
                   LOCAL BROWSER
                         |
                         |
                   localhost:8080
                         |
                         v
                FRONTEND SERVICE
                         |
                         v
               FRONTEND DEPLOYMENT
                    React + Nginx
                         |
                         |
                   localhost:8000
                         |
                         v
                BACKEND SERVICE
                         |
                         v
               BACKEND DEPLOYMENT
                  Django + Gunicorn
                         |
                  +------+------+
                  |             |
                  v             v
             PostgreSQL     Gemini API
              + pgvector
                  |
                  v
          Persistent Docker Volume
```

### Kubernetes Configuration

The Kubernetes manifests are maintained separately inside the repository.

```text
k8s/
│
├── namespace.yaml
├── kustomization.yaml
│
├── config/
│   ├── configmap.yaml
│   └── secret.yaml.example
│
├── backend/
│   ├── deployment.yaml
│   └── service.yaml
│
├── frontend/
│   ├── deployment.yaml
│   └── service.yaml
│
└── networking/
    └── ingress.yaml
```

### Reliability & Resource Management

The Kubernetes workloads include:

- Liveness and readiness probes.
- CPU and memory requests and limits.
- Automatic container restart policies.
- Rolling update deployment strategies.
- Kubernetes Services for internal communication.
- Secret-based sensitive configuration.
- GHCR image pulling configuration where required.

### Database Connectivity

PostgreSQL with pgvector continues running through the existing Docker Compose configuration.

Kubernetes connects to the existing database through:

```text
host.docker.internal:5433
```

This approach avoids deploying PostgreSQL as a disposable Kubernetes Pod and preserves the existing database volume.

### Local Application Access

The current Docker Desktop deployment uses Kubernetes port forwarding:

```bash
kubectl port-forward -n tenderlens \
  svc/tenderlens-frontend 8080:80

kubectl port-forward -n tenderlens \
  svc/tenderlens-backend 8000:8000
```

Application URL:

```text
http://localhost:8080
```

---

# Getting Started

## Prerequisites

- Python 3.12+
- Node.js 22+
- Docker Desktop
- Docker Compose
- Kubernetes enabled in Docker Desktop
- kubectl
- Git
- Google Gemini API key

## 1. Clone the Repository

```bash
git clone https://github.com/21sam-05/TenderLens.git

cd TenderLens
```

## 2. Environment Configuration

Create a local `.env` file containing the required application configuration.

Configure the Django database settings, Django secret key, and Gemini API key.

Never commit `.env` or application credentials to GitHub.

## 3. Run with Docker Compose

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

## 4. Deploy on Kubernetes

Make sure Docker Desktop Kubernetes is enabled and your cluster is available.

Apply the Kubernetes resources:

```bash
kubectl apply -k k8s/
```

Create the application Secret locally:

```bash
kubectl create secret generic tenderlens-secrets \
  --namespace=tenderlens \
  --from-env-file=.env \
  --dry-run=client -o yaml | kubectl apply -f -
```

Wait for deployments:

```bash
kubectl rollout status deployment/tenderlens-backend \
  -n tenderlens --timeout=180s

kubectl rollout status deployment/tenderlens-frontend \
  -n tenderlens --timeout=180s
```

Expose the application:

```bash
kubectl port-forward -n tenderlens \
  svc/tenderlens-frontend 8080:80
```

In a second terminal:

```bash
kubectl port-forward -n tenderlens \
  svc/tenderlens-backend 8000:8000
```

Open:

```text
http://localhost:8080
```

For private GHCR packages, create the `ghcr-pull-secret` in the `tenderlens` namespace and configure it in the Deployments before applying them.

---

# Kubernetes Verification

Check Pods:

```bash
kubectl get pods -n tenderlens
```

Check Deployments:

```bash
kubectl get deployments -n tenderlens
```

Check Services:

```bash
kubectl get services -n tenderlens
```

Check backend logs:

```bash
kubectl logs deployment/tenderlens-backend -n tenderlens
```

Check frontend logs:

```bash
kubectl logs deployment/tenderlens-frontend -n tenderlens
```

Check application health:

```bash
curl http://127.0.0.1:8000/health/
```

Verify PostgreSQL and pgvector connectivity:

```bash
kubectl exec deployment/tenderlens-backend -n tenderlens -- \
  python manage.py shell -c \
  "from django.db import connection; c=connection.cursor(); c.execute(\"SELECT extversion FROM pg_extension WHERE extname='vector'\"); print(c.fetchone())"
```

---

# Project Structure

```text
TenderLens/
│
├── backend/
│   ├── config/
│   ├── users/
│   ├── tenders/
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
│
├── k8s/
│   ├── namespace.yaml
│   ├── kustomization.yaml
│   ├── config/
│   ├── backend/
│   ├── frontend/
│   └── networking/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# Engineering Highlights

TenderLens demonstrates practical implementation of:

- Full-stack application development using React and Django REST Framework.
- Retrieval-Augmented Generation (RAG) architecture.
- Document extraction, cleaning, and section-aware chunking.
- Embedding generation and vector similarity retrieval.
- LLM integration using the Gemini API.
- PostgreSQL and pgvector integration.
- Containerization with Docker.
- Multi-container orchestration using Docker Compose.
- Automated CI workflows using GitHub Actions.
- Container image publishing using GHCR.
- Kubernetes Deployments, Services, ConfigMaps, and Secrets.
- Application health monitoring through Kubernetes probes.
- Persistent database connectivity across containerized environments.

---

## Author

**Samridhi Saxena**

B.Tech Computer Science & Engineering (AI & ML)

VIT Bhopal University

GitHub: [21sam-05](https://github.com/21sam-05)

LinkedIn: (https://www.linkedin.com/in/samridhi-saxena-07231a28a/)

E-mail: saxenasamridhi1921@gmail.com

Phone: 📞-+91 9540934924

---

**TenderLens — Turning complex tenders into actionable bidding intelligence.**
