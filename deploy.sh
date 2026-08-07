#!/usr/bin/env bash
# ==============================================================================
# Production Deployment Script for Bahari Inventory
# Path: /home/maquiz/projects/bahari_inventory/deploy.sh
# ===========================================================================

set -euo pipefail

# Determine the directory containing this script and change to it
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "🚀 Starting Bahari Inventory Production Deployment"

# 1. Pull latest code from git (if repository)
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "🔄 Pulling latest changes..."
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    git pull origin "$CURRENT_BRANCH" || true
else
    echo "⚠️ Not a git repository. Skipping pull."
fi

# 2. Ensure runtime directories exist
mkdir -p static media

# 3. Ensure .env.docker exists (create from .env if missing)
if [[ ! -f .env.docker ]]; then
    echo "⚙️ Creating .env.docker from .env (fallback)"
    cp .env .env.docker || true
fi

# 4. Build and start Docker Compose services (if docker-compose.yml exists)
if [[ -f docker-compose.yml ]]; then
    echo "🐳 Building and starting Docker containers..."
    docker compose up -d --build
    echo "✅ Docker containers are up."
else
    echo "⚠️ No docker-compose.yml found. Skipping Docker steps."
fi

# 5. Run migrations and collect static files inside the container (if using Docker)
if [[ -f docker-compose.yml ]]; then
    echo "🛠️ Running migrations inside the web container..."
    docker compose exec -T web python manage.py migrate --noinput
    echo "📦 Collecting static files..."
    docker compose exec -T web python manage.py collectstatic --noinput
else
    # Fallback to local commands (useful for non‑Docker setups)
    echo "🛠️ Running migrations locally..."
    python manage.py migrate --noinput
    echo "📦 Collecting static files locally..."
    python manage.py collectstatic --noinput
fi

# 6. Show status of containers (if Docker used)
if [[ -f docker-compose.yml ]]; then
    echo "📊 Docker container status:"
    docker compose ps
fi

echo "✅ Deployment script completed successfully."
