#!/bin/bash

# Define variables
IMAGE_NAME="client"
CONTAINER_NAME="CS5939_A3_Client"

# Build the Docker image
docker build -t $IMAGE_NAME .

# Remove any existing container with the same name
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    docker rm -f $CONTAINER_NAME
fi

# Run the Docker container
docker run --name $CONTAINER_NAME -d $IMAGE_NAME