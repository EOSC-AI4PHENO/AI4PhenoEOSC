import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import time
from datetime import date
from tqdm import tqdm
from timezonefinder import TimezoneFinder
import pytz
from astral.sun import sun
from astral import Observer
from datetime import datetime


def convert_to_utc(date1, time1):
    # Łączymy date1 i time1, aby utworzyć obiekt datetime
    local_time = datetime.combine(date1, time1)

    # Definiowanie strefy czasowej dla Warszawy
    warsaw_tz = pytz.timezone('Europe/Warsaw')

    # Lokalizacja czasu dla strefy czasowej Warszawy
    localized_time = warsaw_tz.localize(local_time)

    # Konwersja na czas UTC
    utc_datetime = localized_time.astimezone(pytz.UTC)

    # Podział na datę i czas
    utc_date = utc_datetime.date()
    utc_time = utc_datetime.time()

    return utc_date, utc_time


def extract_time_from_filename(filename):
    date_str = filename.split("_")[0]
    time_str = filename.split("_")[1]

    year1, month1, day1 = map(int, date_str.split("-"))
    hour1, minute1, second1 = map(int, time_str.split("."))

    date1 = date(year1, month1, day1)
    time1 = time(hour1, minute1, second1)

    return time1, date1


def get_timezone(lat, lon):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    return timezone_str


def get_sunrise_sunset(lat, lon, UTCdate):
    observer = Observer(latitude=lat, longitude=lon)
    s = sun(observer, date=UTCdate)

    UTCsunrise = s['sunrise'].astimezone(pytz.timezone('UTC'))
    UTCsunset = s['sunset'].astimezone(pytz.timezone('UTC'))

    return UTCsunrise, UTCsunset


def is_image_well_exposedByHisto(image_path, low_threshold=0.1, high_threshold=0.99, lat=None, lon=None, UTCdate=None,
                                 image_time=None):
    # Wczytaj obraz w skali szarości
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Oblicz histogram
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    # Normalizuj histogram
    hist /= hist.sum()

    # Oblicz skumulowany histogram
    cumulative_hist = np.cumsum(hist)

    # Jeśli podano współrzędne geograficzne oraz datę i czas obrazu
    if lat and lon and UTCdate and image_time:
        # Oblicz czas wschodu i zachodu słońca
        UTCsunrise, UTCsunset = get_sunrise_sunset(lat, lon, UTCdate)

        # Jeżeli czas zdjęcia jest po zachodzie słońca lub przed wschodem słońca
        if image_time > UTCsunset.time() or image_time < UTCsunrise.time():
            return False, 'Image is too dark due to being taken after sunset or before sunrise', cumulative_hist

    # Sprawdź, czy obraz jest za ciemny
    if cumulative_hist[30] < low_threshold:
        return False, 'Image is too dark', cumulative_hist

    # Sprawdź, czy obraz jest za jasny
    if cumulative_hist[200] > high_threshold:
        return False, 'Image is too bright', cumulative_hist

    return True, 'Image is well exposed', cumulative_hist


def process_images_in_folder(folder_path, low_threshold, high_threshold, lat, lon):
    # ile=1
    data = []
    # for filename in os.listdir(folder_path):
    for filename in tqdm(os.listdir(folder_path), desc=f'Processing images in {folder_path}'):
        # rint(ile)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # print(filename)
            full_path = os.path.join(folder_path, filename)
            extracted_time, extracted_date = extract_time_from_filename(filename)
            utc_date, utc_time = convert_to_utc(extracted_date, extracted_time)
            UTCsunrise, UTCsunset = get_sunrise_sunset(lat, lon, utc_date)
            result, message, cumulative_hist = is_image_well_exposedByHisto(full_path, low_threshold, high_threshold,
                                                                            lat, lon, utc_date, utc_time)
            data.append(
                [full_path, filename, folder_path, extracted_date, extracted_time, utc_date, utc_time, UTCsunrise.replace(tzinfo=None),
                 UTCsunset.replace(tzinfo=None), low_threshold,
                 high_threshold, lat,
                 lon,
                 result, message,
                 cumulative_hist[0],
                 cumulative_hist[10],
                 cumulative_hist[20],
                 cumulative_hist[30],
                 cumulative_hist[40],
                 cumulative_hist[50],
                 cumulative_hist[100],
                 cumulative_hist[150],
                 cumulative_hist[200],
                 cumulative_hist[210],
                 cumulative_hist[220],
                 cumulative_hist[230],
                 cumulative_hist[240],
                 cumulative_hist[250],
                 cumulative_hist[255]
                 ])
    return data


def save_to_excel(data, output_file):
    df = pd.DataFrame(data,
                      columns=['fullname', 'filename', 'directory', 'date', 'time', 'utc_date', 'utc_time',
                               'UTCsunrise', 'UTCsunset',
                               'low_threshold', 'high_threshold', 'lat', 'lon', 'is_image_dark_bright', 'message',
                               'cumulative_hist_0',
                               'cumulative_hist_10',
                               'cumulative_hist_20',
                               'cumulative_hist_30',
                               'cumulative_hist_40',
                               'cumulative_hist_50',
                               'cumulative_hist_100',
                               'cumulative_hist_150',
                               'cumulative_hist_200',
                               'cumulative_hist_210',
                               'cumulative_hist_220',
                               'cumulative_hist_230',
                               'cumulative_hist_240',
                               'cumulative_hist_250',
                               'cumulative_hist_255',
                               ])
    df.to_excel(output_file, index=False)


# przykładowe współrzędne i data
## utc_now = datetime.now(pytz.timezone('UTC')).date()
# lat, lon = 52.2297, 21.0122  # współrzędne dla Warszawy
# d = date(2023, 5, 18)
# sunrise, sunset = get_sunrise_sunset(lat, lon, d)

# Definiuj ścieżkę do folderu z obrazami
images_folder_path1 = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI/0"
images_folder_path2 = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI/1"

# Używamy funkcji dla dwóch folderów
low_threshold = 0.1
high_threshold = 0.99
lat, lon = 52.2297, 21.0122  # współrzędne dla Warszawy

data = process_images_in_folder(images_folder_path1, low_threshold, high_threshold, lat, lon) + \
       process_images_in_folder(images_folder_path2, low_threshold, high_threshold, lat, lon )

#data=process_images_in_folder(images_folder_path2, low_threshold, high_threshold, lat, lon)

# Zapisujemy wyniki do pliku Excel

save_to_excel(data, 'darkimageHistogramSun2.xlsx')
