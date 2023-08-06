import os
import numpy as np
import tensorflow as tf
from PIL import Image
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
from sklearn.utils.class_weight import compute_sample_weight
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import time
import platform
from tensorflow.python.framework.config import set_memory_growth
from tqdm import tqdm
from tensorflow.keras.models import load_model

def load_images_from_folder(folder_path, resize_shape=None):
    image_files, loaded_images = [], []
    max_width, max_height = resize_shape if resize_shape else (0, 0)

    # Wczytanie nazw wszystkich obrazów z folderu
    for img_file in os.listdir(folder_path):
        if img_file.endswith('.jpg'):
            img_path = os.path.join(folder_path, img_file)
            img = Image.open(img_path)

            if resize_shape:
                img = img.resize(resize_shape)  # Dostosowanie rozmiaru
            else:
                width, height = img.size
                max_width = max(max_width, width)
                max_height = max(max_height, height)

            image_files.append(img_file)
            loaded_images.append(np.array(img))

    return np.array(loaded_images)

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

# Wczytanie modelu

#loaded_model = load_model('best_model_721.h5')
#loaded_model = tf.keras.models.load_model('ClassificationLindenModelv3')

# Określenie rozmiaru obrazów (na podstawie tego, co oczekuje model)
# Dostosuj to do Twojego modelu!

width = 321
height = 384

image_shape = (width,height)
#image_shape = None

# Wczytanie obrazów z folderu do przewidywań
images_to_predict = load_images_from_folder('Test/1', resize_shape=image_shape)

# Stworzenie listy do przechowywania przewidywanych etykiet
predicted_labels_list = []

# Przewidywanie przy użyciu wczytanego modelu
for image in images_to_predict:
    #image = np.expand_dims(image, axis=0)
    #predictions = loaded_model.predict(image)
    predictions = infer(image)
    predicted_label = np.argmax(predictions, axis=1)
    print(predictions)
    print(predicted_label)
    predicted_labels_list.append(predicted_label[0])

# Wypisanie wyników
# Obliczenie ilości predykcji dla klasy 0 i 1
count_class_0 = predicted_labels_list.count(0)
count_class_1 = predicted_labels_list.count(1)

# Obliczenie procentowego udziału dla klasy 0 i 1
total_predictions = len(predicted_labels_list)
percentage_class_0 = (count_class_0 / total_predictions) * 100
percentage_class_1 = (count_class_1 / total_predictions) * 100

# Wypisanie wyników
print(f"Klasa 0 została przewidziana {count_class_0} razy, co stanowi {percentage_class_0:.2f}% wszystkich predykcji.")
print(f"Klasa 1 została przewidziana {count_class_1} razy, co stanowi {percentage_class_1:.2f}% wszystkich predykcji.")

imageRGB = Image.open('/home/kurekj/AI4PhenoEOSC/linden/LindenClassification/2023-08-05/Test/1/2022-06-19_04.18.34_class_1_ROI.jpg')
imageRGB = imageRGB.resize(image_shape)
imageRGB = np.array(imageRGB)
#imageRGB = np.expand_dims(imageRGB, axis=0)
#predictions = loaded_model.predict(imageRGB)
predictions = infer(imageRGB)
predicted_label = np.argmax(predictions, axis=1)
print(predictions)
print(predicted_label)