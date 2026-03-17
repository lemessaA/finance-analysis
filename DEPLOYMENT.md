# AI Business Intelligence Platform - Deployment to Render

This guide will help you deploy the AI Business Intelligence Platform to Render.

## Prerequisites

1. A [Render](https://render.com) account
2. API keys for:
   - [Groq API](https://console.groq.com/)
   - [Tavily API](https://app.tavily.com/) (optional, for web search)

## Deployment Steps

### 1. Prepare Your Repository

Ensure all deployment files are committed to your repository:
- `render.yaml` - Multi-service deployment configuration
- `src/backend/Dockerfile` - Backend container configuration
- `src/backend/requirements.txt` - Python dependencies
- `src/frontend/package.json` - Frontend dependencies
- `.env.example` - Environment variables template

### 2. Deploy to Render

1. **Connect your GitHub repository** to Render
2. **Create a new Blueprint** (multi-service) deployment
3. **Use the `render.yaml` configuration**
4. **Set environment variables** in Render dashboard:
   - `GROQ_API_KEY`: Your Groq API key
   - `TAVILY_API_KEY`: Your Tavily API key (optional)

### 3. Environment Variables

Set these in your Render service environment variables:

**Backend Service:**
- `GROQ_API_KEY` - Required
- `TAVILY_API_KEY` - Optional
- `ENVIRONMENT=production`

**Frontend Service:**
- `NEXT_PUBLIC_API_URL` - Will be auto-set by Render
- `NODE_ENV=production`

### 4. Post-Deployment Configuration

After deployment:

1. **Update CORS origins** in your backend if needed
2. **Test the application** using the provided URLs
3. **Monitor logs** in the Render dashboard

## Services Overview

### Backend (FastAPI + LangGraph)
- **URL**: `https://your-backend-app.onrender.com`
- **Health Check**: `https://your-backend-app.onrender.com/api/v1/health/`
- **API Docs**: `https://your-backend-app.onrender.com/docs`

### Frontend (Next.js)
- **URL**: `https://your-frontend-app.onrender.com`
- **Features**: Financial Report Analyzer, Startup Validation, Forecasting

## Troubleshooting

### Common Issues

1. **Build Failures**: Check that all dependencies are listed in `requirements.txt`
2. **Environment Variables**: Ensure API keys are set correctly
3. **CORS Issues**: Update `ALLOWED_ORIGINS` in backend configuration
4. **Port Issues**: Render assigns random ports, use `$PORT` environment variable

### Logs and Debugging

- Check Render service logs for detailed error messages
- Use the health endpoint to verify backend status
- Test API endpoints directly using the `/docs` interface

## Local Development

To run locally:

```bash
# Backend
cd src/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd src/frontend
npm install
npm run dev
```

## Support

For issues with deployment, check:
1. Render documentation: https://docs.render.com/
2. FastAPI deployment guide: https://fastapi.tiangolo.com/deployment/
3. Next.js deployment guide: https://nextjs.org/docs/deployment