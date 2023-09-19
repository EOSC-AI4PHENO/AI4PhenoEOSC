#!/bin/bash

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq//
CELERY_BACKEND_URL=redis://redis:6379/0
CELERY_QUEUE=my_queue

CONTAINER_ID=$(docker ps | grep ':5555' | awk '{print $1}')

if [ -z "$CONTAINER_ID" ]; then
    echo "Nie znaleziono kontenera z portem 5555."
    exit 1
fi

CELERY_STATUS=$(docker exec $CONTAINER_ID celery -A worker.celery status 2>&1)

echo "Oryginalny status Celery:"
echo "$CELERY_STATUS"
echo "-------------------------"

if [[ $CELERY_STATUS == *"online"* ]]; then
    echo 1
else
    #docker exec $CONTAINER_ID celery -A worker.celery purge
    docker exec $CONTAINER_ID celery --broker ${CELERY_BROKER_URL} --result-backend ${CELERY_BACKEND_URL} -A worker.celery worker --loglevel=INFO --concurrency 36
fi
