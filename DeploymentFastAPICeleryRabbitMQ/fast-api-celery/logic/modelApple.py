from datetime import datetime
import cv2
import numpy as np


class AppleSegmentationModel:
    def __init__(self):
        self.m = 7.0  # not used only example
        self.q = 0.5  # not used only example

    def get_apple_automatic_rois(self, imageBase64: str, filename: str, jsonBase64ImageROIs: str) -> tuple[str, str]:
        filename = filename
        jsonBase64AppleROIs = 'json2323...'
        return filename, jsonBase64AppleROIs

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
