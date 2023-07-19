import requests
import json
import numpy as np

def query_triton_model(molded_images: np.ndarray, image_metas: np.ndarray, anchors: np.ndarray):
    # Konwertuj dane wejściowe do listy (format obsługiwany przez JSON)
    input_image_data = molded_images.tolist()
    input_image_meta_data = image_metas.tolist()
    input_anchors_data = anchors.tolist()

    # Tworzymy dane wejściowe
    data = {
        "inputs": [
            {"name": "input_image", "data": input_image_data, "datatype": "FP32", "shape": molded_images.shape},
            {"name": "input_image_meta", "data": input_image_meta_data, "datatype": "FP32", "shape": image_metas.shape},
            {"name": "input_anchors", "data": input_anchors_data, "datatype": "FP32", "shape": anchors.shape},
        ]
    }

    # Adres serwera Triton (zamień na prawdziwy adres serwera)
    #triton_server_url = "http://10.0.20.50:8050/v2/models/AppleMaskRCNNModel/infer"

    triton_server_url = "http://10.0.20.50:8050/v2/models/AppleMaskRCNNModel/versions/1/infer"

    # Wykonujemy zapytanie POST do serwera Triton
    response = requests.post(triton_server_url, data=json.dumps(data))

    # Pobieramy odpowiedź od serwera
    response_data = response.json()

    # Zwracamy dane wyjściowe
    ROI = response_data['outputs'][0]['data']
    mrcnn_bbox = response_data['outputs'][1]['data']
    mrcnn_class = response_data['outputs'][2]['data']
    mrcnn_detection = response_data['outputs'][3]['data']
    mrcnn_mask = response_data['outputs'][4]['data']
    rpn_bbox = response_data['outputs'][5]['data']
    rpn_class = response_data['outputs'][6]['data']

    return ROI, mrcnn_bbox, mrcnn_class, mrcnn_detection, mrcnn_mask, rpn_bbox, rpn_class
