import cv2
import os
import pandas as pd
from datetime import time
import numpy as np
from tqdm import tqdm

def extract_time_from_filename(filename):
    time_str = filename.split("_")[1]
    hour, minute, second = map(int, time_str.split("."))
    return time(hour, minute, second)


# def calculate_image_brightness(img_path):
#    image = cv2.imread(img_path)
#   return image.mean()

def calculate_image_brightness(img_path):
    # Wczytaj obraz
    img = cv2.imread(img_path)

    # Konwertuj obraz do przestrzeni kolorów szarości
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Oblicz średnią wartość pikseli
    mean_value = np.mean(gray_img)

    # Zwróć, czy obraz jest ciemny
    return mean_value


def process_image(file, brightness_values):
    folder_path, filename = file
    full_path = os.path.join(folder_path, filename)
    extracted_time = extract_time_from_filename(filename)
    brightness = calculate_image_brightness(full_path)
    is_daytime = time(6, 0, 0) <= extracted_time <= time(18, 0, 0)
    if is_daytime == 1:
        brightness_values.append(brightness)
    return [full_path, folder_path, filename, extracted_time, brightness, is_daytime]


# def process_images_in_folder(folder_path):
#    files = [(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".jpg") or filename.endswith(".png")]
#   return [process_image(file) for file in files]

def process_images_in_folder(folder_path, brightness_values):
    files = [(folder_path, filename) for filename in os.listdir(folder_path) if
             filename.endswith(".jpg") or filename.endswith(".png")]
    return [process_image(file, brightness_values) for file in tqdm(files, desc=f'Processing images in {folder_path}')]


def save_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=['fullname', 'directory', 'filename', 'time', 'brightness', 'is_daytime'])
    df.to_excel(output_file, index=False)


images_folder_path1 = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI/0"
images_folder_path2 = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI/1"

brightness_values = []

# Przetwarzamy obrazy w obu folderach
data = process_images_in_folder(images_folder_path1, brightness_values) + process_images_in_folder(images_folder_path2,
                                                                                                   brightness_values)

# Obliczamy średnią jasność dla obrazów wykonanych w ciągu dnia
#daytime_brightness_values = [row[4] for row in data if row[5]]
avg_brightness = sum(brightness_values) / len(brightness_values)

# Dodajemy wynik do danych
data.append(['', '', '', '', avg_brightness, 'Average brightness for 6-18'])

# Zapisujemy wyniki do pliku Excel
save_to_excel(data, 'darkimageAssesment.xlsx')
