#!/bin/bash

CONTAINER_ID=$(docker ps | grep ':5555' | awk '{print $1}')

CELERY_STATUS=$(docker exec $CONTAINER_ID celery -A worker.celery status 2>&1)

echo "Oryginalny status Celery:"
echo "$CELERY_STATUS"
echo "-------------------------"

if [[ $CELERY_STATUS == *"online"* ]]; then
    echo 1
else
    echo 0
fi
