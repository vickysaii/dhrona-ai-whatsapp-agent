# 🤖 Dhrona AI - WhatsApp AI Business Agent

An AI-powered WhatsApp Business Agent built using FastAPI, Supabase, Retrieval-Augmented Generation (RAG), and Large Language Models (Groq). The agent automatically answers customer queries using a business knowledge base uploaded by the admin.

---

## 🚀 Features

- 💬 WhatsApp Cloud API Integration
- 🧠 AI-Powered Customer Support
- 📚 RAG (Retrieval-Augmented Generation)
- 📄 Knowledge Base Upload (PDF, DOCX, TXT, CSV)
- 🔍 Semantic Search using Embeddings
- 🤖 Groq LLM Integration
- 💾 Supabase Database
- 👤 Customer Session Management
- 📝 Conversation History
- 📊 Admin Dashboard APIs
- 🔐 JWT Authentication
- ⚡ FastAPI Backend
- 🌐 Webhook Support
- 🐳 Docker Ready

---

# 🏗 Architecture

```
Customer
      │
      ▼
WhatsApp
      │
      ▼
Meta Cloud API
      │
      ▼
FastAPI Webhook
      │
      ▼
Business Agent
      │
 ┌────┴─────────────┐
 │                  │
 ▼                  ▼
Conversation     Knowledge Base
History          (Supabase)
 │                  │
 └──────► RAG ◄─────┘
           │
           ▼
      Groq LLM
           │
           ▼
 WhatsApp Response
```

---

# 🛠 Tech Stack

### Backend

- FastAPI
- Python
- Uvicorn

### AI

- Groq LLM
- FastEmbed
- RAG
- Prompt Engineering

### Database

- Supabase
- PostgreSQL
- pgvector

### WhatsApp

- Meta WhatsApp Cloud API
- Webhooks

### Deployment

- Docker
- Railway (Planned)
- Vercel (Frontend)

---

# 📂 Project Structure

```
backend
│
├── app
│   ├── agents
│   ├── api
│   ├── repositories
│   ├── schemas
│   ├── services
│   ├── middleware
│   ├── utils
│   └── core
│
├── tests
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
SUPABASE_URL=
SUPABASE_KEY=

GROQ_API_KEY=

WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_VERIFY_TOKEN=

JWT_SECRET=
```

---

# 🚀 Installation

```bash
git clone https://github.com/your-username/dhrona-ai-business-agent.git

cd dhrona-ai-business-agent/backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

# 📡 API

FastAPI Docs

```
http://localhost:8000/docs
```

---

# 🎯 Future Roadmap

- Multi-business support
- Human handoff
- Voice message support
- Image understanding
- Appointment booking
- Analytics Dashboard
- SaaS Platform

---

# 👨‍💻 Author

**Virupaksh Annarapu**

AI Engineer | Generative AI | Agentic AI | FastAPI | RAG | LLMs

---

# ⭐ If you like this project

Give it a ⭐ on GitHub.