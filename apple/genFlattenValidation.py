import os
import json

def validation_json_files(folder_path):
    i = 1
    # Przechodzi przez wszystkie pliki JSON w folderze
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)

            nazwa_bez_rozszerzeniaJSON = os.path.splitext(filename)[0]

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
                    i = i + 1
                    print(f'{i}.{filename}')

folder_path = "oznaczone_jablka_flatten_oryg_input"  # Ścieżka do folderu
#validation_json_files(folder_path)
