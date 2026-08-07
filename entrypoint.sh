#!/bin/sh
set -e

echo "Waiting for database..."
python -c "
import time, socket, os
host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', 5432))
for _ in range(30):
    try:
        with socket.create_connection((host, port), timeout=2):
            print('Database is ready!')
            break
    except OSError:
        time.sleep(1)
"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
