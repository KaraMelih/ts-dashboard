FROM python:3.12-slim AS builder
WORKDIR /app

# Copy only dependency files
COPY pyproject.toml poetry.lock* README.md ./
# Copy application code
COPY src/ ./src

# Install build deps & Poetry via pip
RUN apt-get update \
 && apt-get install -y build-essential curl \
 && python3 -m pip install --upgrade pip \
 && pip install poetry \
 && rm -rf /var/lib/apt/lists/*

# Confirm Poetry is available
RUN poetry --version

# Install your main dependencies
RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-interaction --no-ansi 
 #--no-root


### In this stage, we just cherry pick the necessary files from the builder stage to keep the final image small.
# This avoids copying unnecessary files like tests, docs, etc.
# Runner stage
FROM python:3.12-slim
WORKDIR /app

# Copy deps from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=builder /usr/local/bin/pip     /usr/local/bin/pip

# Copy app code
COPY src/ ./src

EXPOSE 8000

CMD ["sh", "-c", "python src/ts_dashboard/scripts/fetch_btc_data.py && uvicorn ts_dashboard.main:app --host 0.0.0.0 --port 8000"]
