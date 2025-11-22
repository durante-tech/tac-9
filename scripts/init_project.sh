#!/bin/bash
# Initialize TAC-9 project

set -e

echo "🚀 Initializing TAC-9 Project..."

# Install dependencies
echo "📦 Installing dependencies..."
uv sync --all-extras

# Create .env from sample if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.sample .env
    echo "⚠️  Please edit .env and add your API keys"
fi

# Create workspace directory
echo "📁 Creating workspace directory..."
mkdir -p workspace
mkdir -p logs/conversations

# Run tests to verify installation
echo "🧪 Running tests..."
uv run pytest tests/ -v

echo "✅ TAC-9 initialization complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys (ANTHROPIC_API_KEY or OPENAI_API_KEY)"
echo "2. Set TARGET_PROJECT_PATH to your Next.js + Supabase project"
echo "3. Run: uv run tac9 interactive"
