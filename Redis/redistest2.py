import redis
import pandas as pd

# Utwórz połączenie do bazy danych Redis
r = redis.Redis(host='10.0.20.50', port=6379, db=0)

# Pobierz wszystkie klucze
keys = r.keys()

# Pobierz wszystkie wartości dla każdego klucza
data = {key.decode("utf-8"): r.get(key).decode("utf-8") for key in keys}

# Tworzymy DataFrame z danymi
df = pd.DataFrame(list(data.items()), columns=['Key', 'Value'])

# Zapisujemy DataFrame do pliku Excela
df.to_excel('redis_data1.xlsx', index=False)
