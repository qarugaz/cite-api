# Base Image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Command to run the Celery worker
CMD ["celery", "-A", "app.celery_app.celery", "worker", "--loglevel=info", "--queues=default"]
CMD ["celery", "-A", "app.celery_app.celery", "worker", "--loglevel=info", "--queues=priority"]
CMD ["celery", "-A", "app.celery_app.celery", "worker", "--loglevel=info", "--queues=slow"]