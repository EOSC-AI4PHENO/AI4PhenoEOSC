#!/bin/bash

run_worker() {
  celery --broker ${CELERY_BROKER_URL} --result-backend ${CELERY_BACKEND_URL} -A worker.celery worker --loglevel=INFO -Q image_exposure_queue,sunrise_sunset_queue,apple_segment_queue,apple_detectron2_queue,linden_class_queue,linden_segment_queue
}

run_flower() {
  export FLOWER_UNAUTHENTICATED_API=true
  celery --broker ${CELERY_BROKER_URL} --result-backend ${CELERY_BACKEND_URL} -A worker.celery flower
}

run_fastapi() {
  uvicorn api.main:app --host 0.0.0.0 --port 80
}

while [ $# -gt 0 ] ; do
  case $1 in
    -t | --target) W="$2" ;;
  esac
  shift
done

case $W in
    worker) run_worker ;;
    flower) run_flower ;;
    fastapi) run_fastapi ;;
esac