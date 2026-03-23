# 🤖 AI Database Chat Interface

A specialized AI platform that enables companies to **configure their databases** and **interact through an intelligent chat interface** — powered by LangChain, LangGraph, FastAPI, and Next.js.

---

## 🌟 Core Features

### �️ Database Configuration
- **Simple Database Setup**: Easy configuration of company databases through intuitive interface
- **Multiple Database Support**: Compatible with PostgreSQL, MySQL, SQLite, and other major databases
- **Secure Connection**: Encrypted database connections with authentication management
- **Schema Discovery**: Automatic detection and mapping of database schemas
- **Connection Testing**: Real-time validation of database connectivity and credentials
- **Multi-Database Support**: Connect and switch between multiple company databases

### � Intelligent Chat Interface
- **Natural Language Queries**: Ask questions in plain English to retrieve company data
- **Real-time Database Access**: Direct integration with configured databases through conversation
- **Context-Aware Responses**: AI understands context and provides relevant data insights
- **Multi-Turn Conversations**: Maintain context across multiple questions for deeper analysis
- **Interactive Data Visualization**: Charts and graphs generated based on chat queries
- **Query Suggestions**: AI suggests relevant questions based on available data
- **Export Capabilities**: Export chat results and data visualizations to various formats

### 🛡️ AI Guardrails & Safety
- **Input Validation**: Comprehensive validation of user inputs and AI-generated queries
- **Output Filtering**: Automated filtering of inappropriate, harmful, or biased content
- **Rate Limiting**: Prevent abuse and ensure fair usage of AI resources
- **Permission-Based Access**: Role-based access control for different AI capabilities
- **Compliance Checks**: Automated compliance with industry regulations and standards
- **Anomaly Detection**: Real-time monitoring for unusual AI behavior or outputs
- **Safety Protocols**: Emergency stop mechanisms for unexpected AI behavior

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Frontend                     │
│  Database Config │ Chat Interface │ Visualization │ Export  │
└─────────────────────────┬───────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────┐
│                  FastAPI Backend                         │
│                                                         │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ Database        │  │ Chat         │  │ Safety     │  │
│  │ Connector       │  │ Processor    │  │ Guardrails │  │
│  │ (SQLAlchemy)    │  │ (LangChain)  │  │ (Custom)   │  │
│  └─────────────────┘  └──────────────┘  └───────────┘  │
│                                                         │
│  Database │ Query │ Visualization │ Export │ Safety   │
│  Agent    │ Agent │ Agent          │ Agent  │ Agent    │
└─────────────────────────────────────────────────────────┘
```

---

## 🧠 AI Agents System

| Agent | Role | Capabilities |
|-------|------|-------------|
| `DatabaseAgent` | Database Management | Database connection, schema discovery, query optimization |
| `ChatAgent` | Natural Language Processing | Convert natural language to SQL, context understanding |
| `VisualizationAgent` | Data Visualization | Generate charts and graphs from query results |
| `ExportAgent` | Data Export | Export chat results and visualizations to various formats |
| `SafetyAgent` | Guardrails & Compliance | Input validation, output filtering, anomaly detection |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)
- Groq API Key
- Database credentials (PostgreSQL, MySQL, SQLite, etc.)

### 1. Clone & Configure
```bash
git clone <repository-url>
cd Startup-to-Business
cp .env.example .env
# Fill in your GROQ_API_KEY and database credentials in .env
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
- **Frontend Chat Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

---

## 📂 Project Structure

```
Startup-to-Business/
├── src/
│   ├── backend/              # FastAPI + LangChain backend
│   │   ├── app/
│   │   │   ├── agents/       # AI agents implementation
│   │   │   ├── api/          # API routes and endpoints
│   │   │   ├── database/     # Database connection and management
│   │   │   ├── services/     # Business logic services
│   │   │   ├── guardrails/   # Safety and compliance systems
│   │   │   └── tools/        # Utility tools
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── frontend/             # Next.js 14 App Router frontend
│   │   ├── app/              # App Router pages
│   │   │   ├── config/       # Database configuration pages
│   │   │   ├── chat/         # Chat interface pages
│   │   │   └── export/       # Export functionality pages
│   │   ├── components/       # Reusable React components
│   │   │   ├── database/     # Database configuration components
│   │   │   ├── chat/         # Chat-specific components
│   │   │   ├── ui/           # General UI components
│   │   │   └── charts/       # Data visualization components
│   │   ├── services/         # API service layer
│   │   │   ├── database.ts   # Database configuration service
│   │   │   └── chat.ts       # Chat API service
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
| `DATABASE_URL` | Database connection string | ✅ |
| `NEXT_PUBLIC_API_URL` | Backend URL for frontend | ✅ |
| `ENVIRONMENT` | Deployment environment (development/production) | ✅ |
| `ALLOWED_ORIGINS` | CORS allowed origins | ✅ |

### API Endpoints

#### Database Configuration
- `POST /api/v1/database/config` - Configure database connection
- `GET /api/v1/database/test` - Test database connectivity
- `GET /api/v1/database/schema` - Get database schema information
- `PUT /api/v1/database/config` - Update database configuration

#### Chat Interface
- `POST /api/v1/chat/query` - Send natural language queries to chat interface
- `GET /api/v1/chat/history` - Get chat conversation history
- `POST /api/v1/chat/visualize` - Generate data visualizations from chat queries
- `GET /api/v1/chat/suggestions` - Get AI-suggested questions based on available data
- `POST /api/v1/chat/export` - Export chat results and visualizations

#### Guardrails & Safety
- `POST /api/v1/guardrails/validate` - Validate inputs and outputs against safety rules
- `GET /api/v1/guardrails/policies` - Get current safety and compliance policies
- `POST /api/v1/guardrails/report` - Report safety concerns or anomalies

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
