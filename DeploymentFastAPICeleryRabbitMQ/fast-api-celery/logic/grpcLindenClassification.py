import numpy as np
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult
from PIL import Image


def infer(image: np.ndarray):
    # Ustawienia
    url = "10.0.20.50:8001"
    model_name = "ClassificationLinden"

    # Inicjalizacja klienta
    client = InferenceServerClient(url)

    image = np.expand_dims(image, axis=0)

    # Konwersja danych na InferInput
    infer_input = InferInput("vgg16_input", image.shape, "FP32")
    # konwersja danych na odpowiedni format
    image = image.astype(np.float32)
    infer_input.set_data_from_numpy(image)

    # określenie wyjścia
    output = InferRequestedOutput("dense_1")

    # Wykonanie inferencji
    results = client.infer(model_name, inputs=[infer_input], outputs=[output])

    # Zwrócenie wyników jako osobnych zmiennych
    dense_1 = results.as_numpy("dense_1")

    return dense_1


# fullname = "E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/LindenClassification/Linden_Photos_ROI/1/2022-06-19_03.48.34_class_1_ROI.jpg"
# image = np.array(Image.open(fullname))  # Wczytanie obrazka i przekształcenie go w np.ndarray
#
# # Wywołanie funkcji infer z przekazanym obrazkiem
# prediction = infer(image)
#
# predicted_labels = np.argmax(prediction)
#
# if predicted_labels == 1:
#     print(1)
# else:
#     print(0)
#
# print(f"Prediction: {prediction}")
# print(f"predicted_labels: {predicted_labels}")
