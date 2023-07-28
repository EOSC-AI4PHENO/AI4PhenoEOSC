import redis

# Utwórz połączenie do bazy danych Redis
r = redis.Redis(host='10.0.20.50', port=6379, db=0)

# Wyczyść bieżącą bazę danych
r.flushdb()
