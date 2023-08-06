import os
import numpy as np
import tensorflow as tf
from PIL import Image
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
from tensorflow.keras.models import load_model`

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

# ... [Twój wcześniejszy kod do uczenia modelu itp.] ...

# Wczytanie modelu

loaded_model = load_model('best_model.h5')

# Określenie rozmiaru obrazów (na podstawie tego, co oczekuje model)
# Dostosuj to do Twojego modelu!
image_shape = (100, 100)

# Wczytanie obrazów z folderu do przewidywań
images_to_predict = load_images_from_folder('Predict_Folder', resize_shape=image_shape)

# Przewidywanie przy użyciu wczytanego modelu
predictions = loaded_model.predict(images_to_predict)
predicted_labels = np.argmax(predictions, axis=1)

# Wypisanie wyników
print(predicted_labels)
