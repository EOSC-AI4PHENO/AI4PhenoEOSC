import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
import requests
import json
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

    # konwersja danych na odpowiedni format
    img = img.astype(np.float32).tolist()

    # URL do serwera Triton
    triton_url = "http://10.0.20.50:8000/v2/models/ExampleCNNModelv1/versions/1/infer"

    # dane wejściowe do inferencji
    infer_input = {
        "inputs": [
            {
                "name": "conv2d_input",
                "shape": [1, 32, 32, 3],
                "datatype": "FP32",
                "data": img
            }
        ],
        "outputs": [
            {
                "name": "dense_1"
            }
        ]
    }

    # wykonanie inferencji
    response = requests.post(triton_url, data=json.dumps(infer_input))
    result = response.json()

    print(result)

    # wyświetlanie wyniku
    prediction = np.array(result['outputs'][0]['data'])
    predicted_labels = np.argmax(prediction)
    print(f"Prediction: {prediction}")
    print(f"predicted_labels: {predicted_labels}")


if __name__ == '__main__':
    main()
