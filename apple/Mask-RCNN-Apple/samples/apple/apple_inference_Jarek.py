import os
import sys
import time
import numpy as np
import tensorflow as tf


def compute_iou(mask1, mask2):
    # Oblicza Intersection over Union (IoU) dla dwóch masek
    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)
    iou_score = np.sum(intersection) / np.sum(union)
    return iou_score

def compute_miou(pred_masks, gt_masks):
    # Oblicza mean Intersection over Union (mIoU) dla zestawu masek
    iou_scores = []
    for pred_mask, gt_mask in zip(pred_masks, gt_masks):
        iou_score = compute_iou(pred_mask, gt_mask)
        iou_scores.append(iou_score)
    miou_score = np.mean(iou_scores)
    return miou_score


# Root directory of the project
ROOT_DIR = os.path.abspath("../../")
sys.path.append(ROOT_DIR)

import apple
from mrcnn.config import Config
from mrcnn import utils
from mrcnn import visualizeJarek
from mrcnn.visualizeJarek import display_images
import mrcnn.model as modellib
from mrcnn.model import log

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
class InferenceConfig(Config):
    NAME = "balloon"
    NUM_CLASSES = 1 + 1  # Background + balloon
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    USE_MINI_MASK = False
    RUN_EAGERLY = False


config = InferenceConfig()
#######################################################################
# Load validation dataset
test_path = os.path.join(ROOT_DIR, "apple_dataset", "apple")
dataset = apple.AppleDataset()
dataset.load_apple(test_path, "test")

# Must call before using the dataset
dataset.prepare()
print("Images: {}\nClasses: {}".format(len(dataset.image_ids), dataset.class_names))
######################################################################
weights_path = os.path.join(ROOT_DIR, "model_logs", "apple20230705T1705", "mask_rcnn_apple_0020.h5")

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

    #overlaps = utils.compute_overlaps_masks(pred_masks, gt_masks)
    #print(f'overlaps={overlaps}')

    #miou_score = compute_miou(pred_masks, gt_masks)
    #print(f'miou_score={miou_score}')

    # display and save results
    visualizeJarek.display_instances(info, image, r['rois'], r['masks'], r['class_ids'],
                                     dataset.class_names, r['scores'],
                                     title=f"Predictions_{image_id}", figsize=(7, 7))
    # save the original image and the image with the mask applied
    # plt.imsave(f'original_image_{image_id}.png', image)
    # plt.imsave(f'masked_image_{image_id}.png', masked_image.astype(np.uint8))
