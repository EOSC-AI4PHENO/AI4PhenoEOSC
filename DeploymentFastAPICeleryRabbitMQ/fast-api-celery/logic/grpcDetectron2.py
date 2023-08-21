import numpy as np
import cv2
# from detectron2.engine import DefaultPredictor
#import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import torch
from detectron2 import model_zoo
from detectron2.config import get_cfg
import copy
from detectron2.data.transforms import ResizeShortestEdge, AugInput
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

def ConvertJsonDict2ListJarek(json_file: str):
    data = json.loads(json_file)
    photos = data.keys()
    for photo in photos:
        one_photo = data[photo]
        regions = one_photo['regions']
        new_regions = {}  # utworzenie nowego słownika
        for i, region in enumerate(regions):
            shape_attributes = region['shape_attributes']
            name = shape_attributes['name']
            new_regions[str(i)] = region  # dodajemy region do nowego słownika
        one_photo['regions'] = new_regions  # zastępujemy starą listę nowym słownikiem
    json_out = json.dumps(data)
    return json_out
def make_json_pred(filename, image_size, masks):
    data = {'filename':filename}
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
    final_json = {f"{filename}{image_size}":data}
    return final_json

def inferDetectron2(original_image: np.ndarray, filename: str, image_size: int):
    #file_prefix = os.path.splitext(os.path.basename(image_file))[0]

    # image = predictor.aug.get_transform(original_image).apply_image(original_image)
    image = copy.deepcopy(original_image)
    input_data = AugInput(image)
    resize = ResizeShortestEdge(800, 1333)#cfg.INPUT.MIN_SIZE_TEST, cfg.INPUT.MAX_SIZE_TEST
    transform = resize(input_data)
    image = transform.apply_image(image)

    image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))

    url = "10.0.20.50:8001"
    model_name = "MaskRCNNAppleBartekModel"
    client = InferenceServerClient(url)

    # Inputs
    input_image = InferInput("image", [3, *image.shape[1:3]], "FP32")
    input_image.set_data_from_numpy(image.numpy().astype(np.float32))

    input_height = InferInput("height", [1], "FP32")
    input_height.set_data_from_numpy(np.array(original_image.shape[0])[np.newaxis].astype(np.float32))

    input_width = InferInput("width", [1], "FP32")
    input_width.set_data_from_numpy(np.array(original_image.shape[1])[np.newaxis].astype(np.float32))

    inputs = [input_image, input_height, input_width]
    # Outputs
    output_names = ["output0", "output1", "output2", "output3", "output4"]
    outputs = [InferRequestedOutput(name) for name in output_names]

    results = client.infer(model_name, inputs, outputs=outputs)

    output0 = results.as_numpy("output0")
    output1 = results.as_numpy("output1")
    output2 = results.as_numpy("output2")
    output3 = results.as_numpy("output3")
    output4 = results.as_numpy("output5")
    masks = output2
    output_json = make_json_pred(filename, image_size, masks)
    json_str = json.dumps(output_json)
    json_str=ConvertJsonDict2ListJarek(json_str)
    return json_str
