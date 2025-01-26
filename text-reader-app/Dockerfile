# Build step: Build the React front end
FROM node:16-alpine AS build-step 
WORKDIR /code/frontend
COPY ./frontend/package.json ./package.json
COPY ./frontend/package-lock.json ./package-lock.json

RUN npm install
COPY ./frontend /code/frontend
RUN npm run build

# Use a Python base image
FROM python:3.12-slim

# Install Node.js and npm in the Python stage
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y \
    nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code/backend

# Copy backend requirements and install dependencies
COPY ./backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy backend code
COPY ./backend /code/backend

# Copy frontend and its dependencies
COPY --from=build-step /code/frontend /code/frontend
# Install frontend dependencies in the Python stage
WORKDIR /code/frontend
RUN npm install
WORKDIR /code/backend

# Copy entrypoint script
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

EXPOSE 8000 3000

ENTRYPOINT ["./entrypoint.sh"]
