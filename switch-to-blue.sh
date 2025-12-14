#!/bin/bash
set -e

echo "Switching traffic to BLUE (v1.0.0)..."

# Проверяем health blue через docker
if docker exec ml-service-blue curl -sf http://localhost:8080/health > /dev/null 2>&1; then
    echo "Blue service is healthy"
    cp nginx/upstream-blue.conf nginx/upstream.conf
    docker exec nginx-lb nginx -s reload
    echo "Traffic switched to BLUE"
    curl -s http://localhost/health | jq .
else
    echo "ERROR: Blue service is not healthy!"
    exit 1
fi
