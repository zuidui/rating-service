# Use an official Python image as the base image
FROM python:3.12.3-alpine as base

# Set the working directory within the container
WORKDIR /src

# Install Poetry and update pip in one step
RUN apk add --no-cache bash && \
    pip install --no-cache-dir --upgrade pip poetry && \
    apk del bash

# Copy the dependency files and install dependencies in one step
COPY pyproject.toml /src/
RUN pip install poetry && \
    poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the source code into the container
COPY . /src

# Define environment variables
ENV APP_PORT=${APP_PORT}
ENV APP_HOST=${APP_HOST}
ENV APP_MODULE=${APP_MODULE}

# Expose the port the FastAPI app will run on
EXPOSE ${APP_PORT}

# Use a single CMD instruction
CMD ["poetry run uvicorn $APP_MODULE --reload --host $APP_HOST --port $APP_PORT"]