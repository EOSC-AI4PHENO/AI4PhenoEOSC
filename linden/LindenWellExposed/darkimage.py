import cv2
import os
import pandas as pd
from datetime import time
import numpy as np
from tqdm import tqdm
from astral.sun import sun
from astral import Observer
#from concurrent.futures import ProcessPoolExecutor

def extract_time_from_filename(filename):
    time_str = filename.split("_")[1]
    hour, minute, second = map(int, time_str.split("."))
    return time(hour, minute, second)

def is_image_dark(img_path, threshold=90):
    # Wczytaj obraz
    img = cv2.imread(img_path)

    # Konwertuj obraz do przestrzeni kolorów szarości
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Oblicz średnią wartość pikseli
    mean_value = np.mean(gray_img)

    # Zwróć, czy obraz jest ciemny
    return mean_value < threshold

def process_images_in_folder(folder_path):
    #ile=1
    data = []
    #for filename in os.listdir(folder_path):
    for filename in tqdm(os.listdir(folder_path), desc=f'Processing images in {folder_path}'):
        #rint(ile)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            #print(filename)
            full_path = os.path.join(folder_path, filename)
            extracted_time = extract_time_from_filename(filename)
            dark_flag = is_image_dark(full_path)
            data.append([full_path, filename, folder_path, extracted_time, dark_flag, 'zbyt ciemny' if dark_flag else 'jest OK'])
        #ile=ile+1
    return data

#[process_image(file, brightness_values) for file in tqdm(files, desc=f'Processing images in {folder_path}')]

def save_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=['fullname', 'filename', 'directory', 'time', 'is_image_dark', 'opis'])
    df.to_excel(output_file, index=False)

# Definiuj ścieżkę do folderu z obrazami
images_folder_path1 = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI/0"
images_folder_path2 = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI/1"

# Używamy funkcji dla dwóch folderów
data = process_images_in_folder(images_folder_path1) + process_images_in_folder(images_folder_path2)

# Zapisujemy wyniki do pliku Excel
save_to_excel(data, 'dark_or_bright.xlsx')
