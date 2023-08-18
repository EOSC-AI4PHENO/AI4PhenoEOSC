import os
from os import walk
import shutil
import json
import PIL
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
import pickle
import math


def zwroc_maskeold(cx, cy, r, width, height):
    xv, yv = np.meshgrid(np.arange(width), np.arange(height), indexing='ij')
    r2 = np.power(r, 2)
    maska = (np.power(xv - cx, 2) + np.power(yv - cy, 2)) <= r2
    x, y = np.where(maska)
    points = np.stack([x, y], axis=1)

    if len(points) == 0:
        raise ValueError("Brak punktów w masce. Sprawdź wartości cx, cy, r, width oraz height.")

    hull = ConvexHull(points)
    x = points[hull.vertices, 0]
    y = points[hull.vertices, 1]
    return x, y


def convert_circle_to_polygonold(input_path, output_path):
    # Załadowanie pliku JSON
    with open(input_path) as f:
        data = json.load(f)

    output_data = {}

    j = 1
    ile = len(data.items())
    # Konwersja elipsy na wielokąt
    for filename, file_data in data.items():
        print(f'{j}/{ile} | {input_path} | {filename}')
        j = j + 1
        output_data[filename] = {
            "fileref": "",
            "size": file_data['size'],
            "filename": file_data['filename'],
            "base64_img_data": "",
            "file_attributes": file_data.get('file_attributes', {}),
            "regions": {}
        }

        for idx, region in enumerate(file_data['regions']):
            shape_attributes = region['shape_attributes']
            if shape_attributes['name'] != 'circle':
                continue

            cx = shape_attributes['cx']
            cy = shape_attributes['cy']
            r = shape_attributes['r']

            path, filenamejson = os.path.split(input_path)
            filenamejpg = file_data['filename']
            fullnamejpg = os.path.join(path, filenamejpg)
            img = Image.open(fullnamejpg)
            width, height = img.size

            all_points_x, all_points_y = zwroc_maske(cx, cy, r, width, height)

            all_points_x = list(all_points_x)
            all_points_y = list(all_points_y)

            all_points_x = np.array(all_points_x, np.int32)
            all_points_y = np.array(all_points_y, np.int32)

            all_points_x = all_points_x.tolist()
            all_points_y = all_points_y.tolist()

            output_data[filename]['regions'][str(idx)] = {
                "shape_attributes": {
                    "name": "polygon",
                    "all_points_x": all_points_x,
                    "all_points_y": all_points_y
                },
                "region_attributes": region.get('region_attributes', {})
            }

    # Zapisywanie wynikowego pliku JSON
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=4)
