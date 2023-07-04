import os
import json

# ścieżka do folderu z plikami JSON
folder_path = "oznaczone_jablka_flatten_merged"
merged_data = {}

# dla każdego pliku JSON w folderze
for file_name in os.listdir(folder_path):
    # sprawdź czy plik ma rozszerzenie .json
    if file_name.endswith('.json'):
        file_path = os.path.join(folder_path, file_name)

        # otwórz plik i załaduj dane
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # połącz dane
        merged_data.update(data)

# usuń oryginalne pliki
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):
        os.remove(os.path.join(folder_path, file_name))

# zapisz połączone dane do nowego pliku
mergedfile_path = os.path.join(folder_path, 'merged.json')
with open(mergedfile_path, 'w') as json_file:
    json.dump(merged_data, json_file, indent=4)