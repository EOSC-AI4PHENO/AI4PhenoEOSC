import os
import sys
import numpy as np
from apple import AppleDataset
import multiprocessing
import tensorflow as tf

# define important dirs
ROOT_DIR = os.path.join(os.getcwd(), "..", "..")
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "model_logs")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# Path to trained weights mrcnn weights - for transfer learning
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "weights", "mask_rcnn_coco.h5")

# show visible GPU devices and limit the memory growth
print('List physical GPU devices:')
gpu_devices = tf.config.list_physical_devices('GPU')
for gpu in gpu_devices:
    print(' '*3, gpu)
    try:
        tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as error:
        print(error)
######################################################
class AppleConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "apple"

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
    #DETECTION_MIN_CONFIDENCE = 0.9
    DETECTION_MIN_CONFIDENCE = 0.5

    # see REMARK in the description
    USE_MINI_MASK = False

    # TF2 feature - now you can run the model interactively
    RUN_EAGERLY = False

config = AppleConfig()
# config.display()
##############################################################################
APPLE_DIR = os.path.join(ROOT_DIR, 'apple_dataset', 'apple')

train_ds = AppleDataset()
val_ds = AppleDataset()

# load data
train_ds.load_apple(APPLE_DIR, 'train')
val_ds.load_apple(APPLE_DIR, 'val')

# transform data into container structure - must have
train_ds.prepare()
val_ds.prepare()
config.VALIDATION_STEPS = len(val_ds.image_ids)

print("Image train count: {}".format(len(train_ds.image_ids)))
print("Class train count: {}".format(train_ds.num_classes))
for i, info in enumerate(train_ds.class_info):
    print("{:3}. {:50}".format(i, info['name']))

print("\nImage val count: {}".format(len(val_ds.image_ids)))
print("Class val count: {}".format(val_ds.num_classes))
for i, info in enumerate(val_ds.class_info):
    print("{:3}. {:50}".format(i, info['name']))

########################################################
# with tf.device('CPU:0'):
model = modellib.MaskRCNN(mode="training", config=config, model_dir=DEFAULT_LOGS_DIR)

# Exclude the last layers because they require a matching
# number of classes
model.load_weights(COCO_WEIGHTS_PATH, by_name=True,
                   exclude=["rpn_model",
                            "mrcnn_class_logits",
                            "mrcnn_bbox_fc",
                            "mrcnn_bbox",
                            "mrcnn_mask"])

##########################################################################
model.train(train_ds,
            val_ds,
            learning_rate=config.LEARNING_RATE,
            epochs=config.EPOCHS,
            layers='heads',
            max_queue_size=10,
            use_multiprocessing=False)