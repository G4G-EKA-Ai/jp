FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8001

# Run migrations and start server with ASGI
CMD python manage.py migrate --noinput && \
    gunicorn jaytipargal.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8001} --workers 2 --timeout 120
