import os
import json

folder_path = "oznaczone_jablka_flatten_cleared"  # Ścieżka do folderu

i = 1

# Przechodzi przez wszystkie pliki JSON w folderze
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        filepath = os.path.join(folder_path, filename)

        nazwa_bez_rozszerzeniaJSON = os.path.splitext(filename)[0]
        # print(f'Nazwa pliku JSON: {filename},nazwa_bez_rozszerzeniaJSON: {nazwa_bez_rozszerzeniaJSON}')

        # Wczytanie pliku JSON
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)

        # Utworzenie kopii słownika do iteracji (ponieważ nie możemy modyfikować słownika podczas iteracji)
        data_copy = data.copy()

        # Sprawdzenie każdego obiektu w słowniku
        for key, value in data_copy.items():
            filenameJPG = value['filename']
            nazwa_bez_rozszerzeniaJPG = os.path.splitext(filenameJPG)[0]
            # Sprawdzenie, czy wartość "filename" jest różna od nazwy pliku JSON z rozszerzeniem ".jpg"
            if nazwa_bez_rozszerzeniaJPG != nazwa_bez_rozszerzeniaJSON:
                # Usuwanie obiektu, jeśli wartość "filename" jest różna
                # print(f'{a},key={key}')
                i = i + 1
                print(f'{i}.{filename}')
                del data[key]

        # Zapisanie zmodyfikowanego pliku JSON
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)
