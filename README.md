# 🤖 Dhrona AI - WhatsApp AI Business Agent

An enterprise-grade, full-stack WhatsApp AI Business Agent system built with **FastAPI**, **Groq (Llama 3.3 70B)**, **FastEmbed**, **Supabase (pgvector)**, **Redis**, and a modern **React + Vite + Tailwind CSS Admin Dashboard**.

The agent autonomously handles customer queries over WhatsApp 24/7 using a business knowledge base (PDF, DOCX, CSV, TXT) via Retrieval-Augmented Generation (RAG). It also provides business owners with a live conversation interface, human-agent takeover, analytics, and customizable AI settings.

---

## 🚀 Key Features

### 🤖 Intelligent WhatsApp Agent
- **💬 Meta WhatsApp Cloud API Integration**: Real-time webhook verification, message receipt, and asynchronous reply dispatch.
- **⚡ Groq LLM Inference**: Powered by `llama-3.3-70b-versatile` for lightning-fast, high-precision contextual responses.
- **📚 Advanced RAG Engine**:
  - Local embedding generation with **FastEmbed** (`BAAI/bge-small-en-v1.5`) — fast, cost-effective, and free from external API rate limits.
  - Cosine similarity vector search backed by **Supabase `pgvector`** with a custom stored procedure (`match_documents`).
  - Intelligent document processing and recursive chunking with boundary alignment for **PDF, DOCX, CSV, and TXT/MD**.
- **🧠 Conversational Context & Memory**: Rolling multi-turn conversation memory with **Redis** caching and PostgreSQL persistence.
- **🛡️ Fallback & Grounding Guardrails**: Strict prompt engineering and business settings to prevent hallucinations.

