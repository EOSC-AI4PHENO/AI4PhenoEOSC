from detectron2.utils.logger import setup_logger
setup_logger()
import numpy as np
import cv2
from detectron2.engine import DefaultPredictor
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import torch
from detectron2 import model_zoo
from detectron2.config import get_cfg
import copy
from detectron2.data.transforms import ResizeShortestEdge, AugInput

def cv2_imshow(im):
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    plt.figure(), plt.imshow(im), plt.axis('off')

def make_json_pred(file,masks):
    data = {'filename':file}
    regions_new=[]
    for maska in masks:
        # contours, _ = cv2.findContours(maska.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, _ = cv2.findContours(maska.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            contour = np.array(contour)
            contour = np.squeeze(contour)
            if contour.ndim == 2:
                wsp_x, wsp_y = contour[:, 0].tolist(), contour[:, 1].tolist()
                shape_attributes = {'name': 'polygon'}
                shape_attributes['all_points_x'] = wsp_x
                shape_attributes['all_points_y'] = wsp_y
                region_new = {'shape_attributes':shape_attributes}
                regions_new.append(region_new)
    data['regions'] = regions_new
    final_json = {f"{os.path.basename(file)}{os.path.getsize(file)}":data}
    return final_json




def odtworz_model(jitfile, image_file, nr_karty, path_to_results):
    os.environ["CUDA_VISIBLE_DEVICES"]=f"{nr_karty}"
    torch.cuda.set_device(nr_karty)

    file_prefix = os.path.splitext(os.path.basename(image_file))[0]
    if not os.path.isdir(path_to_results):
        os.makedirs(path_to_results)

    original_image = cv2.imread(image_file)


    # image = predictor.aug.get_transform(original_image).apply_image(original_image)
    image = copy.deepcopy(original_image)
    input_data = AugInput(image)
    resize = ResizeShortestEdge(800, 1333)#cfg.INPUT.MIN_SIZE_TEST, cfg.INPUT.MAX_SIZE_TEST
    transform = resize(input_data)
    image = transform.apply_image(image)

    image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))
    inputs = [image, torch.as_tensor([original_image.shape[0]]), torch.as_tensor([original_image.shape[1]])]

    traced_model = torch.jit.load(jitfile)
    with torch.no_grad():
        outputs= traced_model(*inputs)

    # pocz
    # for element in outputs:
    #     print(f"element.shape = {element.shape}, dtype(element) = {dtype(element)}")
    # # kon
    # exit()
    masks = np.asarray(outputs[2].cpu())
    output_json = make_json_pred(image_file,masks)
    with open(f"{path_to_results}/{file_prefix}_jit_pred_json_Jr_array.json", "w") as fp:
        json.dump(output_json, fp)

nr_karty = 0
image_file = '/home/kurekj/AI4PhenoEOSC/apple/Mask-RCNN-Apple-Detectron2/apple_dataset/apple/test/przybroda1_20230802_143628.jpg'
#image_file = '/home/swidersb/bswiderski/data/inne/001_20230818062050_[R][0@0][0].jpg'
# image_file = '/home/swidersb/bswiderski/data/inne/jakis_obraz2.jpeg'
# image_file = '/home/swidersb/bswiderski/data/inne/jakis_obraz3.jpg'

path_to_results = 'wyniki_tmp'
jitfile = 'model/model4_array.pt'

odtworz_model(jitfile, image_file, nr_karty, path_to_results)
