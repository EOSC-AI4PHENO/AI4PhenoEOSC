from celery import Celery
import os

worker = Celery("myapp", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"), include=["worker.tasks", "logic"], task_serializer='pickle',  result_serializer='pickle', accept_content=['pickle'])

#worker = Celery("myapp", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"), include=["worker.tasks", "logic"])

worker.conf.task_serializer = 'pickle'
worker.conf.result_serializer = 'pickle'
worker.conf.event_serializer = 'pickle'
worker.conf.accept_content = ['pickle']
worker.conf.task_accept_content = ['pickle']
worker.conf.result_accept_content = ['pickle']
worker.conf.event_accept_content = ['pickle']

# Optional configuration, see the application user guide.
worker.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    worker.start()