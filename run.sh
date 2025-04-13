#!/bin/bash

docker stop --all
docker system prune -af

CLIENT_IMAGE_NAME="client-api"
CLIENT_CONTAINER_NAME="client-api"

EDGE_CLIENT_IMAGE_NAME="edge-client"
EDGE_CLIENT_CONTAINER_NAME="edge-client"


docker build -t $CLIENT_IMAGE_NAME .

if [ "$(docker ps -aq -f name=$CLIENT_CONTAINER_NAME)" ]; then
    docker rm -f $CLIENT_CONTAINER_NAME
fi

docker run --name $CLIENT_CONTAINER_NAME -d $CLIENT_IMAGE_NAME


cd edge-client

if [ ! -f Dockerfile ]; then
    echo "Dockerfile not found in edge-client directory"
    exit 1
fi

docker build -t $EDGE_CLIENT_IMAGE_NAME .

if [ "$(docker ps -aq -f name=$EDGE_CLIENT_CONTAINER_NAME)" ]; then
    docker rm -f $EDGE_CLIENT_CONTAINER_NAME
fi

docker run --name $EDGE_CLIENT_CONTAINER_NAME -d -p 3000:3000 $EDGE_CLIENT_IMAGE_NAME

cd ..

podman-compose down
podman-compose up -d