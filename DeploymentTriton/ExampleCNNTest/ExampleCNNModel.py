import tensorflow as tf
from tensorflow.keras import datasets, layers, models

# Pobranie i przygotowanie zestawu danych CIFAR10
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# Normalizacja wartości pikseli do przedziału 0 do 1
train_images, test_images = train_images / 255.0, test_images / 255.0

# Definiowanie architektury modelu
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# Dodanie warstw Dense
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))

# Kompilowanie i trenowanie modelu
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=20,
                    validation_data=(test_images, test_labels))

# Zapisanie modelu do formatu .pb (SavedModel format) dla Nvidia Triton Inference Server
model.save('ExampleCNNModelv1', save_format='tf')  # gdzie model_path to ścieżka, do której chcesz zapisać model
