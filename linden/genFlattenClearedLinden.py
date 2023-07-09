import os
import json

def update_json_file(folder_path, json_file):
    fullnamejson = os.path.join(folder_path, json_file)

    # Wczytaj dane z pliku json
    with open(fullnamejson, 'r') as file:
        data = json.load(file)

    # Wybierz pliki jpg z folderu
    jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

    # Zaktualizuj dane json, usuwając obiekty, których pliki nie istnieją w folderze
    updated_data = {key: value for key, value in data.items() if value['filename'] in jpg_files}

    # Zapisz zaktualizowane dane do pliku json
    with open(fullnamejson, 'w') as file:
        json.dump(updated_data, file, indent=4)


# Zaktualizuj plik json na podstawie plików jpg w folderze ....
update_json_file('dataset_2023_07_09_11_07_54/train', 'via_region_data.json')
update_json_file('dataset_2023_07_09_11_07_54/val', 'via_region_data.json')
update_json_file('dataset_2023_07_09_11_07_54/test', 'via_region_data.json')
