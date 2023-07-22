from astral import Observer
import pytz
from astral.sun import sun
from datetime import datetime

# class FakeModel:
#     def __init__(self):
#         self.m = 7.0
#         self.q = 0.5
#     def predict(self, x):
#         return self.m * x + self.q
#
class ImageWellExposedModel:
    def __init__(self):
        self.m = 7.0
        self.q = 0.5
    def get_sunrise_sunset(self,lat, lon, UTCdate):
        observer = Observer(latitude=lat, longitude=lon)
        s = sun(observer, date=UTCdate)

        UTCsunrise = s['sunrise'].astimezone(pytz.timezone('UTC'))
        UTCsunset = s['sunset'].astimezone(pytz.timezone('UTC'))

        return UTCsunrise, UTCsunset

# Tworzę instancję klasy WellExposedModel
model = ImageWellExposedModel()

# Wartości do funkcji get_sunrise_sunset
lat = 52.2297  # Przykładowa szerokość geograficzna dla Warszawy
lon = 21.0122  # Przykładowa długość geograficzna dla Warszawy
UTCdate = datetime.utcnow()  # Aktualna data i czas UTC

# Wywołanie funkcji get_sunrise_sunset
sunrise, sunset = model.get_sunrise_sunset(lat, lon, UTCdate)

# Wydrukowanie wyników
print(f"UTC sunrise: {sunrise}")
print(f"UTC sunset: {sunset}")