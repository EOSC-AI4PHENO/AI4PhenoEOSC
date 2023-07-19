import mrcnn.modelJarek as modellib
from mrcnn.config import Config
import os
import skimage

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


class AppleDeploymentConfig(Config):
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
    DETECTION_MIN_CONFIDENCE = 0.9

    # see REMARK in the description
    USE_MINI_MASK = False

    # TF2 feature - now you can run the model interactively
    RUN_EAGERLY = True
#####################################################################

config = AppleDeploymentConfig()

# create inference model
model = modellib.MaskRCNN(mode="inference", model_dir="/home", config=config)

fullname = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/apple/Mask-RCNN-Apple/apple_dataset/apple/test1/20220710_1204_0700F136_PIC_84_CAM_2.xml.pi.jpg'
image = load_image(fullname)
dirname, filename = os.path.split(fullname)

# make prediction
results = model.detect([image], verbose=1)