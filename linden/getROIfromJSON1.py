import json
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw

def read_json(nazwa_pliku):
    with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
        dane = json.load(plik)
    return dane

data = read_json('ODUPP_2022.06.28.05.54.35._json.json')

# Wczytaj obrazek i informacje o ROI
image_data = data['ODUPP_2022.06.28.05.54.35.jpg669073']
filename = image_data['filename']
regions = image_data['regions']
shape_attributes = regions[0]['shape_attributes']
all_points_x = shape_attributes['all_points_x']
all_points_y = shape_attributes['all_points_y']

# Wczytaj obraz
#image = Image.open(filename)

# Stwórz maskę dla ROI
#mask = Image.new('L', image.size, 0)
#mask_draw = ImageDraw.Draw(mask)
#polygon = list(zip(all_points_x, all_points_y))
#mask_draw.polygon(polygon, fill=255)

# Wycięcie ROI z obrazu
#image_roi = Image.composite(image, Image.new('RGBA', image.size), mask)
#rgb_im = image_roi.convert('RGB')

# Zapisz ROI do pliku JPG
#output_filename = os.path.splitext(filename)[0] + '_ROI.jpg'
#rgb_im.save(output_filename)

image = cv2.imread(filename)

# Stwórz maskę dla ROI
mask = np.zeros(image.shape[:2], dtype=np.uint8)
polygon = np.array(list(zip(all_points_x, all_points_y)), dtype=np.int32)
cv2.fillPoly(mask, [polygon], 255)

# Wycięcie ROI z obrazu
image_roi = cv2.bitwise_and(image, image, mask=mask)

# Zapisz ROI do pliku JPG
output_filename = os.path.splitext(filename)[0] + '_ROI_mask.jpg'
cv2.imwrite(output_filename, image_roi)

###################################################
# Oblicz prostokąt otaczający wielokąt
polygon = np.array(list(zip(all_points_x, all_points_y)), dtype=np.int32)
x_min, y_min = np.min(polygon, axis=0)
x_max, y_max = np.max(polygon, axis=0)

# Przycinanie (crop) ROI
image_roi = image[y_min:y_max, x_min:x_max]

# Zapisz ROI do pliku JPG
output_filename = os.path.splitext(filename)[0] + '_ROI_cropped.jpg'
cv2.imwrite(output_filename, image_roi)