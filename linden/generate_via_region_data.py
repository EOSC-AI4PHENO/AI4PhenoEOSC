import os
import glob
import json

# ścieżka do folderu
folder_path = 'Linden_Photos_Flowering_WellExposed'

# szablon danych dla pliku json
template = {
    "filename": "",
    "size": 0,
    "regions": [
        {
            "shape_attributes": {
                "name": "polygon",
                "all_points_x": [
                    158, 216, 229, 266, 298, 317, 309, 318, 318, 283, 265, 268, 238,
                    198, 167, 136, 89, 58, 29, 47, 43, 49, 35, 18, 16, 33, 56, 65,
                    77, 107, 127, 139, 127, 127
                ],
                "all_points_y": [
                    325, 383, 414, 410, 436, 480, 521, 551, 578, 597, 623, 669, 685,
                    685, 664, 646, 659, 690, 681, 658, 622, 583, 550, 548, 512, 498,
                    489, 453, 420, 405, 400, 383, 352, 334
                ]
            },
            "region_attributes": {}
        }
    ],
    "file_attributes": {}
}

# utworzenie słownika, który będzie zawierać wszystkie dane
output_dict = {}

# przejście przez wszystkie pliki jpg w folderze
for file_num, filename in enumerate(glob.glob(os.path.join(folder_path, '*.jpg')), 1):
    # wyznaczenie rozmiaru pliku
    size = os.path.getsize(filename)

    # skopiowanie szablonu
    data = template.copy()

    # podmiana nazwy pliku i rozmiaru pliku
    data['filename'] = os.path.basename(filename)
    data['size'] = size

    # dodanie danych do słownika wyjściowego
    output_dict[os.path.basename(filename) + str(size)] = data

fullnameJsonOutput = os.path.join(folder_path, 'via_region_data.json')
# zapis danych do pliku json
with open(fullnameJsonOutput, 'w') as f:
    json.dump(output_dict, f)
