#!/bin/bash

# Define variables for the client
CLIENT_IMAGE_NAME="client"
CLIENT_CONTAINER_NAME="CS5939_A3_Client"

# Define variables for the edge-client
EDGE_CLIENT_IMAGE_NAME="edgeclient"
EDGE_CLIENT_CONTAINER_NAME="CS5939_A3_Edge_Client"

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

# Build the Docker image for the edge-client
docker build -t $EDGE_CLIENT_IMAGE_NAME .

# Remove any existing container with the same name for the edge-client
if [ "$(docker ps -aq -f name=$EDGE_CLIENT_CONTAINER_NAME)" ]; then
    docker rm -f $EDGE_CLIENT_CONTAINER_NAME
fi

# Run the Docker container for the edge-client
docker run --name $EDGE_CLIENT_CONTAINER_NAME -d -p 3000:3000 $EDGE_CLIENT_IMAGE_NAME