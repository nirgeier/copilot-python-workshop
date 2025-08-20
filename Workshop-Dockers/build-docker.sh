#!/bin/bash

# Load .env file first
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    exit 1
fi

# Load .env and pass all as build args
set -a
source .env
set +a

# Build with all env vars as build args - using array for proper handling
BUILD_ARGS=()
while IFS= read -r line; do
    # Skip comments, empty lines, and lines that don't contain =
    if [[ ! "$line" =~ ^[[:space:]]*# && -n "$line" && "$line" =~ = ]]; then
        BUILD_ARGS+=(--build-arg "$line")
    fi
done < .env

# Build the Docker image
echo "Building with ${#BUILD_ARGS[@]} build arguments..."

# Build the Docker image using compose
docker-compose build "${BUILD_ARGS[@]}"

# Push the Docker image
docker-compose push
