import numpy as np
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult

def infer(image: np.ndarray, image_meta: np.ndarray, anchors: np.ndarray):
    # Ustawienia
    url = "10.0.20.50:8001"
    #model_name = "AppleMaskRCNNModel"
    model_name = "AppleMaskRCNNModelv3"

    # Inicjalizacja klienta
    client = InferenceServerClient(url)

    # Konwersja danych na InferInput
    inputs = []
    input_image = InferInput("input_image", image.shape, "FP32")
    input_image.set_data_from_numpy(image.astype(np.float32))
    inputs.append(input_image)

    input_anchors = InferInput("input_anchors", anchors.shape, "FP32")
    input_anchors.set_data_from_numpy(anchors.astype(np.float32))
    inputs.append(input_anchors)

    input_image_meta = InferInput("input_image_meta", image_meta.shape, "FP32")
    input_image_meta.set_data_from_numpy(image_meta.astype(np.float32))
    inputs.append(input_image_meta)

    # Zdefiniowanie danych wyjściowych
    outputs = []
    output_names = ["ROI", "mrcnn_bbox", "mrcnn_class", "mrcnn_detection", "mrcnn_mask", "rpn_bbox", "rpn_class"]
    for name in output_names:
        outputs.append(InferRequestedOutput(name))

    # Wykonanie inferencji
    results = client.infer(model_name, inputs, outputs=outputs)

    # Zwrócenie wyników jako osobnych zmiennych
    ROI = results.as_numpy("ROI")
    mrcnn_bbox = results.as_numpy("mrcnn_bbox")
    mrcnn_class = results.as_numpy("mrcnn_class")
    mrcnn_detection = results.as_numpy("mrcnn_detection")
    mrcnn_mask = results.as_numpy("mrcnn_mask")
    rpn_bbox = results.as_numpy("rpn_bbox")
    rpn_class = results.as_numpy("rpn_class")

    return ROI, mrcnn_bbox, mrcnn_class, mrcnn_detection, mrcnn_mask, rpn_bbox, rpn_class
