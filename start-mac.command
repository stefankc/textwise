#!/bin/bash

cd "$(dirname "$0")/text-reader-app" || exit 1

echo "Starting Docker containers..."
docker-compose up -d

# Show logs until backend is ready (indicated by "Server is running" message)
echo "Waiting for containers to be ready..."
timeout=60
while [ $timeout -gt 0 ]; do
    if docker-compose logs backend | grep -q "Server is running"; then
        echo "✔ Backend is ready"
        break
    fi
    sleep 1
    ((timeout--))
done

# Open browser once ready
open http://localhost:3000

# Show logs in background
docker-compose logs -f &
