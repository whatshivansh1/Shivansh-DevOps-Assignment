#!/bin/bash
set -eu

CONTAINER_NAME="jenkins"

if ! docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
    echo "FAIL: Jenkins container does not exist."
    exit 1
fi

STATUS=$(docker inspect -f '{{.State.Status}}' "$CONTAINER_NAME")
echo "Container status: $STATUS"

if [ "$STATUS" != "running" ]; then
    echo "FAIL: Jenkins container is not running."
    exit 1
fi

echo
echo "Published ports:"
docker port "$CONTAINER_NAME"

echo
echo "Checking Jenkins HTTP endpoint..."
HTTP_CODE=$(curl -sS -o /dev/null -w '%{http_code}' \
    --max-time 10 http://localhost:8080/login) || {
    echo "FAIL: Jenkins HTTP endpoint is unreachable."
    exit 1
}

echo "HTTP status: $HTTP_CODE"

if [ "$HTTP_CODE" != "200" ]; then
    echo "FAIL: Expected HTTP 200."
    exit 1
fi

echo
echo "Recent startup logs:"
docker logs --tail 15 "$CONTAINER_NAME" 2>&1

echo
echo "PASS: Jenkins container is running and the login endpoint responds."
