from grpc import insecure_channel
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import numpy as np
import tensorflow as tf

def request_server(input_image, input_anchors, input_image_meta):
    # Ustalamy kanał i klienta do komunikacji z serwerem Triton
    channel = insecure_channel('10.0.20.50:8001')
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    # Tworzymy żądanie do modelu
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'AppleMaskRCNNModel'
    request.model_spec.signature_name = 'serving_default'

    # Dodajemy dane wejściowe do żądania
    request.inputs['input_image'].CopyFrom(tf.make_tensor_proto(input_image, shape=input_image.shape))
    request.inputs['input_anchors'].CopyFrom(tf.make_tensor_proto(input_anchors, shape=input_anchors.shape))
    request.inputs['input_image_meta'].CopyFrom(tf.make_tensor_proto(input_image_meta, shape=input_image_meta.shape))

    # Wykonujemy żądanie
    response = stub.Predict(request, timeout=30.0)

    # Zwracamy odpowiedź
    return response.outputs

# Przykładowe dane wejściowe
input_image = np.random.rand(1, 800, 800, 3).astype(np.float32)
input_anchors = np.random.rand(1, 261888, 4).astype(np.float32)
input_image_meta = np.random.rand(1, 14).astype(np.float32)

# Odpytanie serwera
response = request_server(input_image, input_anchors, input_image_meta)

# Wypisanie odpowiedzi
print(response)
