from datetime import datetime
import cv2
import numpy as np
# import modelJarek as modellib
from .modelJarek import MaskRCNN
from .config import Config
from .grpcJarek2 import infer
import skimage
from skimage.measure import find_contours
import base64
import json
from . import Convert2Polygon
from . import roi_intersection
from . import calculate_indicators_with_area_Jarek
import pandas as pd

class AppleDeploymentConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "apple"

    GPU_COUNT = 1

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + balloon

    # Number of training steps
    EPOCHS = 500
    STEPS_PER_EPOCH = 61

    # Number of gt instances to use in batch
    MAX_GT_INSTANCES = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    # see REMARK in the description
    USE_MINI_MASK = False

    # TF2 feature - now you can run the model interactively
    RUN_EAGERLY = True


#####################################################################

class AppleSegmentationModel:
    def load_image(self, image):
        """Load the specified image and return a [H,W,3] Numpy array.
        """
        # If grayscale. Convert to RGB for consistency.
        if image.ndim != 3:
            image = skimage.color.gray2rgb(image)
        # If has an alpha channel, remove it for consistency
        if image.shape[-1] == 4:
            image = image[..., :3]
        return image

    def results_to_json(self, results, filename, file_size):
        # Inicjalizuj strukturę pliku JSON
        json_file = {
            filename: {
                "fileref": "",
                "size": file_size,
                "filename": filename,
                "base64_img_data": "",
                "file_attributes": {},
                "regions": {},
            }
        }

        # Przejdź przez wszystkie regiony wyników
        for i in range(len(results['rois'])):
            # Wyodrębnij punkty (x,y) wielokąta z maski
            all_points_x, all_points_y = self.mask_to_polygon(results['masks'][:, :, i])

            # Dodaj region do pliku JSON
            json_file[filename]["regions"][str(i)] = {
                "shape_attributes": {
                    "name": "polygon",
                    "all_points_x": [int(x) for x in all_points_x],
                    "all_points_y": [int(y) for y in all_points_y]
                },
                "region_attributes": {},
            }
        return json_file

    def mask_to_polygon(self, mask):
        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros((mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)

        # Dla wielu obiektów w jednej masce, wybierz ten z największym polem
        largest_contour = max(contours, key=lambda x: x.shape[0])

        # Przekształć kontury do formatu (x,y)
        points_x, points_y = np.fliplr(largest_contour).T

        return points_x.tolist(), points_y.tolist()

    def __init__(self):
        self.m = 7.0  # not used only example
        self.q = 0.5  # not used only example

    def get_apple_automatic_rois(self, imageRGB: np.ndarray, image_size: int, height: int, width: int, filename: str,
                                 jsonBase64ImageROIs: str) -> tuple[str, str]:

        config = AppleDeploymentConfig()
        image = self.load_image(imageRGB)
        # model = modellib.MaskRCNN(mode="inference", model_dir="/home", config=config)
        model = MaskRCNN(mode="inference", model_dir="/home", config=config)
        results = model.detect([image], verbose=1)
        r = results[0]

        json_results = self.results_to_json(r, filename, image_size)
        json_str = json.dumps(json_results)
        json_apple_rois_b64 = base64.b64encode(json_str.encode()).decode()

        if jsonBase64ImageROIs is None:
            # Koduj ciąg tekstowy do base64
            # nie ma regionów gdzie szukać jabłek, zwróć z całego obrazu

            return filename, json_apple_rois_b64
        else:
            jsonBase64ImageROIsPolygon = Convert2Polygon.Convert2Polygon2(jsonBase64ImageROIs, width, height)
            json_apple_rois_b64_filtered = roi_intersection.filter_json_file1(jsonBase64ImageROIsPolygon, json_apple_rois_b64, width, height)
            return filename, json_apple_rois_b64_filtered

    def get_apple_automatic_rois_with_indicators(self, imageRGB: np.ndarray, image_size: int, height: int, width: int, filename: str,
                                 jsonBase64ImageROIs: str):

        config = AppleDeploymentConfig()
        image = self.load_image(imageRGB)
        # model = modellib.MaskRCNN(mode="inference", model_dir="/home", config=config)
        model = MaskRCNN(mode="inference", model_dir="/home", config=config)
        results = model.detect([image], verbose=1)
        r = results[0]

        json_results = self.results_to_json(r, filename, image_size)
        json_str = json.dumps(json_results)
        json_apple_rois_b64 = base64.b64encode(json_str.encode()).decode()

        if jsonBase64ImageROIs is None:
            # Koduj ciąg tekstowy do base64
            # nie ma regionów gdzie szukać jabłek, zwróć z całego obrazu

            df_local = calculate_indicators_with_area_Jarek.calculate_indicators(imageRGB, json_apple_rois_b64)

            # Sprawdź, czy df_local jest pusty
            if df_local.empty:
                r_av = g_av = b_av = r_sd = g_sd = b_sd = bri_av = bri_sd = gi_av = gei_av = gei_sd = ri_av = ri_sd = bi_av = bi_sd = avg_width = avg_height = avg_area = number_of_apples = -1
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
                number_of_apples = int(df_local["number_of_apples"].iloc[0])

            return filename, json_apple_rois_b64, r_av, g_av, b_av, r_sd, g_sd, b_sd, bri_av, bri_sd, gi_av, gei_av, gei_sd, ri_av, ri_sd, bi_av, bi_sd, avg_width, avg_height, avg_area, number_of_apples
        else:
            jsonBase64ImageROIsPolygon = Convert2Polygon.Convert2Polygon2(jsonBase64ImageROIs, width, height)
            json_apple_rois_b64_filtered = roi_intersection.filter_json_file1(jsonBase64ImageROIsPolygon, json_apple_rois_b64, width, height)
            df_local = calculate_indicators_with_area_Jarek.calculate_indicators(imageRGB, json_apple_rois_b64_filtered)

            # Sprawdź, czy df_local jest pusty
            if df_local.empty:
                r_av = g_av = b_av = r_sd = g_sd = b_sd = bri_av = bri_sd = gi_av = gei_av = gei_sd = ri_av = ri_sd = bi_av = bi_sd = avg_width = avg_height = avg_area = number_of_apples = -1
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
                number_of_apples = int(df_local["number_of_apples"].iloc[0])

            return filename, json_apple_rois_b64_filtered, r_av, g_av, b_av, r_sd, g_sd, b_sd, bri_av, bri_sd, gi_av, gei_av, gei_sd, ri_av, ri_sd, bi_av, bi_sd, avg_width, avg_height, avg_area, number_of_apples


# # Tworzę instancję klasy AppleSegmentationModel
# model = AppleSegmentationModel()
#
# # Wartości do funkcji get_sunrise_sunset
# lat = 52.2297  # Przykładowa szerokość geograficzna dla Warszawy
# lon = 21.0122  # Przykładowa długość geograficzna dla Warszawy
# UTCdate = datetime.utcnow()  # Aktualna data i czas UTC
#
# # Wywołanie funkcji get_sunrise_sunset
# sunrise, sunset = model.get_sunrise_sunset(lat, lon, UTCdate)
#
# # Wydrukowanie wyników
# print(f"UTC sunrise: {sunrise}")
# print(f"UTC sunset: {sunset}")
