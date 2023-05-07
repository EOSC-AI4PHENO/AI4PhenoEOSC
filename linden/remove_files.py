import os
from datetime import time

def extract_time_from_filename(filename):
    time_str = filename.split("_")[1]
    hour, minute, second = map(int, time_str.split("."))
    return time(hour, minute, second)

def should_delete_file(filename):
    file_time = extract_time_from_filename(filename)
    time_start = time(18, 0)
    time_end = time(6, 0)
    return (file_time >= time_start) or (file_time < time_end)

def delete_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") and should_delete_file(filename):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Usunięto plik: {file_path}")

dir='E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI_20.00_and_06.00/0'
delete_files(dir)