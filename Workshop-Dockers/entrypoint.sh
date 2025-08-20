#!/bin/bash

# =============================================================================
# Container Startup Script
# =============================================================================
# This script runs when the container starts and handles:

# Copy the src folder to the shared volume, excluding .git directory, only if it does not exist
rsync -a --ignore-existing ${REPO_DEST} /app/src

# Start the backend service
echo "Starting backend service..."
cd /app/src/copilot-python-workshop/backend
python3 app/app.py &

# Start the front end service
echo "Starting front end service..."
cd /app/src/copilot-python-workshop/frontend
npm start &

# Execute the main container command
# This allows the container to run the specified CMD or any override command
echo "Container initialization complete. Keeping container alive..."
tail -f /dev/null
