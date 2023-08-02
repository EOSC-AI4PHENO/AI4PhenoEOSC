import mrcnn.modelJarek as modellib
from mrcnn.config import Config
import os
import skimage
import sys
import json
import time
import numpy as np
import tensorflow as tf
import random
import colorsys
from skimage.measure import find_contours
import matplotlib.pyplot as plt
from matplotlib import patches, lines
from matplotlib.patches import Polygon
from datetime import datetime
import shutil

#ROOT_DIR = os.path.abspath("../")
ROOT_DIR = os.path.abspath("")
sys.path.append(ROOT_DIR)

def results_to_json(results, filename, file_size):
    # Inicjalizuj strukturę pliku JSON
    json_file = {
        filename: {
            "fileref": "",
            "size": file_size,
            "filename": filename,
            "base64_img_data": "",
            "file_attributes": {},
            "regions": {},
        }
    }

    # Przejdź przez wszystkie regiony wyników
    for i in range(len(results['rois'])):
        # Wyodrębnij punkty (x,y) wielokąta z maski
        all_points_x, all_points_y = mask_to_polygon(results['masks'][:,:,i])

        # Dodaj region do pliku JSON
        json_file[filename]["regions"][str(i)] = {
            "shape_attributes": {
                "name": "polygon",
                "all_points_x": [int(x) for x in all_points_x],
                "all_points_y": [int(y) for y in all_points_y]
            },
            "region_attributes": {},
        }
    return json_file

def mask_to_polygon(mask):
    # Mask Polygon
    # Pad to ensure proper polygons for masks that touch image edges.
    padded_mask = np.zeros((mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
    padded_mask[1:-1, 1:-1] = mask
    contours = find_contours(padded_mask, 0.5)

    # Dla wielu obiektów w jednej masce, wybierz ten z największym polem
    largest_contour = max(contours, key=lambda x: x.shape[0])

    # Przekształć kontury do formatu (x,y)
    points_x, points_y = np.fliplr(largest_contour).T

    return points_x.tolist(), points_y.tolist()


def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

def load_image(fullnameImage):
    """Load the specified image and return a [H,W,3] Numpy array.
    """
    # Load image
    image = skimage.io.imread(fullnameImage)
    # If grayscale. Convert to RGB for consistency.
    if image.ndim != 3:
        image = skimage.color.gray2rgb(image)
    # If has an alpha channel, remove it for consistency
    if image.shape[-1] == 4:
        image = image[..., :3]
    return image


class LindenDeploymentConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "linden"

    GPU_COUNT = 1

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + balloon

    # Number of training steps
    EPOCHS = 500
    STEPS_PER_EPOCH = 61

    # Number of gt instances to use in batch
    MAX_GT_INSTANCES = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    # see REMARK in the description
    USE_MINI_MASK = False

    # TF2 feature - now you can run the model interactively
    RUN_EAGERLY = True
#####################################################################

config = LindenDeploymentConfig()

# create inference model
model = modellib.MaskRCNN(mode="inference", model_dir="/home", config=config)

fullname = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/dataset_2023_07_09_11_07_54/test/2022-06-25_07.12.34_class_1.jpg'

image = load_image(fullname)
dirname, filename = os.path.split(fullname)

# make prediction
results = model.detect([image], verbose=1)
r = results[0]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f#")  # Dodaj mikrosekundy do formatu czasu
output_path = os.path.join(ROOT_DIR, "Output")

os.makedirs(output_path, exist_ok=True)
basename1, extension1 = os.path.splitext(filename)
new_filenameimage = f"{timestamp}_{basename1}{extension1}"
fullnameCopyTo = os.path.join(output_path, new_filenameimage)
shutil.copy(fullname, fullnameCopyTo)

#display_instancesDeploment(timestamp, output_path, filename, image, r['rois'], r['masks'], r['class_ids'],
#                           'apple', r['scores'],
#                           title=f"Predictions_{filename}", figsize=(10, 10))

#########################################################
file_size = os.path.getsize(fullname)
basename, extension = os.path.splitext(filename)
new_filenameJSON = f"{timestamp}_{basename}.json"
fullnamejson = os.path.join(output_path, new_filenameJSON)

# Przekształć wyniki do formatu JSON
json_results = results_to_json(r, filename, file_size)

# Zapisz wyniki do pliku JSON
with open(fullnamejson, 'w') as json_file:
    json.dump(json_results, json_file, indent=4)

