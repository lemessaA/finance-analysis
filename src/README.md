# 🤖 AI Business Intelligence Platform

A full-stack Agentic AI platform combining **Startup Idea Validation**, **Financial Report Analysis**, and **Financial Forecasting** — powered by LangChain, LangGraph, FastAPI, and Next.js.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Frontend                     │
│  Dashboard │ Startup Validator │ Reports │ Forecasting  │
└─────────────────────────┬───────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────┐
│                  FastAPI Backend                         │
│                                                         │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ Startup         │  │ Financial    │  │ Forecast  │  │
│  │ Validator Graph │  │ Analyzer     │  │ Engine    │  │
│  │ (LangGraph)     │  │ (PyMuPDF)    │  │ (sklearn) │  │
│  └─────────────────┘  └──────────────┘  └───────────┘  │
│                                                         │
│  Market │ Competitor │ Decision │ Financial │ Forecast   │
│  Agent  │ Agent      │ Agent    │ Agent     │ Agent      │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)

### 1. Clone & Configure
```bash
cp .env.example .env
# Fill in your GROQ_API_KEY and TAVILY_API_KEY
```

### 2. Run with Docker
```bash
docker-compose up --build
```

### 3. Run Locally

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 4. Open
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## 🧠 Agents

| Agent | Role |
|-------|------|
| `MarketResearchAgent` | TAM/SAM analysis, trend research via Tavily |
| `CompetitorAgent` | Competitor landscape & positioning |
| `FinancialAnalysisAgent` | Metric extraction from PDFs |
| `ForecastingAgent` | ML-based financial forecasting interpretation |
| `DecisionAgent` | Synthesis & final scoring |

## 📂 Project Structure

```
ai-business-intelligence-platform/
├── backend/         # FastAPI + LangGraph backend
├── frontend/        # Next.js 14 App Router frontend
├── infrastructure/  # Nginx, monitoring, deployment
└── docs/            # Architecture & API documentation
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key (llama3-70b-8192) |
| `TAVILY_API_KEY` | Tavily search API key |
| `DATABASE_URL` | PostgreSQL connection string |
| `NEXT_PUBLIC_API_URL` | Backend URL for frontend |

## 📄 License

MIT
