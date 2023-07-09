import os
import sys
import time
import numpy as np
import tensorflow as tf

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")
sys.path.append(ROOT_DIR)

import linden
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

def poly2mask(vertex_row_coords, vertex_col_coords, shape):
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    mask = np.zeros(shape, dtype=np.bool_)
    mask[fill_row_coords, fill_col_coords] = True
    return mask
def get_regions(data, target_filename):
    # Przejdź przez każdy element w danych
    for key, value in data.items():
        if value["filename"] == target_filename:
            return value["regions"]  # Zwróć "regions" jeżeli "filename" pasuje

    # Zwróć None, jeżeli nie znaleziono pasującego "filename"
    return None


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
class LindenConfig(Config):
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
    EPOCHS = 20
    STEPS_PER_EPOCH = 61

    # Number of gt instances to use in batch
    MAX_GT_INSTANCES = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    # see REMARK in the description
    USE_MINI_MASK = False

    # TF2 feature - now you can run the model interactively
    RUN_EAGERLY = True


config = LindenConfig()

#######################################################################
# Load validation dataset
test_path = os.path.join(ROOT_DIR, "linden_dataset", "linden")
dataset = linden.LindenDataset()
dataset.load_linden(test_path, "test")

jsonfullname = os.path.join(test_path,"test", "via_region_data.json")

with open(jsonfullname, 'r') as file:
    jsondata = json.load(file)

# Must call before using the dataset
dataset.prepare()
print("Images: {}\nClasses: {}".format(len(dataset.image_ids), dataset.class_names))
######################################################################

weights_path = os.path.join(ROOT_DIR, "model_logs", "linden20230709T1128", "mask_rcnn_linden_0020.h5")

# create inference model
model = modellib.MaskRCNN(mode="inference", model_dir="/home", config=config)

print("Loading weights:", weights_path)
model.load_weights(weights_path, by_name=True)
model.keras_model.compile(run_eagerly=config.RUN_EAGERLY)
#################################################################################
# for image_id in dataset.image_ids:
# image_id = np.random.choice(dataset.image_ids)
# print(f"Processing image_id:{image_id}")

# image, image_meta, gt_class_id, gt_bbox, gt_masks =\
#    modellib.load_image_gt(dataset, config, image_id)
# info = dataset.image_info[image_id]

# results = model.detect([image], verbose=1)
# r = results[0]
# visualizeJarek.display_instances(image, r['rois'], r['masks'], r['class_ids'], dataset.class_names, r['scores'],
#                            title="Predictions", figsize=(7,7))

#################################################################################

# Compute mIOU for the test dataset
# miou = compute_miou(dataset, model)
# print("mIOU:", miou)

df_results = pd.DataFrame(columns=['file', 'mioumicro', 'miouweighted', 'f1', 'acc', 'tn', 'fp', 'fn', 'tp'])
# for each image in the dataset
for image_id in dataset.image_ids:
    print(f"Processing image_id:{image_id}")

    # load image
    image, image_meta, gt_class_id, gt_bbox, gt_masks = \
        modellib.load_image_gt(dataset, config, image_id)
    info = dataset.image_info[image_id]

    # make prediction
    results = model.detect([image], verbose=1)
    r = results[0]

    # Compute IoU overlaps [pred_masks, gt_masks]
    pred_masks = r['masks']
    overlaps = utils.calculate_iouJArek2(pred_masks, gt_masks)
    print(f'overlaps={overlaps}')

    # overlaps = utils.compute_overlaps_masks(pred_masks, gt_masks)
    # print(f'overlaps={overlaps}')

    # miou_score = compute_miou(pred_masks, gt_masks)
    # print(f'miou_score={miou_score}')

    # display and save results
    visualizeJarek.display_instances(info, image, r['rois'], r['masks'], r['class_ids'],
                                     dataset.class_names, r['scores'],
                                     title=f"Predictions_{image_id}", figsize=(7, 7))

    fullname = info['path']
    dirname, filename = os.path.split(fullname)
    print(f"filename_kod = {filename}")
    #poligony= data[filename_kod[0]]['regions']
    poligony = get_regions(jsondata,filename)
    img = image.copy().astype(np.float_)
    base_mask = np.full(image.shape[:-1], False)

    for region_key, region_value in poligony.items():
        # Dla każdego regionu, zapisz punkty x i y
        x = region_value["shape_attributes"]["all_points_x"]
        y = region_value["shape_attributes"]["all_points_y"]
        mask = poly2mask(vertex_row_coords=y, vertex_col_coords=x, shape=image.shape[:-1])
        base_mask = np.logical_or(base_mask, mask)

#    for polygon in poligony:
#        # print(polygon['shape_attributes'])
#        x = np.array(polygon['shape_attributes']['all_points_x'])
#        y = np.array(polygon['shape_attributes']['all_points_y'])
#        mask = poly2mask(vertex_row_coords=y, vertex_col_coords=x, shape=image.shape[:-1])
#        base_mask = np.logical_or(base_mask, mask)

    estimated_mask = np.full(image.shape[:-1], False)
    for i in range(r['masks'].shape[2]):
        estimated_mask = np.logical_or(estimated_mask, r['masks'][:,:,i])

    mioumicro = jaccard_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(), average='micro')
    miouweighted= jaccard_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(), average='weighted')
    f1 = f1_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(), pos_label=True)
    acc = accuracy_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten())
    tn, fp, fn, tp = confusion_matrix(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(),
                                      normalize='all').ravel()

    print(f'mioumicro={mioumicro}, miouweighted={miouweighted}')

    rekord = [filename, mioumicro, miouweighted, f1, acc, tn, fp, fn, tp]
    df_results.loc[df_results.shape[0]] = rekord

Statistics_fullname = os.path.join(dirname, "linden_Statistics_20_0.9.xlsx")
df_results.to_excel(Statistics_fullname, index=False)
