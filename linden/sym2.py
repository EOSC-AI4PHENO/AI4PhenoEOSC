import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Stałe
batch_size = 32
epochs = 50
image_height, image_width = 150, 150
input_shape = (image_height, image_width, 3)

# Katalogi z obrazkami
train_dir = 'path/to/train/directory'
class1_dir = os.path.join(train_dir, 'class1')
class2_dir = os.path.join(train_dir, 'class2')

# Wyznaczanie ilości próbek w klasach
class1_samples = len(os.listdir(class1_dir))
class2_samples = len(os.listdir(class2_dir))

# Obliczenie współczynnika oversampling
oversample_ratio = int(class2_samples / class1_samples)

# Wczytywanie i augmentacja danych
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    shear_range=0.2)

train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(image_height, image_width),
    batch_size=batch_size,
    class_mode='binary',
    subset='training')

validation_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(image_height, image_width),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation')

# Oversampling klasy mniejszej
train_generator.class_indices['class1'] *= oversample_ratio

# Budowanie modelu CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=Adam(learning_rate=0.001),
              metrics=['accuracy'])

# Callbacks
checkpoint = ModelCheckpoint('model.h5', save_best_only=True)
early_stopping = EarlyStopping(patience=5, restore_best_weights=True)

# Trenowanie modelu
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size,
    callbacks=[checkpoint, early_stopping])
