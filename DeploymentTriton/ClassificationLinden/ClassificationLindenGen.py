import os
import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import time
import platform
from tensorflow.python.framework.config import set_memory_growth
def load_images_and_labels(class_dirs, img_size=224):
    images, labels = [], []

    for label, class_dir in enumerate(class_dirs):
        for img_file in os.listdir(class_dir):
            if img_file.endswith('.jpg'):
                img_path = os.path.join(class_dir, img_file)
                img = Image.open(img_path)
                #img = img.resize((img_size, img_size))

                images.append(np.array(img))
                labels.append(label)

    return np.array(images), np.array(labels)

#os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
#print(os.getenv('TF_GPU_ALLOCATOR'))

#os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'

print(platform.python_version())
print(tf.version.VERSION)

print("Num of GPUs available: ", len(tf.test.gpu_device_name()))

start = time.process_time()

class_dirs = ['E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/LindenClassification/Linden_Photos_ROI/0', 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/LindenClassification/Linden_Photos_ROI/1']
images, labels = load_images_and_labels(class_dirs)

print('After loaded images')
print(time.process_time() - start)

X_train, X_temp, y_train, y_temp = train_test_split(images, labels, stratify=labels, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, stratify=y_temp, test_size=0.5, random_state=42)

# model = tf.keras.Sequential([
#     tf.keras.layers.InputLayer(input_shape=(365,302, 3)),
#     tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
#     tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
#     tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.Dense(2, activation='softmax')
# ])

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(None, None, 3)),  # zmieniamy input_shape na None, None
    tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.GlobalAveragePooling2D(),  # zmieniamy Flatten na GlobalAveragePooling2D
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(2, activation='softmax')
])


model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])


#with tf.device('/gpu:0'):
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = model.fit(X_train, y_train, batch_size=32, epochs=30, validation_data=(X_val, y_val), callbacks=[early_stopping])

model.save('ClassificationLindenModelv1', save_format='tf')  # gdzie model_path to ścieżka, do której chcesz zapisać model

plt.plot(history.history['loss'], label='Training loss')
plt.plot(history.history['val_loss'], label='Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
#plt.show()
plt.savefig('Training_loss.png')

plt.plot(history.history['accuracy'], label='Training accuracy')
plt.plot(history.history['val_accuracy'], label='Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
#plt.show()
plt.savefig('Training_accuracy.png')

test_loss, test_accuracy = model.evaluate(X_test, y_test)

print(f"Test accuracy: {test_accuracy:.2f}")

y_pred = np.argmax(model.predict(X_test), axis=1)

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['0', '1'])
disp.plot(values_format='d')
#plt.show()
plt.savefig('confusion_matrix.png')