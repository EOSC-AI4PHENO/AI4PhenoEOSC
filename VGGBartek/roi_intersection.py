import json
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
from skimage import draw
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import cv2
from sympy import Point, Polygon, intersection
# from shapely.geometry import Polygon

def poly2mask(vertex_row_coords, vertex_col_coords, shape):
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask


json_file_zaznaczenie = 'E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\VGGBartek\iloczyn_ROI\via_project_30Jul2023_10h45m_json.json'
json_file_wykrywane_jablka = 'E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\VGGBartek\iloczyn_ROI\20220821_1302_0700F136_PIC_128_CAM_2.xml.pi.json'
image_file = 'obraz_wejscie.png'



img = Image.open(image_file)
width, height = img.size

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

print(data)
new_file = 'json_wyjscie.json'
with open(new_file, 'w') as f:
    json.dump(data, f)


img = np.array(img).astype(float)
print(mask_all.shape)
print(img.shape)
for i in range(3):
    tmp = img[:,:,i]
    tmp[mask_all]  = tmp[mask_all] + 100
    img[:,:,i] = tmp
img = np.minimum(np.maximum(img,0),255).astype(np.uint8)
img = Image.fromarray(img)

img.show()
plt.show()
#
# # https://stackoverflow.com/questions/67708224/shapely-polygon-to-binary-mask