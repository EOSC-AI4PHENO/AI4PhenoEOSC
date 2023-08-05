import pandas as pd
import os
import shutil
from tqdm import tqdm

# Wczytaj plik Excel
df = pd.read_excel('darkimageHistogramSun6.xlsx')

# Filtruj tylko rekordy, które są dobrze naświetlone
df = df[df['is_well_exposed'] == True]

# Przejdź przez każdy rekord w ramce danych
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Copying files"):
    # Pobierz pełną ścieżkę pliku
    source_path = row['fullname']

    # Utwórz ścieżkę docelową, zmieniając katalog nadrzędny
    dest_path = source_path.replace('/Linden_Photos/', '/Linden_Photos_WellExposed/')

    # Upewnij się, że katalog docelowy istnieje
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Skopiuj plik
    shutil.copy2(source_path, dest_path)
