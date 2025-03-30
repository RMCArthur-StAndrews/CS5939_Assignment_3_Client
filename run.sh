#!/bin/bash

docker stop --all
docker system prune -af

# Define variables for the client
CLIENT_IMAGE_NAME="client"
CLIENT_CONTAINER_NAME="client-api"

# Define variables for the edge-client
EDGE_CLIENT_IMAGE_NAME="edge-client"
EDGE_CLIENT_CONTAINER_NAME="edge-client"

# Build the Docker image for the client
docker build -t $CLIENT_IMAGE_NAME .

# Remove any existing container with the same name for the client
if [ "$(docker ps -aq -f name=$CLIENT_CONTAINER_NAME)" ]; then
    docker rm -f $CLIENT_CONTAINER_NAME
fi

# Run the Docker container for the client
docker run --name $CLIENT_CONTAINER_NAME -d $CLIENT_IMAGE_NAME

# Navigate to the edge-client directory
cd edge-client

# Check if Dockerfile exists in the edge-client directory
if [ ! -f Dockerfile ]; then
    echo "Dockerfile not found in edge-client directory"
    exit 1
fi

# Build the Docker image for the edge-client
docker build -t $EDGE_CLIENT_IMAGE_NAME .

# Remove any existing container with the same name for the edge-client
if [ "$(docker ps -aq -f name=$EDGE_CLIENT_CONTAINER_NAME)" ]; then
    docker rm -f $EDGE_CLIENT_CONTAINER_NAME
fi

# Run the Docker container for the edge-client
docker run --name $EDGE_CLIENT_CONTAINER_NAME -d -p 3000:3000 $EDGE_CLIENT_IMAGE_NAME

# Navigate back to the root directory
cd ..

# Use docker-compose to manage the services
docker-compose down
docker-compose up -d