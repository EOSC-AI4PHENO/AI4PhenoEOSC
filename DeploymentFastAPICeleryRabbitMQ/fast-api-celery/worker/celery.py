from celery import Celery
import os

worker = Celery("myapp", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"),
                include=["worker.tasks", "logic"], task_serializer='json', result_serializer='json',
                accept_content=['json'])

# worker = Celery("myapp", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"),
#                 include=["worker.tasks", "logic"], task_serializer='pickle', result_serializer='pickle',
#                 accept_content=['pickle'])

# worker = Celery("myapp", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"),
#                 include=["worker.tasks", "logic"], task_serializer='msgpack', result_serializer='msgpack',
#                 accept_content=['msgpack'])

# worker = Celery("myapp", backend=os.getenv("CELERY_BACKEND_URL"), broker=os.getenv("CELERY_BROKER_URL"), include=["worker.tasks", "logic"])


# Optional configuration, see the application user guide.
# worker.conf.update(
#     result_expires=3600,
# )

worker.conf.broker_transport_options = {
    'confirm_publish': True,
    #'acknowledgement_timeout':3600000 #1h,
    'acknowledgement_timeout': 86400000  # 24h
}

worker.conf.update(
    result_expires=864000,
    #result_expires=86400,
)

if __name__ == "__main__":
    worker.start()
