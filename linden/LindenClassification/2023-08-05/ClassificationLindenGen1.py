import os
import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import time
import platform
from tqdm import tqdm
from tensorflow.python.framework.config import set_memory_growth
def load_images_and_labels(class_dirs):
    images, labels = [], []

    total_files = sum([len(os.listdir(class_dir)) for class_dir in class_dirs])

    with tqdm(total=total_files, desc="Loading images", dynamic_ncols=True) as pbar:
        for label, class_dir in enumerate(class_dirs):
            for img_file in os.listdir(class_dir):
                if img_file.endswith('.jpg'):
                    img_path = os.path.join(class_dir, img_file)
                    img = Image.open(img_path)

                    images.append(np.array(img))
                    labels.append(label)

                    pbar.update(1)

    return np.array(images), np.array(labels)


print(platform.python_version())
print(tf.version.VERSION)
print("Num of GPUs available: ", tf.test.gpu_device_name())

start = time.process_time()

class_dirs = ['E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/Linden_Photos_WellExposed_ROIs/0', 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/Linden_Photos_WellExposed_ROIs/1']
images, labels = load_images_and_labels(class_dirs)

print('After loaded images')
print(time.process_time() - start)

X_train, X_temp, y_train, y_temp = train_test_split(images, labels, stratify=labels, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, stratify=y_temp, test_size=0.5, random_state=42)

# Computing class weights
class_weights = compute_class_weight('balanced', np.unique(y_train), y_train)
class_weight_dict = dict(enumerate(class_weights))

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(None, None, 3)),
    tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

# Setting up model checkpoint
checkpoint = tf.keras.callbacks.ModelCheckpoint('best_model.h5', monitor='val_loss', mode='min', save_best_only=True)

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_val, y_val), callbacks=[early_stopping, checkpoint], class_weight=class_weight_dict)

model.save('ClassificationLindenModelv2', save_format='tf')

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
