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
from tensorflow.keras.applications import VGG16

#width = 321
#height = 384

def load_images_and_labels(class_dirs):
    imagefilenames, images_class0, images_class1, labels = [], [], [], []
    max_width, max_height = 0, 0

    total_files = sum([len(os.listdir(class_dir)) for class_dir in class_dirs])
    with tqdm(total=total_files, desc="Loading images", dynamic_ncols=True) as pbar:
        for label, class_dir in enumerate(class_dirs):
            for img_file in os.listdir(class_dir):
                if img_file.endswith('.jpg'):
                    img_path = os.path.join(class_dir, img_file)
                    img = Image.open(img_path).resize((321, 384))

                    imagefilenames.append(img_file)
                    if label == 0:
                        images_class0.append(np.array(img))
                    else:
                        images_class1.append(np.array(img))
                    labels.append(label)

                    pbar.update(1)

    # Balancing the classes
    if len(images_class1) < len(images_class0):
        selected_indices = np.random.choice(len(images_class0), len(images_class1), replace=False)
        images_class0 = [images_class0[i] for i in selected_indices]
    else:
        selected_indices = np.random.choice(len(images_class1), len(images_class0), replace=False)
        images_class1 = [images_class1[i] for i in selected_indices]

    images = images_class0 + images_class1
    labels = [0] * len(images_class0) + [1] * len(images_class1)

    return np.array(images), np.array(labels)


def load_images_and_labelsold(class_dirs):
    imagefilenames, images, labels = [], [], []
    max_width, max_height = 0, 0

    total_files = sum([len(os.listdir(class_dir)) for class_dir in class_dirs])
    with tqdm(total=total_files, desc="Loading images", dynamic_ncols=True) as pbar:
        for label, class_dir in enumerate(class_dirs):
            for img_file in os.listdir(class_dir):
                if img_file.endswith('.jpg'):
                    img_path = os.path.join(class_dir, img_file)
                    img = Image.open(img_path).resize((321, 384))  # Dostosowanie rozmiaru do największych wymiarów

                    imagefilenames.append(img_file)
                    images.append(np.array(img))
                    labels.append(label)

                    pbar.update(1)

    return np.array(images), np.array(labels)

print(platform.python_version())
print(tf.version.VERSION)
print("Num of GPUs available: ", tf.test.gpu_device_name())

start = time.process_time()

class_dirs = ['Linden_Photos_WellExposed_ROIs/0', 'Linden_Photos_WellExposed_ROIs/1']

images_list, labels = load_images_and_labels(class_dirs)

print("Shape of images_list:", images_list.shape)
print("Shape of labels:", labels.shape)

unique_classes, counts = np.unique(labels, return_counts=True)

for u, c in zip(unique_classes, counts):
    print(f"Number of images in class {u}: {c}")

print('After loaded images')
print(time.process_time() - start)


X_train, X_temp, y_train, y_temp = train_test_split(images_list, labels, stratify=labels, test_size=0.3,
                                                    random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, stratify=y_temp, test_size=0.5, random_state=42)

# Computing class weights
#class_weights = compute_sample_weight(class_weight='balanced', y=y_train)
#class_weight_dict = dict(enumerate(class_weights))

print(np.shape(X_train))
print(np.shape(y_train))

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(384, 321, 3))

# Zamrażanie warstw bazowego modelu
for layer in base_model.layers:
    layer.trainable = False

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(2, activation='softmax')
])

# model = tf.keras.Sequential([
#     tf.keras.layers.InputLayer(input_shape=(384, 321, 3)),
#     tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
#     tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
#     tf.keras.layers.GlobalAveragePooling2D(),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.Dense(2, activation='softmax')
# ])

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

# Setting up model checkpoint
checkpoint = tf.keras.callbacks.ModelCheckpoint('best_model_721.h5', monitor='val_loss', mode='min', save_best_only=True)

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(X_train, y_train, batch_size=32, epochs=500, validation_data=(X_val, y_val), callbacks=[early_stopping, checkpoint])

model.save('ClassificationLindenModelv3', save_format='tf')

plt.plot(history.history['loss'], label='Training loss')
plt.plot(history.history['val_loss'], label='Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig('Training_loss.png')

plt.plot(history.history['accuracy'], label='Training accuracy')
plt.plot(history.history['val_accuracy'], label='Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('Training_accuracy.png')

test_loss, test_accuracy = model.evaluate(X_test, y_test)

print(f"Test accuracy: {test_accuracy:.2f}")

y_pred = np.argmax(model.predict(X_test), axis=1)

cm = confusion_matrix(y_test, y_pred)
np.savetxt('confusion_matrix.csv', cm, delimiter=",")
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['0', '1'])
disp.plot(values_format='d')
plt.savefig('confusion_matrix.png')
