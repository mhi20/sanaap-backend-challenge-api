#!/bin/bash
set -e

DB_NAME=${DB_NAME:-sanaap_challenge}
DB_USER=${POSTGRES_USER:-postgres}
DB_PASSWORD=${POSTGRES_PASSWORD:-samplePass412}
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

DB_EXIST=$(psql "postgresql://postgres:samplePass412@db:5432/postgres" \
  -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" || true)

if [ "$DB_EXIST" = "1" ]; then
  echo "database '$DB_NAME' already exists"
else
  echo "database '$DB_NAME' does not exist. creating..."

  psql "postgresql://${DB_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:${DB_PORT}/postgres" <<EOSQL
CREATE DATABASE ${DB_NAME};
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
EOSQL
  echo "Database '$DB_NAME' created successfully."
fi