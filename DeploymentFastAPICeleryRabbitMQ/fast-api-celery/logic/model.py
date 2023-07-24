# import ephem
from astral import Observer
import pytz
from astral.sun import sun
from datetime import datetime
import cv2
import numpy as np


# class FakeModel:
#     def __init__(self):
#         self.m = 7.0
#         self.q = 0.5
#     def predict(self, x):
#         return self.m * x + self.q
#
class ImageWellExposedModel:
    def __init__(self):
        self.m = 7.0  # not used only example
        self.q = 0.5  # not used only example

    # def convert_to_datetime(self, date_str) -> datetime:
    #     formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S.%f%z"]
    #     #2023-07-24T15:30:00.000Z
    #     #2023-07-24 15:30:00.000+0200
    #
    #     for fmt in formats:
    #         try:
    #             return datetime.strptime(date_str, fmt)
    #         except ValueError:
    #             pass
    #
    #     raise ValueError("Nieznany format daty: {}".format(date_str))

    def get_sunrise_sunset(self, lat: float, lon: float, UTCdate: datetime) -> tuple[datetime, datetime]:
        # UTCdate = self.convert_to_datetime(UTCdate)
        # a3 = UTCdate.strftime('%Y/%m/%d')
        observer = Observer(latitude=lat, longitude=lon)
        s = sun(observer, date=UTCdate)

        UTCsunrise = s['sunrise'].astimezone(pytz.timezone('UTC'))
        UTCsunset = s['sunset'].astimezone(pytz.timezone('UTC'))

        return UTCsunrise, UTCsunset

    def is_Image_WellExposedByHisto(self, imageRGB: np.ndarray, filename: str, lat: float = 52.2297,
                                    lon: float = 21.0122,
                                    UTCdate: datetime = None) -> tuple[bool, str]:
        # Wczytaj obraz w skali szarości

        low_threshold = 0.73
        high_threshold = 0.5

        image = cv2.cvtColor(imageRGB, cv2.COLOR_BGR2GRAY)

        # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Oblicz histogram
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])

        ### to remove
        total_pixels = image.shape[0] * image.shape[1]
        dark_pixels = np.sum(hist[:80])  # Można dostosować próg
        bright_pixels = np.sum(hist[176:])  # Można dostosować próg

        dark_pixels_stats = dark_pixels / total_pixels
        bright_pixels_stats = bright_pixels / total_pixels

        # Jeśli podano współrzędne geograficzne oraz datę i czas obrazu
        if lat and lon and UTCdate:

            image_time = UTCdate.time()

            # Oblicz czas wschodu i zachodu słońca
            UTCsunrise, UTCsunset = self.get_sunrise_sunset(lat, lon, UTCdate)

            # Jeżeli czas zdjęcia jest po zachodzie słońca lub przed wschodem słońca
            if image_time > UTCsunset.time() or image_time < UTCsunrise.time():
                return False, 'Image is too dark due to being taken after sunset or before sunrise', filename

        # Sprawdź, czy obraz jest za ciemny
        if dark_pixels_stats > low_threshold:  # 0.7
            return False, 'Image is too dark', filename
        # Sprawdź, czy obraz jest za jasny
        elif bright_pixels_stats > high_threshold:  # 0.5
            return False, 'Image is too bright', filename
        else:
            return True, 'Image is well exposed', filename

# # Tworzę instancję klasy WellExposedModel
# model = ImageWellExposedModel()
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
