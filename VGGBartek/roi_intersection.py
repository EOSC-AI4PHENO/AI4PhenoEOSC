import json
# from io import BytesIO
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
from skimage import draw
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import cv2
import base64
import io
from skimage import draw
from sympy import Point, Polygon, intersection
from vgg_helper import is_json_structure_with_0_1_2_3,convert_json_to_structure_with_0_1_2_3

def poly2mask(vertex_row_coords, vertex_col_coords, shape):
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask


def filter_json_file(json_file_zaznaczenie_b64, json_file_wykrywane_jablka_b64, width, height):
    mask_all_roi = np.full((height, width), False)

    json_bytes = base64.b64decode(json_file_zaznaczenie_b64)

    with io.StringIO(json_bytes.decode('utf-8')) as json_file:
        data = json.load(json_file)
        photos = data.keys()
        for photo in photos:
            one_photo = data[photo]
            regions = one_photo['regions']
            for region in regions:
                shape_attributes = region['shape_attributes']
                x = shape_attributes['all_points_x']
                y = shape_attributes['all_points_y']
                polygon = np.stack((y, x), axis=1)
                mask = draw.polygon2mask((height, width), polygon)
                mask_all_roi = np.logical_or(mask_all_roi, mask)

    mask_all = np.full((height, width), False)

    json_bytes = base64.b64decode(json_file_wykrywane_jablka_b64)
    with io.StringIO(json_bytes.decode('utf-8')) as json_file:
        data = json.load(json_file)
        photos = data.keys()
        for photo in photos:
            one_photo = data[photo]
            regions = one_photo['regions']
            new_regions = []
            for region in regions.values():
                shape_attributes = region['shape_attributes']
                x = shape_attributes['all_points_x']
                y = shape_attributes['all_points_y']
                polygon = np.stack((y, x), axis=1)
                mask = draw.polygon2mask((height, width), polygon)
                mask = np.logical_and(mask_all_roi, mask)
                if np.sum(mask) > 0:
                    mask_all = np.logical_or(mask_all, mask)
                    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                    for contour in contours:
                        contour = np.array(contour)
                        contour = np.squeeze(contour)

                        x, y = contour[:, 0].tolist(), contour[:, 1].tolist()
                        new_region = region.copy()
                        new_shape_attributes = shape_attributes.copy()
                        new_shape_attributes['all_points_x'] = x
                        new_shape_attributes['all_points_y'] = y
                        new_region['shape_attributes'] = new_shape_attributes

                        new_regions.append(new_region)
                    one_photo['regions'] = new_regions

    # Konwertuj dane z powrotem na string JSON
    json_str = json.dumps(data, indent=4)

    # Koduj string JSON do base64
    output_base64 = base64.b64encode(json_str.encode('utf-8'))

    # Zwróć base64 string
    return output_base64.decode('utf-8')


def jsonfile_to_base64(jsonfilename: str) -> str:
    with open(jsonfilename, 'r', encoding='utf-8') as json_file:
        json_content = json_file.read()
    return base64.b64encode(json_content.encode('utf-8')).decode('utf-8')


def base64_to_jsonfile(jsoncontent_base64: str, outputfilename: str):
    json_content = base64.b64decode(jsoncontent_base64).decode('utf-8')
    with open(outputfilename, 'w', encoding='utf-8') as json_file:
        json_file.write(json_content)


json_areas_in_image = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/VGGBartek/via_project_28Jul2023_19h2m_json_converted.json'
json_apple_rois = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/VGGBartek/20220914_1207_0700F136_PIC_150_CAM_2.xml.pi.json'
imagefullname = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/VGGBartek/20220914_1207_0700F136_PIC_150_CAM_2.xml.pi.jpg'

json_areas_in_image_b64 = jsonfile_to_base64(json_areas_in_image)
json_apple_rois_b64 = jsonfile_to_base64(json_apple_rois)

img = Image.open(imagefullname)
width, height = img.size

result_base64 = filter_json_file(json_areas_in_image_b64, json_apple_rois_b64, width, height)
base64_to_jsonfile(result_base64, "outputfile.json")

###################################################################
# file = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/VGGBartek/rozne_struktury_VGG/struktura1_lista.json'
# file_b64 = jsonfile_to_base64(file)
# is_json_structure_with_0_1_2_3_Result = is_json_structure_with_0_1_2_3(file_b64)
# if not is_json_structure_with_0_1_2_3_Result:
#     file_b64 = convert_json_to_structure_with_0_1_2_3(file_b64)
# base64_to_jsonfile(file_b64,
#                    "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/VGGBartek/rozne_struktury_VGG/outputfile0123.json")
