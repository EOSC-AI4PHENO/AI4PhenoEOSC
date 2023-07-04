import os
import shutil

# Definiuję ścieżki
source_dir = 'oznaczone_jablka'
target_dir = 'oznaczone_jablka_flatten'

# Tworzę folder docelowy, jeśli nie istnieje
os.makedirs(target_dir, exist_ok=True)

i = 1
# Iteruję przez wszystkie pliki i podfoldery w folderze źródłowym
for root, dirs, files in os.walk(source_dir):

    # Przeszukuję wszystkie pliki w bieżącym folderze
    for file in files:

        # Jeśli plik to jpg lub json
        if file.endswith('.jpg') or file.endswith('.json'):
            # Sprawdzam, czy istnieje plik o tej samej nazwie z drugim rozszerzeniem
            base_name = os.path.splitext(file)[0]
            other_ext = '.json' if file.endswith('.jpg') else '.jpg'
            other_file = base_name + other_ext

            # Jeśli istnieje taka para, kopiuję oba pliki do folderu docelowego
            if other_file in files:
                print(i)
                shutil.copy2(os.path.join(root, file), target_dir)
                shutil.copy2(os.path.join(root, other_file), target_dir)
                i = i + 1