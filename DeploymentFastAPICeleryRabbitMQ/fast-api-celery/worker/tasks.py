import importlib
import sys
import logging
from celery import Task
from .celery import worker
from datetime import datetime
import numpy as np
import cv2
import base64

class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logging.info('Loading Model...')
            sys.path.append("..")
            module_import = importlib.import_module(self.path[0])
            model_obj = getattr(module_import, self.path[1])
            self.model = model_obj()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@worker.task(ignore_result=False,
             bind=True,
             base=PredictTask,
             path=('logic.model', 'ImageWellExposedModel'),
             name='{}.{}'.format(__name__, 'is_Image_WellExposedByHisto'))

def is_Image_WellExposedByHisto(self, imageBase64:str, filename:str, lat: float, lon: float, UTCdate: datetime):
    image_bytes = base64.b64decode(imageBase64)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    imageRGB = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    return self.model.is_Image_WellExposedByHisto(imageRGB, filename, lat, lon, UTCdate)

@worker.task(ignore_result=False,
             bind=True,
             base=PredictTask,
             path=('logic.model', 'ImageWellExposedModel'),
             name='{}.{}'.format(__name__, 'get_sunrise_sunset'))

def get_sunrise_sunset(self, lat: float, lon: float, UTCdate: datetime):
    return self.model.get_sunrise_sunset(lat, lon, UTCdate)

@worker.task(ignore_result=False,
             bind=True,
             base=PredictTask,
             path=('logic.modelApple', 'AppleSegmentationModel'),
             name='{}.{}'.format(__name__, 'get_apple_automatic_rois'))
def get_apple_automatic_rois(self, imageBase64: str, filename: str, jsonBase64ImageROIs: str):
    image_bytes = base64.b64decode(imageBase64)
    image_size = len(image_bytes)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    imageRGB = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    # Get the width and height
    height, width, _ = imageRGB.shape
    return self.model.get_apple_automatic_rois(imageRGB, image_size, height, width, filename, jsonBase64ImageROIs)

@worker.task(ignore_result=False,
             bind=True,
             base=PredictTask,
             path=('logic.modelApple', 'AppleSegmentationModel'),
             name='{}.{}'.format(__name__, 'get_apple_automatic_rois_with_indicators'))
def get_apple_automatic_rois_with_indicators(self, imageBase64: str, filename: str, jsonBase64ImageROIs: str):
    image_bytes = base64.b64decode(imageBase64)
    image_size = len(image_bytes)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    imageRGB = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    # Get the width and height
    height, width, _ = imageRGB.shape
    return self.model.get_apple_automatic_rois_with_indicators(imageRGB, image_size, height, width, filename, jsonBase64ImageROIs)

@worker.task(ignore_result=False,
             bind=True,
             base=PredictTask,
             path=('logic.modelLinden', 'LindenModel'),
             name='{}.{}'.format(__name__, 'get_classification_linden'))
def get_classification_linden(self, imageBase64: str, filename: str, jsonBase64ImageROIs: str):
    image_bytes = base64.b64decode(imageBase64)
    image_size = len(image_bytes)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    imageRGB = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    # Get the width and height
    height, width, _ = imageRGB.shape
    return self.model.get_classification_linden(imageRGB, filename, jsonBase64ImageROIs)

@worker.task(ignore_result=False,
             bind=True,
             base=PredictTask,
             path=('logic.modelLinden2', 'LindenSegmentationModel'),
             name='{}.{}'.format(__name__, 'get_linden_automatic_rois'))
def get_apple_automatic_rois(self, imageBase64: str, filename: str, jsonBase64ImageROIs: str):
    image_bytes = base64.b64decode(imageBase64)
    image_size = len(image_bytes)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    imageRGB = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    # Get the width and height
    height, width, _ = imageRGB.shape
    return self.model.get_linden_automatic_rois(imageRGB, image_size, height, width, filename, jsonBase64ImageROIs)