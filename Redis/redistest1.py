from celery import Celery
import redis

app = Celery('myapp', broker='amqp://guest@10.0.20.50//')
workers = app.control.inspect().active()
for worker in workers:
    print(worker)

app = Celery('myapp', broker='amqp://guest@10.0.20.50//')
r = redis.Redis(host='10.0.20.50', port=6379, db=0)

worker_name = "celery@0df2087bebd4"  # Zmień na nazwę workera, który Cię interesuje
track_ids = r.lrange(worker_name, 0, -1)  # Zwraca wszystkie track_id dla danego workera
for track_id in track_ids:
    print(track_id)