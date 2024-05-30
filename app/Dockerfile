# Use an official Python image as the base image
FROM python:3.12.3-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory within the container
WORKDIR /app

# Copy necessary files
COPY requirements.txt .

# Install dependencies and clean up
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Copy the rest of the source code into the container
COPY src /app/src
COPY tests /app/tests
COPY .env /app

# Install wait-for-it.sh script
RUN apt-get update && apt-get install -y curl && \
    curl -LJO https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh

# Define environment variables
ENV APP_PORT=${APP_PORT}
ENV APP_HOST=${APP_HOST}
ENV APP_MODULE=${APP_MODULE}
ENV PYTHONPATH="/app/src"
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}

# Expose the port the FastAPI app will run on
EXPOSE ${APP_PORT}

# Use a single CMD instruction
CMD ["sh", "-c", "./wait-for-it.sh ${DB_HOST}:${DB_PORT} --timeout=0 --strict -- uvicorn ${APP_MODULE} --host ${APP_HOST} --port ${APP_PORT}"]
