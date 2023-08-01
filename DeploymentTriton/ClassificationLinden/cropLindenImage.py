import json
import os
import cv2
import numpy as np
import base64
import Convert2Polygon

def base64_to_json(base64_string):
    # Kodujemy ciąg base64 z powrotem do bajtów
    base64_bytes = base64_string.encode('utf-8')

    # Dekodujemy bajty base64 z powrotem do oryginalnych bajtów
    json_bytes = base64.b64decode(base64_bytes)

    # Zapisujemy oryginalne bajty z powrotem do pliku JSON
    fullname = "your_output_file.json"
    with open(fullname, 'wb') as file:
        file.write(json_bytes)

    return fullname

def json_to_base64(fullname):
    # Otwórz plik w trybie binarnym i odczytaj
    with open(fullname, 'rb') as file:
        json_bytes = file.read()

    # Konwertuj bajty na base64
    base64_bytes = base64.b64encode(json_bytes)

    # Dekoduj bajty base64 na string
    base64_string = base64_bytes.decode('utf-8')

    # Zamień string base64 na format JSON
    base64_json = json.dumps(base64_string)

    return base64_json


def cropImage(imageRGB: np.ndarray, jsonBase64ImageROIs: str):
    height, width, _ = imageRGB.shape
    jsonBase64ImageROIsPolygon=Convert2Polygon.Convert2Polygon1(jsonBase64ImageROIs, width, height)

    base64_to_json(jsonBase64ImageROIsPolygon)

    # Dekodowanie base64
    decoded_json = base64.b64decode(jsonBase64ImageROIsPolygon).decode('utf-8')

    # Konwersja na słownik Pythona
    json_data = json.loads(decoded_json)

    # Pierwszy klucz w słowniku
    first_key = list(json_data.keys())[0]

    # Pierwszy region
    first_region = json_data[first_key]["regions"]['0']

    # Współrzędne punktów
    all_points_x = first_region["shape_attributes"]["all_points_x"]
    all_points_y = first_region["shape_attributes"]["all_points_y"]

    # Obliczanie prostokąta otaczającego
    min_x = min(all_points_x)
    max_x = max(all_points_x)
    min_y = min(all_points_y)
    max_y = max(all_points_y)

    image_roi = imageRGB[min_y:max_y, min_x:max_x]
    return image_roi


# fullname = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_Flowering/1/2022-06-19_02.48.33_class_1.jpg'
# image = cv2.imread(fullname)
#
# fullnameROIs = 'via_project_1Aug2023_7h29m_json.json'
#
# jsonBase64ImageROIs = json_to_base64(fullnameROIs)
#
# image_roi = cropImage(image, jsonBase64ImageROIs)
#
# # Zapis obrazu do pliku
# cv2.imwrite('output_image.jpg', cv2.cvtColor(image_roi, cv2.COLOR_RGB2BGR))
