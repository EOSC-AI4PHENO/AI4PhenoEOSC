import base64
import json
import numpy as np
from pydantic import BaseModel
from . import Convert2Polygon
from . import grpcLindenClassification
import cv2

class LindenModel:
    def __init__(self):
        self.m = 7.0  # not used only example
        self.q = 0.5  # not used only example

    def cropImages(self, imageRGB: np.ndarray, jsonBase64ImageROIs: str, image_shape):
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
            #image_roi = image_roi.resize(image_shape)  # Dostosowanie rozmiaru
            image_roi = cv2.resize(image_roi, image_shape)  # Dostosowanie rozmiaru za pomocą OpenCV

            images_roi.append(image_roi)

        return np.array(images_roi)

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
        width = 321
        height = 384
        image_shape = (width, height)

        croppedImagesList = self.cropImages(imageRGB, jsonBase64ImageROI, image_shape)
        isFloweringList = []
        isFloweringConfidence = []

        for croppedImage in croppedImagesList:
            prediction = grpcLindenClassification.infer(croppedImage)
            predicted_label = np.argmax(prediction)
            predicted_score = np.max(prediction)

            # Append to lists instead of creating a LindenDecision object
            isFloweringList.append(int(predicted_label))
            isFloweringConfidence.append(float(predicted_score))

        return filename, isFloweringList, isFloweringConfidence

