#!/bin/bash

# Change directoy to root of the application
cd "$(dirname "$0")/../app"

ENV_FILE=".env"

# Check if .env file exists
if [ ! -f $ENV_FILE ]; then
  echo "$ENV_FILE not found!"
  exit 1
fi

DEPENDENCIES=$(grep -oP '(?<=DEPENDENCIES=").*(?=")' $ENV_FILE)

# Check if DEPENDENCIES variable is set
if [ -z "$DEPENDENCIES" ]; then
  echo "No dependencies found in $ENV_FILE"
  exit 1
fi

# Crear o sobrescribir el archivo requirements.txt
echo "$DEPENDENCIES" | tr ' ' '\n' > requirements.txt

echo "requirements.txt has been created with the following dependencies:"
cat requirements.txt