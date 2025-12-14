#!/bin/bash
set -e

echo "Switching traffic to GREEN (v1.1.0)..."

# Проверяем health green через docker
if docker exec ml-service-green curl -sf http://localhost:8080/health > /dev/null 2>&1; then
    echo "Green service is healthy"
    cp nginx/upstream-green.conf nginx/upstream.conf
    docker exec nginx-lb nginx -s reload
    echo "Traffic switched to GREEN"
    curl -s http://localhost/health | jq .
else
    echo "ERROR: Green service is not healthy! Rolling back..."
    ./switch-to-blue.sh
    exit 1
fi
