from detectron2.utils.logger import setup_logger
setup_logger()
import numpy as np
import cv2
from detectron2.engine import DefaultPredictor
import matplotlib.pyplot as plt
import pandas as pd
import os
import random
import torch
from torch import nn
from detectron2 import model_zoo
from detectron2.export.flatten import TracingAdapter
from detectron2.config import get_cfg
from detectron2.data.transforms import ResizeShortestEdge, AugInput
from detectron2.utils.testing import get_sample_coco_image
from detectron2.data.transforms import ResizeShortestEdge, AugInput
import copy


def odtworz_model(model_path, nr_karty, jitfile):
    os.environ["CUDA_VISIBLE_DEVICES"]=f"{nr_karty}"
    torch.cuda.set_device(nr_karty)

    df = pd.read_csv(f"{model_path}/df_results_podsumowanie.csv")
    SOLVER_MAX_ITER = np.uint32(df.loc[0,'SOLVER.MAX_ITER']).item()
    wagi_coco = df.loc[0,'wagi_coco']
    BATCH_SIZE_PER_IMAGE = np.uint32(df.loc[0,'SOLVER.IMS_PER_BATCH']).item()
    print(df.loc[0])

    cfg = get_cfg()
    cfg.MODEL.DEVICE = f'cuda:{nr_karty}'
    cfg.merge_from_file(model_zoo.get_config_file(wagi_coco))
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(wagi_coco)  # Let training initialize from model zoo
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
    cfg.SOLVER.MAX_ITER = SOLVER_MAX_ITER    # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
    cfg.SOLVER.STEPS = []        # do not decay learning rate
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = BATCH_SIZE_PER_IMAGE   # faster, and good enough for this toy dataset (default: 512)
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
    cfg.MODEL.WEIGHTS = os.path.join(model_path, "model_final.pth")  # path to the model we just trained
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # set a custom testing threshold

    predictor = DefaultPredictor(cfg)

    model = predictor.model
    model.eval()


    def inference_func(model, image_info):
        image = image_info[0]
        oryginal_height = image_info[1]
        oryginal_width = image_info[2]
        inputs = [{"image": image, "height": oryginal_height, "width": oryginal_width}]
        return model.inference(inputs, do_postprocess=True)#[0]["instances"]


    original_image = get_sample_coco_image().numpy().transpose(1, 2, 0)

    image = copy.deepcopy(original_image)
    input_data = AugInput(image)
    resize = ResizeShortestEdge(cfg.INPUT.MIN_SIZE_TEST, cfg.INPUT.MAX_SIZE_TEST)
    transform = resize(input_data)
    image = transform.apply_image(image)


    image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))
    inputs = [image, torch.as_tensor(original_image.shape[0]), torch.as_tensor(original_image.shape[1])]

    wrapper = TracingAdapter(model, inputs, inference_func)
    wrapper.eval()
    with torch.no_grad():
        # trace with smaller images, and the trace must still work
        image_interpolated = nn.functional.interpolate(image, scale_factor=random.uniform(0.5, 0.7))
        trace_inputs_info = [image_interpolated, torch.as_tensor(image_interpolated.size(1)), torch.as_tensor(image_interpolated.size(2))]
        traced_model = torch.jit.trace(wrapper, trace_inputs_info)

    torch.jit.save(traced_model, jitfile)


nr_karty = 0
# model_path = '/home/swidersb/bswiderski/detectron2_v5/detectron2/wyniki_automat/wyniki60'
model_path = '/home/swidersb/bswiderski/detectron2_v5/detectron2/wyniki_automat2/wyniki2'

# jitfile = '/home/swidersb/model_zapisany/model3.jit'
jitfile = '/home/swidersb/model_zapisany/model4.jit'
odtworz_model(model_path, nr_karty, jitfile)
