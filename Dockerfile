# FROM python:3.12-slim

# # Set working directory on the container
# # This is where the application code will be copied and run
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#     build-essential curl \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir poetry

# COPY pyproject.toml poetry.lock* ./
# RUN poetry config virtualenvs.create false \
#     && poetry install --no-interaction --no-ansi --only main --no-root
# ## poetry install --no-dev (this flag does not exists)

# # Copy the application code into the container (everything in the current directory)
# COPY . .

# # Expose the port that the FastAPI app will run on
# # This is the port that will be used to access the application from outside the container
# EXPOSE 8000

# # default command to run the FastAPI application using uvicorn
# CMD ["sh", "-c", \
#      "python scripts/fetch_btc_data.py && uvicorn ts_dashboard.main:app --host  0.0.0.0 --port 8000"]




FROM python:3.12-slim AS builder
WORKDIR /app

# Install build deps & Poetry via pip
RUN apt-get update \
 && apt-get install -y build-essential curl \
 && python3 -m pip install --upgrade pip \
 && pip install poetry \
 && rm -rf /var/lib/apt/lists/*

# Confirm Poetry is available
RUN poetry --version

# Copy only dependency files
COPY pyproject.toml poetry.lock* ./

# Install your main dependencies
RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-interaction --no-ansi --no-root

# Copy application code
COPY src/ ./src
COPY scripts/ ./scripts

# Runner stage
FROM python:3.12-slim
WORKDIR /app

# Copy deps from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# Copy app code
COPY src/ ./src
COPY scripts/ ./scripts

EXPOSE 8000

CMD ["sh", "-c", "python scripts/fetch_btc_data.py && uvicorn ts_dashboard.main:app --host 0.0.0.0 --port 8000"]
