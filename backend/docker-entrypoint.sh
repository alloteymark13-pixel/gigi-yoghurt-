#!/bin/sh
set -e

echo "Waiting for Postgres to be ready..."
# Render provides RENDER_DB_* variables; build DATABASE_URL if not set
: "${DATABASE_URL:=postgresql://${RENDER_DB_USER:-user}:${RENDER_DB_PASSWORD:-pass}@${RENDER_DB_HOST:-db}:${RENDER_DB_PORT:-5432}/${RENDER_DB_NAME:-gigi_yogurt}}"
export DATABASE_URL

# extract host and user for pg_isready; fallback to db host
DB_HOST=$(echo "$DATABASE_URL" | sed -E 's#.*@([^:/]+).*#\1#' || echo "db")
DB_USER=$(echo "$DATABASE_URL" | sed -E 's#.*://([^:]+):.*#\1#' || echo "gigi")

until pg_isready -h "$DB_HOST" -p 5432 -U "$DB_USER"; do
  sleep 1
done
echo "Postgres ready."

if [ -f /app/../sql/schema.sql ]; then
  echo "Applying schema..."
  psql "$DATABASE_URL" -f /app/../sql/schema.sql || true
fi

if [ -f /app/../sql/seed.sql ]; then
  echo "Seeding..."
  psql "$DATABASE_URL" -f /app/../sql/seed.sql || true
fi

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
