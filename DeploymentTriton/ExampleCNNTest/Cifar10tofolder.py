import os
import numpy as np
from tensorflow.keras.datasets import cifar10
from PIL import Image

# Ładujemy dane CIFAR10
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

# Wybieramy katalog do zapisania obrazów
output_dir = "cifar10_images"

# Tworzymy katalog, jeśli jeszcze nie istnieje
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Kombinujemy obrazy treningowe i testowe
all_images = np.concatenate((train_images, test_images))
all_labels = np.concatenate((train_labels, test_labels))

# Mapa etykiet do nazw klas, zgodnie z dokumentacją CIFAR10
label_names = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

# Przechodzimy przez wszystkie obrazy i zapisujemy je jako pliki
for i in range(len(all_images)):
    # Tworzymy nazwę obrazu z indeksem i nazwą klasy
    image_name = f"{i}_{label_names[all_labels[i][0]]}_{all_labels[i][0]}.png"

    print(image_name)

    # Tworzymy ścieżkę do zapisania obrazu
    image_path = os.path.join(output_dir, image_name)

    # Konwertujemy obraz z NumPy array na obiekt PIL Image i zapisujemy go
    img = Image.fromarray(all_images[i])
    img.save(image_path)
