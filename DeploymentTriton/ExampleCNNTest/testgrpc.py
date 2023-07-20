import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult
import matplotlib.pyplot as plt


def main():
    # ładowanie datasetu CIFAR10
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    img1 = x_test[0]

    plt.imshow(img1)
    plt.show()

    print(y_test[0])

    # normalizacja danych
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # wybór jednego obrazka
    img = x_test[0]

    # tworzenie obiektu klienta
    triton_client = InferenceServerClient(url="10.0.20.50:8001")

    # tworzenie wejścia dla modelu
    infer_input = InferInput("conv2d_input", [1, 32, 32, 3], "FP32")

    # konwersja danych na odpowiedni format
    img = img.astype(np.float32)
    infer_input.set_data_from_numpy(img.reshape(1, 32, 32, 3))

    # określenie wyjścia
    output = InferRequestedOutput("dense_1")

    # wykonanie inferencji
    result = triton_client.infer("ExampleCNNModelv1",
                                 model_version="1",
                                 inputs=[infer_input],
                                 outputs=[output])

    # wyświetlanie wyniku
    prediction = result.as_numpy('dense_1')
    predicted_labels = np.argmax(prediction)
    print(f"Prediction: {prediction}")
    print(f"predicted_labels: {predicted_labels}")



if __name__ == '__main__':
    main()
