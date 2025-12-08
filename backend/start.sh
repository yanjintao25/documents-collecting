#!/bin/bash
echo "Starting FastAPI backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

