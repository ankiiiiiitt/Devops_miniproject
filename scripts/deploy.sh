#!/bin/bash

# Configuration
IMAGE_NAME="focusvault-app"
CONTAINER_NAME="focusvault-web"
DOCKER_HUB_USER="your_dockerhub_username"

echo "🚀 Starting Deployment Process..."

# 1. Pull the latest image
echo "📥 Pulling latest image from Docker Hub..."
docker pull ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest

# 2. Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🛑 Stopping and removing existing container: ${CONTAINER_NAME}..."
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
fi

# 3. Run the new container
echo "🏗️ Starting new container..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -p 5001:5000 \
    --restart always \
    -e MONGO_URI="mongodb://mongodb:27017/ai_sem_project" \
    ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest

# 4. Cleanup old images
echo "🧹 Cleaning up dangling Docker images..."
docker image prune -f

echo "✅ Deployment successful! App is running on port 5001."
