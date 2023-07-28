import redis

redis_client = redis.Redis(host='10.0.20.50', port=6379, db=0)

track_ids = redis_client.lrange(worker_id, 0, -1)

# Pobierz wszystkie klucze (track_id)
all_keys = r.keys('*')

# Wyświetl wszystkie klucze
for key in all_keys:
    print(key.decode())

# Pobierz i wyświetl liczbę wszystkich kluczy
num_keys = len(all_keys)
print(f"Number of keys: {num_keys}")