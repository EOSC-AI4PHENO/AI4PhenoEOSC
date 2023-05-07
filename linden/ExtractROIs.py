import json
import os
import cv2
import numpy as np


def read_json(nazwa_pliku):
    with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
        dane = json.load(plik)
    return dane


def ExtractAndSave(fullname, x_min, y_min, x_max, y_max):
    image = cv2.imread(fullname)

    head_tail = os.path.split(fullname)
    dirsrc = head_tail[0]
    filename = head_tail[1]

    # Przycinanie (crop) ROI
    image_roi = image[y_min:y_max, x_min:x_max]

    # Zapisz ROI do pliku JPG
    output_filename = os.path.splitext(filename)[0] + '_ROI.jpg'

    dirsrc = dirsrc.replace("Linden_Photos", "Linden_Photos_ROI")
    dst = os.path.join(dirsrc, output_filename)

    cv2.imwrite(dst, image_roi)


# Wczytaj informacje o ROI
data = read_json('ODUPP_2022.06.28.05.54.35._json.json')
image_data = data['ODUPP_2022.06.28.05.54.35.jpg669073']
filename = image_data['filename']
regions = image_data['regions']
shape_attributes = regions[0]['shape_attributes']
all_points_x = shape_attributes['all_points_x']
all_points_y = shape_attributes['all_points_y']

# Oblicz prostokąt otaczający wielokąt
polygon = np.array(list(zip(all_points_x, all_points_y)), dtype=np.int32)
x_min, y_min = np.min(polygon, axis=0)
x_max, y_max = np.max(polygon, axis=0)

root_folder = 'Linden_Photos'

iter = 1

for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file.lower().endswith('.jpg'):
            print(iter)
            fullname = os.path.join(root, file)
            print(fullname)
            ExtractAndSave(fullname, x_min, y_min, x_max, y_max)
            iter = iter + 1
