FROM python:3.13-slim

RUN pip install uv

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local/.venv

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    gcc \
    gettext \
    curl \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./

RUN uv sync --frozen

ENV PATH="/usr/local/.venv/bin:$PATH"

COPY . .

RUN chmod 755 ./logs

COPY deployments/development/entrypoint.sh /app/deployments/development/entrypoint.sh
RUN chmod +x ./deployments/development/init-db.sh
RUN chmod +x ./deployments/development/entrypoint.sh
CMD ["/app/deployments/development/entrypoint.sh"]
