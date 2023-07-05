import os
import shutil
import random
from datetime import datetime

def split_data(src_dir, val_pct, train_pct, test_pct):
    assert val_pct + train_pct + test_pct == 1.0, "Suma procentów powinna wynosić 1.0"

    # Utwórz nadrzędny katalog o nazwie "dataset_yyyy_MM_dd_HH_mm_ss"
    timestamp_str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    parent_dir = f"dataset_{timestamp_str}"

    # Lista docelowych katalogów
    dest_dirs = [os.path.join(parent_dir, dir_name) for dir_name in ['train', 'val',  'test']]

    # Utworzenie docelowych katalogów, jeśli jeszcze nie istnieją
    for dir in dest_dirs:
        os.makedirs(dir, exist_ok=True)

    # Wyszukanie wszystkich par plików JSON i JPG
    files = [file for file in os.listdir(src_dir) if file.endswith('.jpg') or file.endswith('.json')]

    # Grupowanie plików w pary
    pairs = {}
    for file in files:
        base = os.path.splitext(file)[0]
        if base not in pairs:
            pairs[base] = []
        pairs[base].append(file)

    # Losowe mieszanie par plików
    pairs = list(pairs.values())
    random.shuffle(pairs)

    # Rozdzielenie par plików na podzbiory
    total = len(pairs)
    val, train, test = pairs[:int(total*val_pct)], pairs[int(total*val_pct):int(total*(val_pct + train_pct))], pairs[int(total*(val_pct + train_pct)):]

    # Skopiowanie plików do odpowiednich katalogów
    for pair in val:
        for file in pair:
            shutil.copy(os.path.join(src_dir, file), dest_dirs[0])
    for pair in train:
        for file in pair:
            shutil.copy(os.path.join(src_dir, file), dest_dirs[1])
    for pair in test:
        for file in pair:
            shutil.copy(os.path.join(src_dir, file), dest_dirs[2])

    return dest_dirs

#train_dir, val_dir, test_dir = split_data('oznaczone_jablka_flatten_oryg_input', 0.7, 0.15, 0.15)
