from astral import Observer
import pytz
from astral.sun import sun

# class FakeModel:
#     def __init__(self):
#         self.m = 7.0
#         self.q = 0.5
#     def predict(self, x):
#         return self.m * x + self.q
#
class WellExposedModel:
    def __init__(self):
        self.m = 7.0
        self.q = 0.5
    def get_sunrise_sunset(self,lat, lon, UTCdate):
        observer = Observer(latitude=lat, longitude=lon)
        s = sun(observer, date=UTCdate)

        UTCsunrise = s['sunrise'].astimezone(pytz.timezone('UTC'))
        UTCsunset = s['sunset'].astimezone(pytz.timezone('UTC'))

        return UTCsunrise, UTCsunset