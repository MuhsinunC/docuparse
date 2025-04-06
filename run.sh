#!/bin/bash
# Simple script to build and run the Docker Compose services

echo "Building and starting Docker containers..."

# Use the bake feature to build the images in parallel (disable if you want to build sequentially)
export COMPOSE_BAKE=true

docker-compose up --build
# docker compose watch

unset COMPOSE_BAKE