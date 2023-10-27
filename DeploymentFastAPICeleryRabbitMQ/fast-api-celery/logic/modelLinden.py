import base64
import json
import numpy as np
from pydantic import BaseModel
from . import Convert2Polygon
from . import grpcLindenClassification
import cv2
from . import Convert2Polygon
from . import roi_intersection
from . import calculate_indicators_with_area_Jarek

class LindenModel:
    def __init__(self):
        self.m = 7.0  # not used only example
        self.q = 0.5  # not used only example

    def cropImages(self, imageRGB: np.ndarray, jsonBase64ImageROIs: str, image_shape):
        height, width, _ = imageRGB.shape

        jsonBase64ImageROIsPolygon = Convert2Polygon.Convert2Polygon2(jsonBase64ImageROIs, width, height)

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

    def get_classification_linden_with_indicators(self, imageRGB: np.ndarray, filename: str, jsonBase64ImageROI: str):
        width = 321
        height = 384
        image_shape = (width, height)

        ### START Indicators
        json_linden_rois_b64_Polygon = Convert2Polygon.Convert2Polygon2(jsonBase64ImageROI, imageRGB.shape[0], imageRGB.shape[1])
        df_local = calculate_indicators_with_area_Jarek.calculate_indicators(imageRGB, json_linden_rois_b64_Polygon)

        # Sprawdź, czy df_local jest pusty
        if df_local.empty:
            r_av = g_av = b_av = r_sd = g_sd = b_sd = bri_av = bri_sd = gi_av = gei_av = gei_sd = ri_av = ri_sd = bi_av = bi_sd = gi_sd = avg_width = avg_height = avg_area = number_of_apples = -1
        else:
            r_av = float(df_local["r.av"].iloc[0])
            g_av = float(df_local["g.av"].iloc[0])
            b_av = float(df_local["b.av"].iloc[0])
            r_sd = float(df_local["r.sd"].iloc[0])
            g_sd = float(df_local["g.sd"].iloc[0])
            b_sd = float(df_local["b.sd"].iloc[0])
            bri_av = float(df_local["bri.av"].iloc[0])
            bri_sd = float(df_local["bri.sd"].iloc[0])
            gi_av = float(df_local["gi.av"].iloc[0])
            gei_av = float(df_local["gei.av"].iloc[0])
            gei_sd = float(df_local["gei.sd"].iloc[0])
            ri_av = float(df_local["ri.av"].iloc[0])
            ri_sd = float(df_local["ri.sd"].iloc[0])
            bi_av = float(df_local["bi.av"].iloc[0])
            bi_sd = float(df_local["bi.sd"].iloc[0])
            gi_sd = float(df_local["gi.sd"].iloc[0])
            avg_width = float(df_local["avg_width"].iloc[0])
            avg_height = float(df_local["avg_height"].iloc[0])
            avg_area = float(df_local["avg_area"].iloc[0])
            number_of_lindens = int(df_local["number_of_apples"].iloc[0])
        ### END Indicators

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

        return filename, isFloweringList, isFloweringConfidence, r_av, g_av, b_av, r_sd, g_sd, b_sd, bri_av, bri_sd, gi_av, gei_av, gei_sd, ri_av, ri_sd, bi_av, bi_sd, gi_sd, avg_width, avg_height, avg_area, number_of_lindens

