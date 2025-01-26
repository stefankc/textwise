#!/bin/sh

# Start backend on port 80
APP_SECRET_TOKEN=your_secure_token_here uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

# Start frontend on port 3000
cd ../frontend && PORT=3000 npm start
ls