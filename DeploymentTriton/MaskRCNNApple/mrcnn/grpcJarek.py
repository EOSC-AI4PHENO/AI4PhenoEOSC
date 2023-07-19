import grpc
import numpy as np
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
def get_GRPC_prediction(molded_images, image_metas, anchors):
    channel = grpc.insecure_channel('10.0.20.50:8051')  # Podmień na właściwy adres serwera
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'AppleMaskRCNNModel'
    request.model_spec.signature_name = 'serving_default'  # Podmień na właściwą nazwę sygnatury, jeśli to konieczne

    # Przekształć dane wejściowe w odpowiedni format
    request.inputs['input_image'].CopyFrom(
        tf.make_tensor_proto(molded_images, shape=molded_images.shape))
    request.inputs['input_anchors'].CopyFrom(
        tf.make_tensor_proto(anchors, shape=anchors.shape))
    request.inputs['input_image_meta'].CopyFrom(
        tf.make_tensor_proto(image_metas, shape=image_metas.shape))

    response = stub.Predict(request, 10.0)  # 10 sekundowy limit czasu

    # Zwróć odpowiednie dane wyjściowe
    ROI = np.array(response.outputs['ROI'].float_val)
    mrcnn_bbox = np.array(response.outputs['mrcnn_bbox'].float_val)
    mrcnn_class = np.array(response.outputs['mrcnn_class'].float_val)
    mrcnn_detection = np.array(response.outputs['mrcnn_detection'].float_val)
    mrcnn_mask = np.array(response.outputs['mrcnn_mask'].float_val)
    rpn_bbox = np.array(response.outputs['rpn_bbox'].float_val)
    rpn_class = np.array(response.outputs['rpn_class'].float_val)

    return ROI, mrcnn_bbox, mrcnn_class, mrcnn_detection, mrcnn_mask, rpn_bbox, rpn_class
