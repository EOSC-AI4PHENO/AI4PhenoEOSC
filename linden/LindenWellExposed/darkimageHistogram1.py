import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import time
from datetime import date
from tqdm import tqdm


def extract_time_from_filename(filename):
    date_str = filename.split("_")[0]
    time_str = filename.split("_")[1]

    year1, month1, day1 = map(int, date_str.split("-"))
    hour1, minute1, second1 = map(int, time_str.split("."))

    date1 = date(year1, month1, day1)
    time1 = time(hour1, minute1, second1)

    return time1, date1


def is_image_well_exposed(image_path, low_threshold=0.3, high_threshold=0.7):
    # Wczytaj obraz w skali szarości
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Oblicz histogram
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    # Normalizuj histogram
    hist /= hist.sum()

    # Stwórz histogram używając matplotlib
    # plt.figure()
    # plt.title("Histogram obrazu")
    # plt.xlabel("Wartość piksela")
    # plt.ylabel("Ilość pikseli")
    # plt.plot(hist)
    # plt.xlim([0, 256])

    # Zapisz histogram do pliku
    # plt.savefig('histogram.png')

    # Oblicz skumulowany histogram
    cumulative_hist = np.cumsum(hist)

    # Stwórz histogram używając matplotlib
    # plt.figure()
    # plt.title("Skumulowany Histogram obrazu")
    # plt.xlabel("Wartość piksela")
    # plt.ylabel("Ilość pikseli")
    # plt.plot(cumulative_hist)
    # plt.xlim([0, 256])

    # Zapisz histogram do pliku
    # plt.savefig('cumulative_hist.png')

    # Sprawdź, czy obraz jest za ciemny
    # aint=76
    #aint = int(256 * low_threshold)
    if cumulative_hist[30] < low_threshold:
        return False, 'Image is too dark',cumulative_hist

    # Sprawdź, czy obraz jest za jasny
    # bint=179
    #bint = int(256 * high_threshold)
    if cumulative_hist[200] > high_threshold:
        return False, 'Image is too bright',cumulative_hist

    return True, 'Image is well exposed',cumulative_hist
def process_images_in_folder(folder_path):
    # ile=1
    data = []
    # for filename in os.listdir(folder_path):
    for filename in tqdm(os.listdir(folder_path), desc=f'Processing images in {folder_path}'):
        # rint(ile)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # print(filename)
            full_path = os.path.join(folder_path, filename)
            extracted_time, extracted_date = extract_time_from_filename(filename)
            result, message,cumulative_hist = is_image_well_exposed(full_path, 0.1, 0.99)
            data.append([full_path, filename, folder_path, extracted_date,extracted_time, result, message,
                         cumulative_hist[0],
                         cumulative_hist[10],
                         cumulative_hist[20],
                         cumulative_hist[30],
                         cumulative_hist[40],
                         cumulative_hist[50],
                         cumulative_hist[100],
                         cumulative_hist[150],
                         cumulative_hist[200],
                         cumulative_hist[210],
                         cumulative_hist[220],
                         cumulative_hist[230],
                         cumulative_hist[240],
                         cumulative_hist[250],
                         cumulative_hist[255]
                         ])
    return data

def save_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=['fullname', 'filename', 'directory', 'date', 'time', 'is_image_dark', 'message',
                                     'cumulative_hist_0',
                                     'cumulative_hist_10',
                                     'cumulative_hist_20',
                                     'cumulative_hist_30',
                                     'cumulative_hist_40',
                                     'cumulative_hist_50',
                                     'cumulative_hist_100',
                                     'cumulative_hist_150',
                                     'cumulative_hist_200',
                                     'cumulative_hist_210',
                                     'cumulative_hist_220',
                                     'cumulative_hist_230',
                                     'cumulative_hist_240',
                                     'cumulative_hist_250',
                                     'cumulative_hist_255',
                                     ])
    df.to_excel(output_file, index=False)


# Definiuj ścieżkę do folderu z obrazami
images_folder_path1 = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI/0"
images_folder_path2 = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI/1"

# Używamy funkcji dla dwóch folderów
data = process_images_in_folder(images_folder_path1) + process_images_in_folder(images_folder_path2)

# Zapisujemy wyniki do pliku Excel
save_to_excel(data, 'dark_or_bright_histogram1.xlsx')
