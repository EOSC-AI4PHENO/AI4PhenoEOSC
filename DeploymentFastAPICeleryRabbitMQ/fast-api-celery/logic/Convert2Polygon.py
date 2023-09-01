import json
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
import base64
import io


def circle2polygon(cx, cy, r, width, height):
    xv, yv = np.meshgrid(np.arange(width), np.arange(height), indexing='ij')
    r2 = np.power(r, 2)
    maska = (np.power(xv - cx, 2) + np.power(yv - cy, 2)) <= r2
    x, y = np.where(maska)
    points = np.stack([x, y], axis=1)
    hull = ConvexHull(points)
    x = points[hull.vertices, 0]
    y = points[hull.vertices, 1]
    return x.tolist(), y.tolist()


def ellipse2polygon(cx, cy, rx, ry, theta, width, height):
    xv, yv = np.meshgrid(np.arange(width), np.arange(height), indexing='ij')
    maska = np.power((np.cos(theta) * (xv - cx) + np.sin(theta) * (yv - cy)) / rx, 2) + np.power(
        (-np.sin(theta) * (xv - cx) + np.cos(theta) * (yv - cy)) / ry, 2) <= 1
    x, y = np.where(maska)
    points = np.stack([x, y], axis=1)
    hull = ConvexHull(points)
    x = points[hull.vertices, 0]
    y = points[hull.vertices, 1]
    return x.tolist(), y.tolist()


def rect2polygon(x, y, rwidth, rheight, width, height):
    x = [x, x, x + rwidth - 1, x + rwidth - 1]
    y = [y, y + rheight - 1, y + rheight - 1, y]
    x = np.maximum(np.minimum(np.array(x), width), 1).tolist()
    y = np.maximum(np.minimum(np.array(y), height), 1).tolist()
    return [x, y]

def Convert2Polygon1(jsonfile_base64: str, width: int, height: int):
    json_bytes = base64.b64decode(jsonfile_base64)
    json_file = io.StringIO(json_bytes.decode('utf-8'))
    data = json.load(json_file)
    photos = data.keys()
    for photo in photos:
        one_photo = data[photo]
        regions = one_photo['regions']
        new_regions = {}  # utworzenie nowego słownika
        for i, region in enumerate(regions):
            shape_attributes = region['shape_attributes']
            name = shape_attributes['name']
            if name in ['circle', 'ellipse', 'rect']:
                if name == 'circle':
                    x, y = circle2polygon(cx=shape_attributes['cx'],
                                          cy=shape_attributes['cy'],
                                          r=shape_attributes['r'],
                                          width=width, height=height)
                elif name == 'ellipse':
                    x, y = ellipse2polygon(
                        cx=shape_attributes['cx'],
                        cy=shape_attributes['cy'],
                        rx=shape_attributes['rx'],
                        ry=shape_attributes['ry'],
                        theta=shape_attributes['theta'],
                        width=width, height=height)

                elif name == 'rect':
                    x, y = rect2polygon(x=shape_attributes['x'],
                                        y=shape_attributes['y'],
                                        rwidth=shape_attributes['width'],
                                        rheight=shape_attributes['height'],
                                        width=width, height=height)

                region['shape_attributes'] = {'name': 'polygon', 'all_points_x': x,
                                              'all_points_y': y}
            new_regions[str(i)] = region  # dodajemy region do nowego słownika
        one_photo['regions'] = new_regions  # zastępujemy starą listę nowym słownikiem
    json_out = json.dumps(data)
    return base64.b64encode(json_out.encode('utf-8')).decode('utf-8')


def Convert2Polygon2(jsonfile_base64: str, width: int, height: int):
    json_bytes = base64.b64decode(jsonfile_base64)
    json_file = io.StringIO(json_bytes.decode('utf-8'))
    data = json.load(json_file)
    photos = data.keys()

    for photo in photos:
        one_photo = data[photo]
        regions = one_photo.get('regions', [])

        new_regions = {}  # utworzenie nowego słownika dla wynikowego JSON-a

        if isinstance(regions, dict):  # Obsługa formatu jsonSlownik
            for i, region in regions.items():
                new_regions[str(i)] = update_shape(region, width, height)

        elif isinstance(regions, list):  # Obsługa formatu JsonLista
            for i, region in enumerate(regions):
                new_regions[str(i)] = update_shape(region, width, height)

        one_photo['regions'] = new_regions  # zastępujemy starą strukturę nowym słownikiem

    json_out = json.dumps(data)
    return base64.b64encode(json_out.encode('utf-8')).decode('utf-8')

def update_shape(region, width, height):
    shape_attributes = region['shape_attributes']
    name = shape_attributes['name']

    if name in ['circle', 'ellipse', 'rect']:
        if name == 'circle':
            x, y = circle2polygon(cx=shape_attributes['cx'],
                                  cy=shape_attributes['cy'],
                                  r=shape_attributes['r'],
                                  width=width, height=height)

        elif name == 'ellipse':
            x, y = ellipse2polygon(
                cx=shape_attributes['cx'],
                cy=shape_attributes['cy'],
                rx=shape_attributes['rx'],
                ry=shape_attributes['ry'],
                theta=shape_attributes['theta'],
                width=width, height=height)

        elif name == 'rect':
            x, y = rect2polygon(x=shape_attributes['x'],
                                y=shape_attributes['y'],
                                rwidth=shape_attributes['width'],
                                rheight=shape_attributes['height'],
                                width=width, height=height)

        region['shape_attributes'] = {'name': 'polygon', 'all_points_x': x, 'all_points_y': y}

    return region

def jsonfile_to_base64(jsonfilename: str) -> str:
    with open(jsonfilename, 'r', encoding='utf-8') as json_file:
        json_content = json_file.read()
    return base64.b64encode(json_content.encode('utf-8')).decode('utf-8')


def base64_to_jsonfile(jsoncontent_base64: str, outputfilename: str):
    json_content = base64.b64decode(jsoncontent_base64).decode('utf-8')
    with open(outputfilename, 'w', encoding='utf-8') as json_file:
        json_file.write(json_content)


# filename = '20220914_1207_0700F136_PIC_150_CAM_2.xml.pi.jpg'
# img = Image.open(filename)
# width, height = img.size
#
# # filenamejson = 'via_project_28Jul2023_19h2m_json.json'
# # filenamejsonout = 'via_project_28Jul2023_19h2m_json_converted.json'
#
# filenamejson = 'jarektest.json'
# filenamejsonout = 'jarektestout.json'
#
# jsonfile_base64_input = jsonfile_to_base64(filenamejson)
#
# # is_json_structure_with_0_1_2_3_Result = is_json_structure_with_0_1_2_3(jsonfile_base64_input)
# # if not is_json_structure_with_0_1_2_3_Result:
# #     file_b64 = convert_json_to_structure_with_0_1_2_3(jsonfile_base64_input)
#
# jsonfile_base64_output = Convert2Polygon(jsonfile_base64_input, width=width, height=height)
# base64_to_jsonfile(jsonfile_base64_output, filenamejsonout)