### 🖥️ Admin Dashboard (React + Vite + Tailwind CSS)
- **📊 Real-time Dashboard**: Overview statistics (Total Messages, Today's Volume, Active Customers, Tokens Used, Latency) and a built-in agent testing playground.
- **💬 Live Conversations & Human Handoff**: Inspect customer chat threads in real time with a one-click **Human Takeover** toggle that temporarily pauses automated AI replies for agent intervention.
- **📁 Knowledge Base Management**: Drag-and-drop document uploader with status tracking (Uploaded, Processing, Indexed, Failed), chunk counts, and cascade deletion.
- **📈 Analytics & Reporting**: Interactive charts (powered by **Recharts**) visualizing message frequency, response times, and token consumption.
- **⚙️ Business & AI Configuration**:
  - **Business Profile**: Business name, working hours (JSON), contact info, greeting message, and fallback response.
  - **AI Prompt Settings**: System prompt, LLM temperature, and max token limits.
- **🔐 Secure Authentication**: JWT authentication with password hashing and route protection.

### 🐳 DevOps & Deployment
- **Docker Ready**: Dedicated Dockerfiles for both Backend (Python 3.11) and Frontend (Nginx SPA), plus `docker-compose.yml` for unified local or server deployment with Redis.

---

## 🏗 System Architecture

```
                               ┌────────────────────────────────────────┐
                               │       WhatsApp Customer (Mobile)       │
                               └──────────────────┬─────────────────────┘
                                                  │
                                                  ▼
                               ┌────────────────────────────────────────┐
                               │         Meta Cloud API Webhook         │
                               └──────────────────┬─────────────────────┘
                                                  │
                                                  ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ FastAPI Backend (Port 8000)                                                            │
│                                                                                        │
│  ┌───────────────────────┐         ┌────────────────────────────────────────────────┐  │
│  │ Webhook Endpoint      │────────►│ BusinessAgent Orchestrator                     │  │
│  │ (Verification/Events) │         │                                                │  │
│  └───────────────────────┘         │  1. Check / Create Session                     │  │
│                                    │  2. Verify Human Takeover Status               │  │
│  ┌───────────────────────┐         │  3. Generate Query Embedding (FastEmbed)       │  │
│  │ Admin REST APIs       │         │  4. Retrieve Relevant Chunks (pgvector)        │  │
│  │ (/auth, /kb, /chat,   │         │  5. Fetch History (Redis / DB)                 │  │
│  │  /settings, /dash)    │         │  6. Assemble Prompt & Context                  │  │
│  └───────────▲───────────┘         │  7. Generate Response (Groq Llama 3.3)         │  │
│              │                     │  8. Dispatch Reply via WhatsApp Service        │  │
│              │                     └───────┬───────────────────┬────────────────────┘  │
│              │                             │                   │                       │
└──────────────┼─────────────────────────────┼───────────────────┼───────────────────────┘
               │                             │                   │
               ▼                             ▼                   ▼
┌───────────────────────────┐ ┌────────────────────────┐ ┌───────────────────────────────┐
│ React Admin Dashboard     │ │ Supabase (PostgreSQL)  │ │ Redis Memory Store            │
│ (Port 5173 / Nginx 80)    │ │ - pgvector Embeddings  │ │ (Port 6379)                   │
│ - Analytics & Metrics     │ │ - Knowledge Documents  │ │ - Rolling Session History     │
│ - Live Chat & Takeover    │ │ - Chat Sessions & Logs │ │ - Fast Response Cache         │
│ - KB Document Uploader    │ │ - Business & AI Config │ └───────────────────────────────┘
│ - Business & AI Settings  │ └────────────────────────┘
└───────────────────────────┘
```

---

## 🛠 Tech Stack

| Domain | Technologies |
|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn, Pydantic v2, Pydantic Settings, Httpx |
| **LLM & Inference** | Groq (`llama-3.3-70b-versatile`), Prompt Engineering |
| **Embeddings & RAG** | FastEmbed (`BAAI/bge-small-en-v1.5`), PyPDF, python-docx, pandas |
| **Database & Search** | Supabase (PostgreSQL 15+ with `pgvector`), Stored Procedures (`match_documents`) |
| **Caching & Memory** | Redis 7 (Alpine) |
| **Authentication** | JWT (`python-jose`), Passlib, Bcrypt |
| **Frontend Dashboard** | React 18, Vite 5, Tailwind CSS, Lucide React, Recharts, Axios, React Router DOM |
| **Containerization** | Docker, Docker Compose, Nginx |

---

## 📂 Project Structure

```text
dhrona-ai-whatsapp-agent/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   └── business_agent.py      # Core AI Agent orchestration logic
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py          # Admin login, registration, JWT auth
│   │   │       │   ├── chat.py          # Direct agent testing endpoint
│   │   │       │   ├── conversations.py # Chat sessions, history, human takeover
│   │   │       │   ├── dashboard.py     # Metrics and activity stats
│   │   │       │   ├── settings.py      # Business & prompt configuration
│   │   │       │   ├── upload.py        # KB file upload, parsing, embedding & indexing
│   │   │       │   └── webhook.py       # WhatsApp verification & webhook event handler
│   │   │       └── router.py            # API V1 router aggregation
│   │   ├── middleware/
│   │   │   └── auth_middleware.py     # JWT validation dependency
│   │   ├── repositories/
│   │   │   └── db_repo.py             # Supabase & DB query abstraction layer
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── response.py
│   │   │   ├── settings.py
│   │   │   └── whatsapp.py
│   │   ├── services/
│   │   │   ├── document/
│   │   │   │   └── processor.py       # Multi-format parsing (PDF/DOCX/CSV/TXT) & chunking
│   │   │   ├── embeddings/
│   │   │   │   └── fastembed.py       # FastEmbed BGE-small embedding generator
│   │   │   ├── llm/
│   │   │   │   └── groq.py            # Groq API client
│   │   │   ├── memory/
│   │   │   │   └── manager.py
│   │   │   ├── prompt/
│   │   │   │   └── builder.py         # Dynamic prompt constructor with RAG context
│   │   │   ├── whatsapp/
│   │   │   │   └── service.py         # WhatsApp Cloud API client
│   │   │   └── redis_memory.py        # Redis rolling memory store with fallback
│   │   ├── utils/
│   │   │   └── security.py            # Password hashing and token generation
│   │   ├── config.py                  # Pydantic BaseSettings configuration
│   │   ├── database.py                # Supabase client initialization
│   │   └── main.py                    # FastAPI application entry point
│   ├── tests/
│   │   └── test_webhook.py            # Webhook and agent test cases
│   ├── database.sql                   # Supabase schema, tables, and match_documents function
│   ├── requirements.txt               # Backend Python dependencies
│   ├── Dockerfile                     # Backend container image
│   └── .env.example                   # Backend environment template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx             # Top bar with admin profile & quick actions
│   │   │   ├── Layout.jsx             # App layout wrapper with sidebar
│   │   │   ├── Sidebar.jsx            # Navigation links
│   │   │   └── StatCard.jsx           # Reusable metric card
│   │   ├── hooks/
│   │   │   └── useAuth.jsx            # Authentication state hook
│   │   ├── pages/
│   │   │   ├── Analytics.jsx          # Volume, latency, and token charts
│   │   │   ├── Conversations.jsx      # Chat sessions & human takeover view
│   │   │   ├── Dashboard.jsx          # High-level metrics & quick chat tester
│   │   │   ├── KnowledgeBase.jsx      # Document upload & index management
│   │   │   ├── Login.jsx              # Admin authentication screen
│   │   │   └── Settings.jsx           # Business profile & AI prompt settings
│   │   ├── services/
│   │   │   └── api.js                 # Axios instance with auth interceptor
│   │   ├── App.jsx                    # Route definitions
│   │   ├── index.css                  # Tailwind styles
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── Dockerfile                     # Multi-stage Nginx build for frontend
├── docker/
│   └── docker-compose.yml             # Orchestration for Backend + Redis
└── README.md
```

---

## ⚙️ Environment Configuration

### Backend `.env`

Create `backend/.env` (refer to `backend/.env.example`):

```env
# Application Settings
APP_NAME="WhatsApp AI Business Agent"
DEBUG=True
HOST="0.0.0.0"
PORT=8000

# Supabase Configurations
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-supabase-service-role-key"

# Groq API Configuration
GROQ_API_KEY="gsk_your_groq_api_key"
GROQ_MODEL="llama-3.3-70b-versatile"

# Meta WhatsApp Cloud API Configurations
WHATSAPP_PHONE_NUMBER_ID="your-phone-number-id"
WHATSAPP_BUSINESS_ACCOUNT_ID="your-business-account-id"
WHATSAPP_ACCESS_TOKEN="your-meta-system-user-access-token"
WHATSAPP_VERIFY_TOKEN="your_custom_webhook_verify_token"

# Redis Cache Configurations
REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_PASSWORD=""
REDIS_DB=0

# Security & JWT
JWT_SECRET="generate-a-secure-random-string"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Frontend `.env`

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## 💾 Database Setup (Supabase)

1. Open your project on [Supabase](https://supabase.com/).
2. Navigate to the **SQL Editor**.
3. Copy and run the entire contents of [`backend/database.sql`](backend/database.sql).
   This script will:
   - Enable `vector` and `uuid-ossp` extensions.
   - Create tables: `users`, `admins`, `business_settings`, `prompt_settings`, `uploaded_files`, `knowledge_documents`, `faq`, `chat_sessions`, `messages`, `analytics`, `conversation_logs`.
   - Seed default business and prompt configurations.
   - Create the `match_documents(query_embedding, match_threshold, match_count)` RPC function for vector similarity matching.
4. Create a Supabase Storage bucket named `knowledge_base` (set to Private or Public according to your preference).

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ & npm
- Redis server (or Docker)
- Supabase project
- Groq API key ([Groq Console](https://console.groq.com/))
- Meta Developer account with WhatsApp Cloud API configured

---

### Method 1: Local Development

#### 1. Start Redis
```bash
# Using Docker:
docker run -d --name redis-local -p 6379:6379 redis:7-alpine

# Or using local Redis installation:
redis-server
```

#### 2. Start Backend API
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI with live reload
uvicorn app.main:app --reload --port 8000
```
- API will run at: `http://localhost:8000`
- Interactive Swagger Docs: `http://localhost:8000/docs`

#### 3. Start Frontend Admin Dashboard
```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
- Dashboard will run at: `http://localhost:5173`

---

### Method 2: Docker Compose

You can launch the backend and Redis together using Docker Compose:

```bash
cd docker
docker compose up --build -d
```

---

## 📡 API Reference

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/` | Health check & API info | No |
| `GET` | `/api/v1/webhook` | Meta WhatsApp webhook verification challenge | No |
| `POST` | `/api/v1/webhook` | Meta WhatsApp incoming event handler | No |
| `POST` | `/api/v1/chat/` | Test agent prompt & RAG pipeline directly | No |
| `POST` | `/api/v1/auth/login` | Admin login & JWT token generation | No |
| `POST` | `/api/v1/auth/register` | Create an admin user | No |
| `GET` | `/api/v1/auth/me` | Current authenticated admin profile | Yes |
| `POST` | `/api/v1/kb/upload` | Upload & index documents (PDF, DOCX, CSV, TXT) | Yes |
| `GET` | `/api/v1/kb/files` | List all uploaded knowledge documents | Yes |
| `DELETE` | `/api/v1/kb/files/{file_id}`| Delete a document and its indexed vectors | Yes |
| `GET` | `/api/v1/conversations` | List all customer chat sessions | Yes |
| `GET` | `/api/v1/conversations/{session_id}/messages` | Get chat history for a session | Yes |
| `POST` | `/api/v1/conversations/{session_id}/takeover` | Toggle human agent takeover flag | Yes |
| `GET` | `/api/v1/conversations/system/logs` | View RAG retrieval logs & latencies | Yes |
| `GET` | `/api/v1/dashboard/metrics` | Retrieve summary metrics for the dashboard | Yes |
| `GET` | `/api/v1/dashboard/recent-activity`| List recent customer interactions | Yes |
| `GET` | `/api/v1/settings/business` | Get business profile configuration | Yes |
| `PUT` | `/api/v1/settings/business` | Update business profile configuration | Yes |
| `GET` | `/api/v1/settings/prompt` | Get AI system prompt & parameters | Yes |
| `PUT` | `/api/v1/settings/prompt` | Update AI system prompt & parameters | Yes |

---

## 🧪 Testing the Webhook Locally

To connect Meta WhatsApp Cloud API to your local machine:

1. Start an ngrok tunnel:
   ```bash
   ngrok http 8000
   ```
2. In the [Meta App Dashboard](https://developers.facebook.com/):
   - Navigate to **WhatsApp > Configuration**.
   - Set **Callback URL** to: `https://<your-ngrok-subdomain>.ngrok-free.app/api/v1/webhook`
   - Set **Verify Token** to match your `WHATSAPP_VERIFY_TOKEN` in `.env`.
   - Subscribe to the **`messages`** webhook field.
3. Send a test message from WhatsApp to your registered test phone number.

---

## 🎯 Completed Milestones & Future Roadmap

- [x] WhatsApp Cloud API Integration & Webhook Handler
- [x] FastEmbed Local Vector Embeddings (`BAAI/bge-small-en-v1.5`)
- [x] Supabase `pgvector` Semantic Similarity Matching
- [x] Multi-format Document Processing (PDF, DOCX, CSV, TXT)
- [x] Groq LLM Generation (`llama-3.3-70b-versatile`)
- [x] Redis Rolling Session Memory Cache
- [x] Human Agent Takeover Toggle
- [x] React + Vite + Tailwind CSS Admin Dashboard
- [x] Interactive Analytics & Latency Charts
- [x] Business Profile & AI Prompt Configuration via UI
- [x] Docker & Docker Compose Containerization
- [ ] Voice message transcription (Whisper)
- [ ] Inbound image understanding (Vision LLM)
- [ ] Automated appointment booking / calendar integration
- [ ] Multi-tenant SaaS support

---

## 👨‍💻 Author

**Virupaksh Annarapu**  
AI Engineer | Generative AI | Agentic AI | FastAPI | RAG | LLMs  
GitHub: [@vickysaii](https://github.com/vickysaii)

---

## ⭐ If you like this project

Give it a ⭐ on [GitHub](https://github.com/vickysaii/dhrona-ai-whatsapp-agent)!