import os
import shutil

def podziel_folder(sciezka_folderu, maks_rozmiar):
    if not os.path.exists(sciezka_folderu):
        print("Podana ścieżka nie istnieje.")
        return

    # Zmiana bieżącego katalogu na ścieżkę folderu
    os.chdir(sciezka_folderu)

    # Ustalanie nazwy i numeru podfolderu
    podfolder_nazwa = "podfolder"
    podfolder_numer = 1

    # Tworzenie pierwszego podfolderu
    nowy_podfolder = f"{podfolder_nazwa}_{podfolder_numer}"
    os.makedirs(nowy_podfolder)

    # Iteracja po plikach w folderze
    rozmiar_podfolderu = 0
    for plik in os.listdir():
        if os.path.isfile(plik):
            rozmiar_pliku = os.path.getsize(plik)

            # Sprawdzanie, czy plik przekracza maksymalny rozmiar podfolderu
            if (rozmiar_podfolderu + rozmiar_pliku) > maks_rozmiar:
                # Tworzenie nowego podfolderu
                podfolder_numer += 1
                nowy_podfolder = f"{podfolder_nazwa}_{podfolder_numer}"
                os.makedirs(nowy_podfolder)
                rozmiar_podfolderu = 0

            # Przenoszenie pliku do podfolderu
            shutil.move(plik, os.path.join(nowy_podfolder, plik))
            rozmiar_podfolderu += rozmiar_pliku

# Przykładowe użycie:
sciezka_folderu = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC_NEW/linden/Linden_Photos_ROI - Copy/0"
maks_rozmiar = 500_000_000  # 500 MB
podziel_folder(sciezka_folderu, maks_rozmiar)
