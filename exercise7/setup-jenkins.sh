#!/bin/bash
set -eu

CONTAINER_NAME="jenkins"

if ! docker info >/dev/null 2>&1; then
    echo "Docker is unavailable. Start Docker Desktop and try again."
    exit 1
fi

if docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
    STATUS=$(docker inspect -f '{{.State.Status}}' "$CONTAINER_NAME")

    if [ "$STATUS" = "running" ]; then
        echo "Jenkins is already running. Existing data will be preserved."
    else
        echo "Starting the existing Jenkins container..."
        docker start "$CONTAINER_NAME"
    fi
else
    echo "Creating the Jenkins container..."
    docker run -d \
        --name jenkins \
        --restart unless-stopped \
        -p 8080:8080 \
        -p 50000:50000 \
        -v jenkins_home:/var/jenkins_home \
        jenkins/jenkins:lts
fi

echo
echo "Jenkins URL: http://localhost:8080"
echo "Container status:"
docker ps --filter "name=^/${CONTAINER_NAME}$"
