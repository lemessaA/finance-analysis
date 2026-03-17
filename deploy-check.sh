#!/bin/bash
# Deployment Checklist for Render

echo "🚀 AI Business Intelligence Platform - Render Deployment Checklist"
echo "=================================================================="

# Check if required files exist
echo "📋 Checking deployment files..."

files=("render.yaml" "src/backend/Dockerfile" "src/backend/requirements.txt" "src/frontend/package.json" ".env.example")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file - Found"
    else
        echo "❌ $file - Missing"
    fi
done

echo ""
echo "🔑 Environment Variables Required:"
echo "   • GROQ_API_KEY (Backend)"
echo "   • TAVILY_API_KEY (Backend - optional)"
echo ""

echo "🌐 Services to be deployed:"
echo "   • Backend API (FastAPI + LangGraph)"
echo "   • Frontend (Next.js)"
echo ""

echo "📝 Next Steps:"
echo "1. Push all changes to GitHub"
echo "2. Connect repository to Render"
echo "3. Create Blueprint deployment using render.yaml"
echo "4. Set environment variables in Render dashboard"
echo "5. Deploy and test both services"
echo ""

echo "🔗 Useful Links:"
echo "   • Render Dashboard: https://dashboard.render.com/"
echo "   • API Documentation: /docs (after deployment)"
echo "   • Health Check: /api/v1/health/ (after deployment)"
echo ""

echo "✨ Ready for deployment!"