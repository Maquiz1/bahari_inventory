#!/usr/bin/env bash
# ==============================================================================
# Production Deployment Script for Bahari Inventory Application
# Path on Server: /opt/bahari_inventory/deploy.sh (you may copy to desired location)
# ==============================================================================
set -e

# -------------------------------------------------------------------------
# 1️⃣  Define paths
# -------------------------------------------------------------------------
PROJECT_DIR="/opt/bahari_inventory"
BACKEND_DIR="${PROJECT_DIR}"
ENV_FILE="${BACKEND_DIR}/.env.docker"

echo "=========================================="
echo "🚀 Starting Bahari Inventory Production Deployment"
echo "=========================================="

# -------------------------------------------------------------------------
# 2️⃣  Go to the project directory
# -------------------------------------------------------------------------
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR"
else
    echo "❌ Error: Project directory $PROJECT_DIR does not exist."
    exit 1
fi

# -------------------------------------------------------------------------
# 3️⃣  Pull latest code (if this is a git repo)
# -------------------------------------------------------------------------
if [ -d ".git" ]; then
    echo "📥 Pulling latest changes from git..."
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    git pull origin "$CURRENT_BRANCH" || true
fi

# -------------------------------------------------------------------------
# 4️⃣  Ensure runtime directories exist (static & media)
# -------------------------------------------------------------------------
echo "📁 Ensuring static and media directories exist..."
mkdir -p "${BACKEND_DIR}/staticfiles"
mkdir -p "${BACKEND_DIR}/media"

# -------------------------------------------------------------------------
# 5️⃣  Create a production .env.docker if it does not exist
# -------------------------------------------------------------------------
if [ ! -f "$ENV_FILE" ]; then
    echo "🛠️  Creating ${ENV_FILE} with inventory defaults..."
    cat <<'EOF' > "$ENV_FILE"
DEBUG=0
SECRET_KEY=change_this_to_a_random_secret_key_in_production

# PostgreSQL Database (docker‑compose)
DB_NAME=inventory_db
DB_USER=inventory_user
DB_PASSWORD=inventory_secure_pass
DB_HOST=db
DB_PORT=5432

DATABASE_URL=postgres://inventory_user:inventory_secure_pass@db:5432/inventory_db

LOAD_SEED_DATA=true
ALLOWED_HOSTS=inventory.tamris.org,www.inventory.tamris.org,localhost,127.0.0.1
EOF
fi

# -------------------------------------------------------------------------
# 6️⃣  Build and launch Docker‑Compose services
# -------------------------------------------------------------------------
echo "🐳 Building and starting Docker containers..."
docker compose up -d --build

# -------------------------------------------------------------------------
# 7️⃣  Wait a moment for the DB to be reachable (entrypoint will handle waiting)
# -------------------------------------------------------------------------
echo "⏳ Waiting a few seconds for the DB to become reachable..."
sleep 10

# -------------------------------------------------------------------------
# 8️⃣  Run migrations & collect static files inside the web container
# -------------------------------------------------------------------------
echo "🔧 Applying migrations..."
docker compose exec web python manage.py migrate --noinput

echo "🗂️  Collecting static files..."
docker compose exec web python manage.py collectstatic --noinput

# -------------------------------------------------------------------------
# 9️⃣  (Optional) Load seed data if the flag is set
# -------------------------------------------------------------------------
if grep -q '^LOAD_SEED_DATA=true' "$ENV_FILE"; then
    echo "🌱 Loading seed data..."
    docker compose exec web python manage.py loaddata /app/db_seed.json || true
fi

# -------------------------------------------------------------------------
# 📊  Show container status
# -------------------------------------------------------------------------
echo "🔍 Checking running services..."
docker compose ps

echo "=========================================="
echo "✅  Deployment completed successfully!"
echo "=========================================="
