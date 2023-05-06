import os
import pandas as pd


def find_jpg_files(root_folder):
    jpg_files = []

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                relative_path = root.replace(root_folder, "")

                tabb = relative_path.split("\\")

                data = tabb[0]
                code = tabb[1]
                jpg = tabb[2]
                hour = tabb[3]

                mins = file.split("[")
                min = mins[0]

                file_end = file.replace(min, "")

                jpg_files.append({
                    'Path': os.path.join(relative_path, file),
                    'Filename': file,
                    'data': data,
                    'code': code,
                    'jpg': jpg,
                    'hour': hour,
                    'min': min,
                    'file_end': file_end
                })

    return jpg_files


def save_to_excel(jpg_files, output_file):
    df = pd.DataFrame(jpg_files)
    df.to_excel(output_file, index=False, engine='openpyxl')


root_folder = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/EOSC-ai4pheno-Project-Photos/'
output_file = 'output.xlsx'

root_folder_to_Save='linden/Linden_Photos'

jpg_files = find_jpg_files(root_folder)
save_to_excel(jpg_files, output_file)


