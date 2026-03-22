# 🤖 AI Business Intelligence Platform

A comprehensive full-stack Agentic AI platform that combines **Startup Idea Validation**, **Financial Report Analysis**, **Market Intelligence**, and **Financial Forecasting** — powered by LangChain, LangGraph, FastAPI, and Next.js.

---

## 🌟 Key Features

### 🚀 Startup Validation Engine
- **AI-Powered Idea Analysis**: Validate startup ideas using multiple specialized AI agents
- **Market Research Integration**: Real-time market size, growth, and trend analysis via Tavily API
- **Competitor Intelligence**: Automated competitor landscape analysis and positioning insights
- **Decision Scoring**: Comprehensive scoring system with detailed breakdowns and recommendations
- **LangGraph Workflow**: Sophisticated multi-agent orchestration for thorough validation

### 📊 Financial Analysis Suite
- **PDF Report Processing**: Extract and analyze financial metrics from uploaded PDF reports
- **Automated Metric Extraction**: Key financial indicators automatically identified and processed
- **Industry Benchmarking**: Compare performance against industry standards and top performers
- **Visual Analytics**: Interactive charts and graphs for financial data visualization

### 📈 Financial Forecasting
- **ML-Based Predictions**: Machine learning models for revenue and financial forecasting
- **Time Series Analysis**: Historical data analysis for accurate trend prediction
- **Scenario Planning**: Multiple forecasting scenarios with confidence intervals
- **Real-time Updates**: Dynamic forecast adjustments based on new data

### 🎯 Market Intelligence
- **TAM/SAM Analysis**: Total Addressable Market and Serviceable Available Market calculations
- **Market Segmentation**: Detailed breakdown of market segments and opportunities
- **Competitive Landscape**: Comprehensive competitor analysis with strengths/weaknesses
- **Opportunity Scoring**: AI-powered assessment of market opportunities

### 🗄️ Database Integration & AI Agents
- **Natural Language to SQL**: AI agents translate user queries into structured SQL statements
- **Real-time Data Retrieval**: Autonomous intermediaries fetch data directly from company databases
- **API Call Generation**: Convert natural language requests into precise API calls
- **Multi-Database Support**: Compatible with various database systems (PostgreSQL, MySQL, etc.)
- **Query Optimization**: Intelligent query generation for optimal performance
- **Data Security**: Secure database access with proper authentication and authorization

### 👥 Human-in-the-Loop System
- **Interactive Validation**: Human approval required for critical decisions and actions
- **Review Workflows**: Step-by-step review process for AI-generated insights and recommendations
- **Feedback Integration**: Continuous learning from human corrections and approvals
- **Escalation Protocols**: Automatic escalation to human experts for ambiguous or high-stakes decisions
- **Collaborative Decision Making**: Combine AI insights with human expertise for optimal outcomes
- **Audit Trail**: Complete traceability of AI decisions and human interventions

### 🛡️ AI Guardrails & Safety
- **Input Validation**: Comprehensive validation of user inputs and AI-generated queries
- **Output Filtering**: Automated filtering of inappropriate, harmful, or biased content
- **Rate Limiting**: Prevent abuse and ensure fair usage of AI resources
- **Permission-Based Access**: Role-based access control for different AI capabilities
- **Compliance Checks**: Automated compliance with industry regulations and standards
- **Anomaly Detection**: Real-time monitoring for unusual AI behavior or outputs
- **Safety Protocols**: Emergency stop mechanisms for unexpected AI behavior

### 📈 Interactive Dashboard
- **Real-time Data**: Live dashboard with up-to-date metrics and insights
- **Responsive Design**: Modern, mobile-friendly interface built with Next.js 14
- **Interactive Charts**: Powered by Recharts for dynamic data visualization
- **Error Handling**: Robust error handling with fallback data and retry mechanisms
- **Dark Mode**: Professional dark-themed UI optimized for data analysis

---

## 🏗️ Architecture Overview

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

---

## 🧠 AI Agents System

| Agent | Role | Capabilities |
|-------|------|-------------|
| `MarketResearchAgent` | Market Analysis | TAM/SAM analysis, trend research via Tavily API |
| `CompetitorAgent` | Competitive Intelligence | Competitor landscape, positioning analysis |
| `FinancialAnalysisAgent` | Financial Processing | Metric extraction from PDFs, report analysis |
| `ForecastingAgent` | Predictive Analytics | ML-based financial forecasting interpretation |
| `DecisionAgent` | Synthesis & Scoring | Comprehensive analysis synthesis and final scoring |
| `DatabaseAgent` | Data Integration | Natural language to SQL conversion, real-time database queries |
| `HumanOversightAgent` | Human-in-the-Loop | Review workflows, approval processes, feedback integration |
| `GuardrailAgent` | Safety & Compliance | Input validation, output filtering, anomaly detection |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)
- Groq API Key
- Tavily API Key (optional, for enhanced web search)

### 1. Clone & Configure
```bash
git clone <repository-url>
cd Startup-to-Business
cp .env.example .env
# Fill in your GROQ_API_KEY and TAVILY_API_KEY in .env
```

### 2. Run with Docker (Recommended)
```bash
docker-compose up --build
```

### 3. Run Locally

**Backend:**
```bash
cd src/backend
python -m venv venv && source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd src/frontend
npm install
npm run dev
```

### 4. Access the Application
- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

---

## 📂 Project Structure

