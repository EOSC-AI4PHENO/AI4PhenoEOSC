import json
import os
import cv2
import numpy as np
from tqdm import tqdm


def read_json(nazwa_pliku):
    with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
        dane = json.load(plik)
    return dane


def jitter_points(points_x, points_y, jitter_amount=5):
    jittered_x = [int(x + np.random.uniform(-jitter_amount, jitter_amount)) for x in points_x]
    jittered_y = [int(y + np.random.uniform(-jitter_amount, jitter_amount)) for y in points_y]

    return jittered_x, jittered_y


def ExtractAndSave(fullname, dest_folder, x_min, y_min, x_max, y_max):
    image = cv2.imread(fullname)

    filename = os.path.basename(fullname)

    # Przycinanie (crop) ROI
    image_roi = image[y_min:y_max, x_min:x_max]

    # Zapisz ROI do pliku JPG
    output_filename = os.path.splitext(filename)[0] + '_ROI.jpg'
    dst = os.path.join(dest_folder, output_filename)

    cv2.imwrite(dst, image_roi)


# Wczytaj informacje o ROI
data = read_json('ODUPP_2022.06.28.05.54.35._json.json')
image_data = data['ODUPP_2022.06.28.05.54.35.jpg669073']
regions = image_data['regions']
shape_attributes = regions[0]['shape_attributes']

source_folders = [
    'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/Linden_Photos_WellExposed/0',
    'E:/!DeepTechnology/!Customers/!2023\Seth Software EOSC-AI4Pheno/Linden_Photos_WellExposed/1'
]

dest_folders = [
    'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/Linden_Photos_WellExposed_ROIs/0',
    'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/Linden_Photos_WellExposed_ROIs/1'
]

iter = 1

for src_folder, dest_folder in zip(source_folders, dest_folders):
    all_files = [os.path.join(src_folder, file) for file in os.listdir(src_folder) if file.lower().endswith('.jpg')]

    for file in tqdm(all_files, desc=f"Processing images from {src_folder}"):
        # Losowe zmiany współrzędnych polygonu dla każdego obrazu
        jittered_points_x, jittered_points_y = jitter_points(shape_attributes['all_points_x'],
                                                             shape_attributes['all_points_y'], jitter_amount=10)

        # Oblicz prostokąt otaczający wielokąt dla jittered points
        polygon = np.array(list(zip(jittered_points_x, jittered_points_y)), dtype=np.int32)
        x_min, y_min = np.min(polygon, axis=0)
        x_max, y_max = np.max(polygon, axis=0)

        #print(iter)
        #print(file)
        ExtractAndSave(file, dest_folder, x_min, y_min, x_max, y_max)
        iter += 1
