import cv2
import numpy as np
from . import grpcJarek2
from . import Convert2Polygon
import base64
import json

class LindenModel:
    def __init__(self):
        self.m = 7.0  # not used only example
        self.q = 0.5  # not used only example

    def cropImage(self, imageRGB: np.ndarray, jsonBase64ImageROIs: str):
        height, width, _ = imageRGB.shape
        jsonBase64ImageROIsPolygon = Convert2Polygon.Convert2Polygon1(jsonBase64ImageROIs, width, height)

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

    def get_classification_linden(self, imageRGB: np.ndarray, filename: str, jsonBase64ImageROI: str):
        cropedImage = self.cropImage(imageRGB, jsonBase64ImageROI)
        prediction = grpcJarek2.infer(cropedImage)
        predicted_labels = np.argmax(prediction)

        if predicted_labels == 1:
            return filename, True
        else:
            return filename, False
