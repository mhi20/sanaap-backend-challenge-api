#!/bin/sh
set -e

echo 'checking and creating database if it does not exist...'
/app/deployments/development/init-db.sh

sleep 1
echo 'running migrations...'
uv run python ./manage.py migrate

echo 'running collecting static...'
python manage.py collectstatic --noinput

echo 'starting server...'
exec gunicorn core.asgi:application \
    --bind 0.0.0.0:8000 \
    -k uvicorn.workers.UvicornWorker