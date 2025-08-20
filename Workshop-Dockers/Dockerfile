# -----------------------------------------------------------------------------
# Dockerfile for building a Debian Slim-based container with Python and Git.
# 
# This Dockerfile creates a lightweight container based on Debian Slim.
# It installs Python 3.11 and Git using the Debian package manager (apt-get).
# The working directory is set to /app, and the default command starts a bash shell.
#
# Usage:
#   docker build -t <image-name> .
#   docker run <image-name>
#
# Default command:
#   /bin/bash
# -----------------------------------------------------------------------------

# Build arguments that can be overridden
ARG BASE_IMAGE=ubuntu:22.04
# Re-declare ARG variables after FROM (they need to be redeclared to be available after FROM)
ARG NODE_VERSION=20
ARG APP_DIR="/usr/src/app"
ARG REPO_URL="https://github.com/nirgeier/copilot-python-workshop.git"
ARG REPO_BRANCH=Docker
ARG CONTAINER_NAME=copilot-python-workshop
ARG VERSION=1.0
ARG DESCRIPTION="Dockerfile for Python Workshop"
ARG AUTHOR="Nir Geier nirgeier@gmail.com"
ARG MAINTAINER="Nir Geier nirgeier@gmail.com"
ARG BACKEND_PORT=3000
ARG FRONTEND_PORT=4200
ARG SRC_DIR=/app/src
ARG WORKSHOP_DIR=/app/copilot-python-workshop/frontend
ARG REPO_DEST=/copilot-python-workshop

FROM ${BASE_IMAGE}

ENV NODE_VERSION=${NODE_VERSION:-20}
ENV APP_DIR=${APP_DIR:-/usr/src/app}
ENV REPO_URL=${REPO_URL:-https://github.com/nirgeier/copilot-python-workshop.git}
ENV REPO_BRANCH=${REPO_BRANCH:-Docker}
ENV CONTAINER_NAME=${CONTAINER_NAME:-copilot-python-workshop}
ENV VERSION=${VERSION:-1.0}
ENV DESCRIPTION=${DESCRIPTION:-"Dockerfile for Python Workshop"}
ENV AUTHOR=${AUTHOR:-"Nir Geier nirgeier@gmail.com"}
ENV MAINTAINER=${MAINTAINER:-"Nir Geier nirgeier@gmail.com"}
ENV BACKEND_PORT=${BACKEND_PORT:-3000}
ENV FRONTEND_PORT=${FRONTEND_PORT:-4200}
ENV SRC_DIR=${SRC_DIR:-/app/src}
ENV WORKSHOP_DIR=${WORKSHOP_DIR:-/app/copilot-python-workshop/frontend}
ENV REPO_DEST=${REPO_DEST:-/copilot-python-workshop}

LABEL name="${CONTAINER_NAME}"
LABEL author="${AUTHOR}"
LABEL version="${VERSION}"
LABEL description="${DESCRIPTION}"
LABEL maintainer="${MAINTAINER}"

RUN printenv

# Install Node.js (LTS), Python 3.11, git, and other dependencies
RUN apt-get update && \
  apt-get install -y curl gnupg2 ca-certificates lsb-release && \
  curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - && \
  apt-get install -y  \
  bash-completion     \
  git                 \
  nodejs              \
  python3             \
  python3-pip         \
  python3-venv        \
  rsync               \
  && rm -rf /var/lib/apt/lists/*

# Enable bash completion
RUN . /etc/profile.d/bash_completion.sh

# Set the working directory to the cloned repository
WORKDIR /app/src
WORKDIR ${APP_DIR}

# Clone only the workshop folder using a sparse-checkout into ${REPO_DEST}
RUN mkdir -p /tmp/repo && \
  git clone --filter=blob:none --no-checkout --depth 1 --branch ${REPO_BRANCH} ${REPO_URL} /tmp/repo && \
  cd /tmp/repo && \
  git sparse-checkout init --cone && \
  git sparse-checkout set copilot-python-workshop && \
  git checkout ${REPO_BRANCH} && \
  mkdir -p ${REPO_DEST} && \
  rsync -a /tmp/repo/copilot-python-workshop/ ${REPO_DEST}/ && \
  rm -rf /tmp/repo

# Verify the clone was successful
RUN if [ ! -d "${REPO_DEST}" ]; then \
  echo "Failed to sparse-checkout repository to ${REPO_DEST}"; \
  exit 1; \
  fi

# Set up the backend Python environment
WORKDIR ${REPO_DEST}/backend
RUN pip3 install --upgrade pip &&  \
  pip3 install -r requirements.txt

RUN pip3 freeze > ${REPO_DEST}/requirements.txt

# Set up the frontend Node.js environment
WORKDIR ${REPO_DEST}/frontend
RUN npm install

# Set the working directory back to the root of the cloned repository
ENV WORKSHOP_DIR=${REPO_DEST}/frontend
WORKDIR ${WORKSHOP_DIR}

# =============================================================================
# ENTRYPOINT SCRIPT CREATION
# =============================================================================
# Create a startup script that handles SSH key setup and service initialization
# Using heredoc syntax for inline script creation (Docker BuildKit feature)
COPY <<EOF /entrypoint.sh
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
EOF

# Expose ports
EXPOSE ${BACKEND_PORT} ${FRONTEND_PORT}

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

# Default command
#CMD ["/bin/bash"]
