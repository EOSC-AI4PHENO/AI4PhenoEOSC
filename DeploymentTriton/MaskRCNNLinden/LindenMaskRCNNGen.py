import os
import sys
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

# Root directory of the project
ROOT_DIR = os.path.abspath("")
sys.path.append(ROOT_DIR)

#import appleDeployment
from mrcnn.config import Config
from mrcnn import utils
from mrcnn import visualizeJarek
from mrcnn.visualizeJarek import display_images
import mrcnn.model as modellib
from mrcnn.model import log
import pandas as pd
from sklearn.metrics import jaccard_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import json
from skimage import draw
import skimage

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


def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors


def display_instancesDeploment(timestamp, output_path, filename, image, boxes, masks, class_ids, class_names,
                               scores=None, title="",
                               figsize=(12, 12), ax=None,
                               show_mask=True, show_bbox=True,
                               colors=None, captions=None):
    """
    boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
    masks: [height, width, num_instances]
    class_ids: [num_instances]
    class_names: list of class names of the dataset
    scores: (optional) confidence scores for each box
    title: (optional) Figure title
    show_mask, show_bbox: To show masks and bounding boxes or not
    figsize: (optional) the size of the image
    colors: (optional) An array or colors to use with each object
    captions: (optional) A list of strings to use as captions for each object
    """
    # Number of instances
    N = boxes.shape[0]
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    # If no axis is passed, create one and automatically call show()
    auto_show = False
    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)
        auto_show = True

    # Generate random colors
    colors = colors or random_colors(N)

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()
    for i in range(N):
        color = colors[i]

        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        y1, x1, y2, x2 = boxes[i]
        if show_bbox:
            p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
                                  alpha=0.7, linestyle="dashed",
                                  edgecolor=color, facecolor='none')
            ax.add_patch(p)

        # Label
        if not captions:
            class_id = class_ids[i]
            score = scores[i] if scores is not None else None
            label = class_names[class_id]
            # caption = "{} {:.3f}".format(label, score) if score else label
            caption = "{:.3f}".format(score) if score else label
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption,
                color='w', size=11, backgroundcolor="none")

        # Mask
        mask = masks[:, :, i]
        if show_mask:
            masked_image = apply_mask(masked_image, mask, color)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            ax.add_patch(p)
    ax.imshow(masked_image.astype(np.uint8))
    # if auto_show:
    # plt.show()

    fullname = os.path.join(output_path,filename)

    new_filename = f"{timestamp}_{filename}"  # Utwórz nową nazwę pliku z dodanym znacznikiem czasu

    basename, extension = os.path.splitext(new_filename)
    Original_basename = basename + "_Original"
    Original_fullname = os.path.join(output_path, Original_basename + extension)

    Predicted_basename = basename + "_Predicted"
    Predicted_fullname = os.path.join(output_path, Predicted_basename + extension)

    Predicted_basenameFig = basename + "_PredictedFIG"
    Predicted_fullnameFig = os.path.join(output_path, Predicted_basenameFig + '.png')

    plt.imsave(fullname, image)
    plt.imsave(Original_fullname, image)
    plt.imsave(Predicted_fullname, masked_image.astype(np.uint8))
    plt.savefig(Predicted_fullnameFig, dpi=300)


# show visible GPU devices and limit the memory growth
print('List physical GPU devices:')
gpu_devices = tf.config.list_physical_devices('GPU')
for gpu in gpu_devices:
    print(' ' * 3, gpu)
    try:
        tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as error:
        print(error)


#####################################################################
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

weights_path = os.path.join(ROOT_DIR, "model_logsDeployment", "linden20230709T1128",
                            "mask_rcnn_linden_0020.h5")

# create inference model
model = modellib.MaskRCNN(mode="inference", model_dir="/home", config=config)

print("Loading weights:", weights_path)
model.load_weights(weights_path, by_name=True)
model.keras_model.compile(run_eagerly=config.RUN_EAGERLY)

model.keras_model.save('LindenMaskRCNNModelv1', save_format='tf')  # gdzie model_path to ścieżka, do której chcesz zapisać model
