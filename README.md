# AI Customer Support RAG

A production-ready Retrieval-Augmented Generation (RAG) customer support platform built with FastAPI, React, PostgreSQL, pgvector, Docker, and the Gemini API.

The system enables organizations to upload their knowledge base, perform semantic search over documents, and provide accurate, source-grounded AI responses through an intuitive web interface.

---

## Preview

### Login

![Login](docs/images/login.png)

### Dashboard

![Dashboard](docs/images/dashboard.png)

### AI Chat

![Chat](docs/images/chat.png)

### Document Management

![Documents](docs/images/documents.png)

### Source Viewer

![Source Viewer](docs/images/source-viewer.png)

### Settings

![Settings](docs/images/settings.png)

---

## Features

- Secure user authentication with JWT
- Upload and manage PDF knowledge base documents
- Automatic text extraction and chunking
- Vector embeddings using Gemini Embeddings
- Semantic search with PostgreSQL pgvector
- Retrieval-Augmented Generation (RAG)
- Source citations for every AI response
- Conversation history
- Configurable AI settings
- Modern responsive React dashboard
- Docker support for development and deployment

---

## Tech Stack

### Backend

- FastAPI
- Python 3.12
- SQLAlchemy
- Alembic
- PostgreSQL
- pgvector
- Pydantic
- JWT Authentication

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Router

### AI

- Gemini 2.5 Flash
- Gemini Embedding API

### DevOps

- Docker
- Docker Compose
- GitHub

---

# Architecture

```text
                        React Frontend
                               │
                               │ REST API
                               ▼
                         FastAPI Backend
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   Authentication        Chat Service       Document Service
                               │
                               ▼
                     Retrieval Service
                               │
                               ▼
                     Embedding Service
                               │
                               ▼
                     Gemini Embeddings
                               │
                               ▼
                    PostgreSQL + pgvector
                               │
                               ▼
                      Similarity Search
                               │
                               ▼
                     Generation Service
                               │
                               ▼
                          Gemini API
                               │
                               ▼
                         AI Response
```

---

# Project Structure

```text
ai-customer-support-rag/
│
├── backend/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── storage/
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── features/
│   │   ├── layouts/
│   │   ├── pages/
│   │   └── types/
│   └── package.json
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env.example
```

---

# Getting Started

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL
- Docker (Optional)
- Gemini API Key

---

## Clone the Repository

```bash
git clone https://github.com/rajab-bett-analytics/ai-customer-support-rag.git

cd ai-customer-support-rag
```

---

## Backend Setup

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Frontend Setup

```bash
cd frontend

npm install
```

---

# Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/rag_db

SECRET_KEY=your_secret_key

GOOGLE_API_KEY=your_api_key

CHAT_MODEL=gemini-2.5-flash

EMBEDDING_MODEL=gemini-embedding-001

UPLOAD_DIRECTORY=storage/uploads
```

---

# Database Migration

```bash
alembic upgrade head
```

---

# Run the Backend

```bash
uvicorn backend.main:app --reload
```

Backend

```
http://localhost:8000
```

---

# Run the Frontend

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# Docker

Build and start the application.

```bash
docker compose up --build
```

Run in detached mode.

```bash
docker compose up -d
```

Stop all containers.

```bash
docker compose down
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | User login |
| GET | `/auth/me` | Current user |
| POST | `/chat` | Chat with AI |
| GET | `/documents` | List documents |
| POST | `/documents/upload` | Upload documents |
| DELETE | `/documents/{id}` | Delete document |
| GET | `/settings` | Get settings |
| PUT | `/settings` | Update settings |

---

# RAG Workflow

1. Upload PDF documents.
2. Extract document text.
3. Split text into chunks.
4. Generate embeddings.
5. Store embeddings in PostgreSQL using pgvector.
6. User submits a question.
7. Generate an embedding for the question.
8. Retrieve the most relevant document chunks.
9. Inject retrieved context into the prompt.
10. Generate an AI response using Gemini.
11. Return the response with supporting document sources.

---

# Roadmap

- Streaming AI responses
- Multiple knowledge bases
- OCR support
- Role-based access control
- Conversation summarization
- Hybrid keyword and vector search
- Redis caching
- Background task processing
- Multi-model AI support
- Kubernetes deployment
- CI/CD pipeline
- Automated testing

---

# Screenshots

Replace the placeholder images with your own screenshots.

```
docs/
└── images/
    ├── dashboard.png
    ├── login.png
    ├── chat.png
    ├── documents.png
    ├── upload.png
    ├── source-viewer.png
    ├── settings.png
```

---

# Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

---

# License

This project is licensed under the MIT License.

---

# Author

**Rajab Cheruiyot Bett**

Data Analyst | Business Intelligence | Data Engineering | AI Applications

- GitHub: https://github.com/rajab-bett-analytics
- LinkedIn: https://www.linkedin.com/in/rajab-bett

---

If you find this project useful, consider giving it a star on GitHub.