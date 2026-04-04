# Financial Analysis Platform - AI-Powered Report Analyzer

An advanced, AI-powered platform for parsing, analyzing, and deriving actionable insights from financial reports (PDFs). Built with a modern FastAPI backend powered by Langchain/LangGraph and a sleek Next.js frontend, this tool extracts vital financial metrics, performs industry benchmarking, identifies risks, and projects future trends automatically.

## 🌟 Key Features

- **Automated Data Extraction**: Upload any company financial report (PDF) and instantly extract core metrics (Revenue, Net Profit, Operating Income, Assets, Liabilities, Margins, etc.).
- **Advanced Financial Analysis**: Get a comprehensive, CFA-level narrative analysis of the financial state driven by OSS language models (via Groq).
- **Health Scoring & Risk Assessment**: Automatically calculates a unified "Financial Health Score" and surfaces immediate liquidity, leverage, or profitability risks.
- **Industry Benchmarking**: Compare extracted metrics against hardcoded industry benchmarks (Technology, Manufacturing, Retail, etc.) to assess relative performance.
- **Trend & Predictive Insights**: Calculates historical trends and forecasts future revenue/profit performance based on historical reporting.
- **Interactive Dashboard**: A beautiful, dark-mode First Next.js UI styled with TailwindCSS for seamless document uploading and reading.

## 💻 Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **AI & Orchestration**: [LangChain](https://python.langchain.com/) / [LangGraph](https://python.langchain.com/docs/langgraph)
- **LLM Provider**: [Groq](https://groq.com/) (using extremely fast open-source models)
- **Data Validation**: Pydantic v2
- **PDF Extraction**: PyMuPDF (`fitz`)

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) (React)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **API Client**: Axios

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python 3.10+
- A Groq API Key (`GROQ_API_KEY`)

### 1. Backend Setup

Navigate to the backend directory and set up a virtual environment:

```bash
cd src/backend

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```
*The backend API will be running at `http://localhost:8000` with Swagger documentation available at `http://localhost:8000/docs`.*

### 2. Frontend Setup

Navigate to the frontend directory:

```bash
cd src/frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
*The frontend application will be running at `http://localhost:3000`.*

---

## ⚙️ Environment Variables

### Backend (`src/backend/.env`)
Create a `.env` file in the `src/backend` directory:
```env
APP_NAME="Business Insights"
VERSION="1.0.0"
ENVIRONMENT="development"
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL="openai/gpt-oss-20b"  # Or your chosen model
ALLOWED_ORIGINS="http://localhost:3000"
```

## 🏗️ Architecture

The platform uses an intelligent pipeline to process files:
1. **Frontend**: Receives the PDF through a drag-and-drop React interface.
2. **FastAPI Route**: The file hits the `/api/v1/advanced/analyze-advanced` endpoint.
3. **Extraction**: Text is extracted locally using PyMuPDF.
4. **Agentic Processing**: `FinancialAnalysisAgent` leverages structured outputs with LangChain to pull accurate Pydantic models (metrics, risks).
5. **Advanced Engine**: The `AdvancedFinancialAnalyzer` processes those raw metrics to generate ratios, benchmarks, health scores, and predictive forecasts.
6. **Result**: The fully enriched JSON is returned and visualized on the client.

## 📝 License
This project is for educational and business analysis use cases.
