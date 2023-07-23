from celery import Celery
import os

worker = Celery("myapp", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"),
                include=["worker.tasks", "logic"], task_serializer='pickle', result_serializer='pickle',
                accept_content=['pickle', 'json'])

# worker = Celery("myapp", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"), include=["worker.tasks", "logic"])

worker.conf.update(task_track_started=True)
worker.conf.update(task_serializer='pickle')
worker.conf.update(result_serializer='pickle')
worker.conf.update(accept_content=['pickle', 'json'])
worker.conf.update(result_persistent=True)
worker.conf.update(worker_send_task_events=False)

# Optional configuration, see the application user guide.
worker.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    worker.start()
