#!/bin/bash

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Check if running in development or production mode
if [ "$1" == "prod" ]; then
    echo "Starting MRI Insight in production mode..."
    gunicorn --bind 0.0.0.0:8080 app:app
else
    echo "Starting MRI Insight in development mode..."
    export FLASK_APP=app.py
    export FLASK_ENV=development
    python app.py
fi