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


def is_image_well_exposedByHisto(image_path, low_threshold, high_threshold, lat=None, lon=None, UTCdate=None,
                                 image_time=None):
    # Wczytaj obraz w skali szarości
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Oblicz histogram
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    ### to remove
    total_pixels = image.shape[0] * image.shape[1]
    dark_pixels = np.sum(hist[:80])  # Można dostosować próg
    bright_pixels = np.sum(hist[176:])  # Można dostosować próg

    dark_pixels_stats = dark_pixels / total_pixels
    bright_pixels_stats = bright_pixels / total_pixels

    # Jeśli podano współrzędne geograficzne oraz datę i czas obrazu
    if lat and lon and UTCdate and image_time:
        # Oblicz czas wschodu i zachodu słońca
        UTCsunrise, UTCsunset = get_sunrise_sunset(lat, lon, UTCdate)

        # Jeżeli czas zdjęcia jest po zachodzie słońca lub przed wschodem słońca
        if image_time > UTCsunset.time() or image_time < UTCsunrise.time():
            return False, 'Image is too dark due to being taken after sunset or before sunrise', dark_pixels_stats, bright_pixels_stats

    # Sprawdź, czy obraz jest za ciemny
    if dark_pixels_stats > low_threshold: #0.7
        return False, 'Image is too dark', dark_pixels_stats, bright_pixels_stats
    # Sprawdź, czy obraz jest za jasny
    elif bright_pixels_stats > high_threshold: #0.5
        return False, 'Image is too bright', dark_pixels_stats, bright_pixels_stats
    else:
        return True, 'Image is well exposed', dark_pixels_stats, bright_pixels_stats


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
            result, message, dark_pixels_stats, bright_pixels_stats = is_image_well_exposedByHisto(full_path, low_threshold, high_threshold,
                                                                            lat, lon, utc_date, utc_time)
            data.append(
                [full_path, filename, folder_path, extracted_date, extracted_time, utc_date, utc_time,
                 UTCsunrise.replace(tzinfo=None),
                 UTCsunset.replace(tzinfo=None), low_threshold,
                 high_threshold, lat,
                 lon,
                 result, message,
                 dark_pixels_stats,
                 bright_pixels_stats,
                 ])
    return data


def save_to_excel(data, output_file):
    df = pd.DataFrame(data,
                      columns=['fullname', 'filename', 'directory', 'date', 'time', 'utc_date', 'utc_time',
                               'UTCsunrise', 'UTCsunset',
                               'low_threshold', 'high_threshold', 'lat', 'lon', 'is_well_exposed', 'message',
                               'dark_pixels_stats',
                               'bright_pixels_stats',
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
low_threshold = 0.73
high_threshold = 0.5
lat, lon = 52.2297, 21.0122  # współrzędne dla Warszawy

data = process_images_in_folder(images_folder_path1, low_threshold, high_threshold, lat, lon) + \
       process_images_in_folder(images_folder_path2, low_threshold, high_threshold, lat, lon)

# data=process_images_in_folder(images_folder_path2, low_threshold, high_threshold, lat, lon)

# Zapisujemy wyniki do pliku Excel

save_to_excel(data, 'darkimageHistogramSun5.xlsx')
