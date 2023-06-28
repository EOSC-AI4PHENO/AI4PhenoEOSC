import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam

# Ścieżki do katalogów z danymi
train_dir_class1 = 'ścieżka/do/katalogu/klasy1'
train_dir_class2 = 'ścieżka/do/katalogu/klasy2'

# Parametry
batch_size = 32
epochs = 50
image_height, image_width = 265, 302
input_shape = (image_height, image_width, 3)

# Katalogi z obrazkami
train_dir = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/Linden_Photos_ROI'
class1_dir = os.path.join(train_dir, '0')
class2_dir = os.path.join(train_dir, '1')

# Wyznaczanie ilości próbek w klasach
class1_samples = len(os.listdir(class1_dir))
class2_samples = len(os.listdir(class2_dir))

# Obliczenie współczynnika oversampling
oversample_ratio = int(class2_samples / class1_samples)

# Obliczanie wag dla niezrównoważonych klas
num_class1 = len(os.listdir(train_dir_class1))
num_class2 = len(os.listdir(train_dir_class2))
total_images = num_class1 + num_class2

class_weights = {
    0: total_images / (2 * num_class1),
    1: total_images / (2 * num_class2)
}

# Przygotowanie danych
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    directory=os.path.dirname(train_dir_class1),
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    directory=os.path.dirname(train_dir_class1),
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'
)

# Budowanie modelu sieci CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

# Kompilowanie modelu
model.compile(optimizer=Adam(learning_rate=1e-4),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Wytrenowanie modelu
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator,
    class_weight=class_weights
)

# Zapisanie modelu
model.save('image_classifier.h5')
