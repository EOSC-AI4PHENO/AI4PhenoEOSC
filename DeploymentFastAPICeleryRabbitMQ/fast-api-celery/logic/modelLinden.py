import cv2
import numpy as np
from . import grpcLindenClassification
from . import Convert2Polygon
import base64
import json
#from models import LindenDecision
#from ..api.models import LindenDecision
from api.models import LindenDecision

class LindenModel:
    def __init__(self):
        self.m = 7.0  # not used only example
        self.q = 0.5  # not used only example

    def cropImages(self, imageRGB: np.ndarray, jsonBase64ImageROIs: str):
        height, width, _ = imageRGB.shape
        jsonBase64ImageROIsPolygon = Convert2Polygon.Convert2Polygon1(jsonBase64ImageROIs, width, height)

        # Dekodowanie base64
        decoded_json = base64.b64decode(jsonBase64ImageROIsPolygon).decode('utf-8')

        # Konwersja na słownik Pythona
        json_data = json.loads(decoded_json)

        # Pierwszy klucz w słowniku
        first_key = list(json_data.keys())[0]

        # Wszystkie regiony
        regions = json_data[first_key]["regions"]

        images_roi = []

        # Przejście przez wszystkie regiony
        for region_key in regions.keys():
            region = regions[region_key]

            # Współrzędne punktów
            all_points_x = region["shape_attributes"]["all_points_x"]
            all_points_y = region["shape_attributes"]["all_points_y"]

            # Obliczanie prostokąta otaczającego
            min_x = min(all_points_x)
            max_x = max(all_points_x)
            min_y = min(all_points_y)
            max_y = max(all_points_y)

            image_roi = imageRGB[min_y:max_y, min_x:max_x]
            images_roi.append(image_roi)

        return images_roi

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

    # def get_classification_linden(self, imageRGB: np.ndarray, filename: str, jsonBase64ImageROI: str):
    #     croppedImagesList = self.cropImages(imageRGB, jsonBase64ImageROI)
    #
    #     predicted_labels_list = []
    #
    #     for croppedImage in croppedImagesList:
    #         prediction = grpcLindenClassification.infer(croppedImage)
    #         predicted_labels = np.argmax(prediction)
    #         predicted_labels_list.append(predicted_labels == 1)
    #
    #     #predicted_labels_list = list(map(bool, predicted_labels_list))
    #
    #     return filename, predicted_labels_list

def get_classification_linden(self, imageRGB: np.ndarray, filename: str, jsonBase64ImageROI: str):
    croppedImagesList = self.cropImages(imageRGB, jsonBase64ImageROI)

    linden_decisions = []

    for croppedImage in croppedImagesList:
        prediction = grpcLindenClassification.infer(croppedImage)
        predicted_label = np.argmax(prediction)

        # Create new LindenDecision object
        linden_decision = LindenDecision(
            is_flowering=int(predicted_label),
            confidence_score=float(prediction),
            message="Linden is flowering." if predicted_label == 1 else "Linden is NOT flowering."
        )

        linden_decisions.append(linden_decision)

    return filename, linden_decisions
