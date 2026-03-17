#!/bin/bash
# Build script for Render deployment

echo "🚀 Starting AI Business Intelligence Platform deployment..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd src/backend
pip install -r requirements.txt

# Build frontend
echo "🔨 Building frontend..."
cd ../frontend
npm install
npm run build

echo "✅ Build completed successfully!"