```
Startup-to-Business/
├── src/
│   ├── backend/              # FastAPI + LangGraph backend
│   │   ├── app/
│   │   │   ├── agents/       # AI agents implementation
│   │   │   ├── api/          # API routes and endpoints
│   │   │   ├── workflows/    # LangGraph workflows
│   │   │   ├── services/     # Business logic services
│   │   │   ├── ml/           # Machine learning models
│   │   │   ├── database/     # Database integration and agents
│   │   │   ├── guardrails/   # Safety and compliance systems
│   │   │   ├── human/        # Human-in-the-loop workflows
│   │   │   └── tools/        # Utility tools
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── frontend/             # Next.js 14 App Router frontend
│   │   ├── app/              # App Router pages
│   │   ├── components/       # Reusable React components
│   │   ├── services/         # API service layer
│   │   └── types/            # TypeScript type definitions
│   └── docker-compose.yml
├── .env.example              # Environment variables template
├── langgraph.json            # LangGraph configuration
├── render.yaml               # Render deployment configuration
└── README.md                 # This file
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM operations | ✅ |
| `TAVILY_API_KEY` | Tavily search API key for market research | ⚠️ |
| `DATABASE_URL` | Database connection string | ⚠️ |
| `NEXT_PUBLIC_API_URL` | Backend URL for frontend | ✅ |
| `ENVIRONMENT` | Deployment environment (development/production) | ✅ |
| `ALLOWED_ORIGINS` | CORS allowed origins | ✅ |

### API Endpoints

#### Startup Validation
- `POST /api/v1/startup/validate` - Validate a startup idea
- `GET /api/v1/startup/ideas` - Get validated ideas history

#### Financial Reports
- `POST /api/v1/financial/upload` - Upload and analyze financial reports
- `GET /api/v1/financial/metrics` - Get extracted financial metrics

#### Forecasting
- `POST /api/v1/forecasting/generate` - Generate financial forecasts
- `GET /api/v1/forecasting/history` - Get forecasting history

#### Market Intelligence
- `POST /api/v1/market/analyze` - Analyze market opportunities
- `GET /api/v1/market/competitors` - Get competitor analysis

#### Database Integration
- `POST /api/v1/database/query` - Execute natural language database queries
- `GET /api/v1/database/schemas` - Get database schema information
- `POST /api/v1/database/api-call` - Generate and execute API calls from natural language

#### Human-in-the-Loop
- `POST /api/v1/human/review` - Submit AI outputs for human review
- `GET /api/v1/human/pending-approvals` - Get pending items requiring human approval
- `POST /api/v1/human/approve` - Approve or reject AI-generated decisions
- `GET /api/v1/human/audit-trail` - Get complete audit trail of decisions

#### Guardrails & Safety
- `POST /api/v1/guardrails/validate` - Validate inputs and outputs against safety rules
- `GET /api/v1/guardrails/policies` - Get current safety and compliance policies
- `POST /api/v1/guardrails/report` - Report safety concerns or anomalies

#### Dashboard
- `GET /api/v1/dashboard/dashboard` - Get comprehensive dashboard data
- `GET /api/v1/dashboard/score` - Get startup validation score
- `GET /api/v1/dashboard/market-analysis` - Get market analysis summary

---

## 🐳 Docker Deployment

### Development Environment
```bash
# Build and start all services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment
The platform supports deployment to Render with the included `render.yaml` configuration:

1. Connect your GitHub repository to Render
2. Create a new Blueprint deployment
3. Set environment variables in Render dashboard
4. Deploy automatically

---

## 🧪 Testing

### Backend Tests
```bash
cd src/backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd src/frontend
npm run test
npm run lint
npm run type-check
```

### Integration Tests
Multiple comprehensive test files are included:
- `test_dashboard_api.py` - Dashboard API integration tests
- `test_startup_validation.py` - Startup validation workflow tests
- `test_financial_analysis.py` - Financial analysis tests
- `test_forecasting.py` - Forecasting engine tests

---

## 🔍 Monitoring & Logging

### Structured Logging
- Comprehensive logging system with structured JSON output
- Different log levels for development and production
- Request tracking and performance monitoring

### Error Handling
- Global exception handlers for consistent error responses
- Graceful degradation with fallback data
- User-friendly error messages with retry options

---

## 🚀 Performance Features

### Caching Strategy
- API response caching for improved performance
- Database query optimization
- Frontend data caching with React Query patterns

### Scalability
- Containerized deployment with Docker
- Horizontal scaling support
- Load balancer ready with Nginx configuration

---

## 🔒 Security Features

- CORS configuration for cross-origin requests
- Environment variable management for sensitive data
- Input validation and sanitization
- Secure API key handling

---

## 📚 Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **LangChain** - Framework for building LLM applications
- **LangGraph** - Build stateful, multi-actor applications with LLMs
- **PyMuPDF** - PDF processing and analysis
- **scikit-learn** - Machine learning library for forecasting
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Composable charting library
- **Lucide React** - Beautiful icon library
- **Axios** - Promise-based HTTP client

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **PostgreSQL** - Primary database (optional)
- **Nginx** - Reverse proxy and load balancer
- **Render** - Cloud deployment platform

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

For support and questions:
- Check the [API Documentation](http://localhost:8000/docs)
- Review the test files for usage examples
- Open an issue on GitHub for bug reports or feature requests

---

## 🔮 Roadmap

### Upcoming Features
- [ ] Real-time WebSocket connections for live updates
- [ ] Advanced ML models for improved forecasting accuracy
- [ ] Multi-language support
- [ ] Advanced user authentication and authorization
- [ ] Integration with additional data sources
- [ ] Mobile application
- [ ] Advanced analytics and reporting features

### Current Development
- Enhanced error handling and recovery mechanisms
- Performance optimization for large datasets
- Improved UI/UX with additional interactive features
- Extended API documentation and examples
