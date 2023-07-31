import json
from PIL import Image
from skimage import draw
import numpy as np
import matplotlib.pyplot as plt
import cv2

json_file_zaznaczenie = 'zaznaczenie_ROI_ogolnego.json'
json_file_wykrywane_jablka = 'zaznaczenie_jablek.json'
image_file = 'obraz_wejscie.png'


def make_jsons_intersections(image_file,json_file_zaznaczenie,json_file_wykrywane_jablka):
    img = cv2.imread(image_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape

    mask_all_roi = np.full((height, width), False)
    with open(json_file_zaznaczenie) as json_file:
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
                mask = draw.polygon2mask((height,width), polygon)
                mask_all_roi = np.logical_or(mask_all_roi, mask)

    mask_all = np.full((height, width), False)
    with open(json_file_wykrywane_jablka) as json_file:
        data = json.load(json_file)
        photos = data.keys()
        for photo in photos:
            one_photo = data[photo]
            regions = one_photo['regions']
            new_regions = []
            for region in regions:
                shape_attributes = region['shape_attributes']
                x = shape_attributes['all_points_x']
                y = shape_attributes['all_points_y']

                polygon = np.stack((y, x), axis=1)
                mask = draw.polygon2mask((height, width), polygon)
                mask = np.logical_and(mask_all_roi,mask)
                if np.sum(mask)>0:
                    mask_all = np.logical_or(mask_all, mask)
                    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                    for contour in contours:
                        contour = np.array(contour)
                        contour = np.squeeze(contour)

                        x, y = contour[:,0].tolist(), contour[:,1].tolist()
                        new_region = region.copy()
                        new_shape_attributes = shape_attributes.copy()
                        new_shape_attributes['all_points_x'] = x
                        new_shape_attributes['all_points_y'] = y
                        new_region['shape_attributes']=new_shape_attributes

                        new_regions.append(new_region)
                    one_photo['regions']=new_regions
    return data

data = make_jsons_intersections(image_file,json_file_zaznaczenie,json_file_wykrywane_jablka)

new_file = 'json_wyjscie_f.json'
with open(new_file, 'w') as f:
    json.dump(data, f)

