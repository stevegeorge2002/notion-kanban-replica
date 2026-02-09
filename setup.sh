#!/bin/bash

# Setup script for Notion Kanban Replica

echo "🚀 Setting up Notion Kanban Replica..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '(?<=Python )\d+\.\d+')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python -m app.database

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start the backend: uvicorn app.api:app --reload --port 8000"
echo "2. Start the frontend: reflex run"
echo ""
echo "Or use Docker: docker build -t notion-kanban . && docker run -p 3000:3000 notion-kanban"
