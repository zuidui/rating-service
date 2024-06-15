# Use an official Python image as the base image
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYDEVD_DISABLE_FILE_VALIDATION 1

# Set the working directory within the container
WORKDIR /workspace/app/src

# Copy necessary files
COPY requirements.txt .

# Install dependencies and clean up
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir debugpy && \
    rm -rf /root/.cache

# Copy the rest of the source code into the container
COPY src /workspace/app/src
COPY tests /workspace/app/tests
COPY .env /workspace/app
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Define environment variables
ENV DEBUG_PORT=${DEBUG_PORT}
ENV APP_PORT=${APP_PORT}
ENV APP_HOST=${APP_HOST}
ENV APP_MODULE=${APP_MODULE}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}

# Expose the port the FastAPI app will run on
EXPOSE ${APP_PORT}
EXPOSE ${DEBUG_PORT}

# Use a single CMD instruction
CMD ["sh", "-c", "wait-for-it.sh ${DB_HOST}:${DB_PORT} --timeout=0 --strict -- python -m debugpy --listen ${APP_HOST}:${DEBUG_PORT} -m uvicorn ${APP_MODULE} --host ${APP_HOST} --port ${APP_PORT} --reload"]
