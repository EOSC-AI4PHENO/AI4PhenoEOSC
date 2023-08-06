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
import numpy as np
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput, InferResult
import base64
import json
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
import base64
import io


def circle2polygon(cx, cy, r, width, height):
    xv, yv = np.meshgrid(np.arange(width), np.arange(height), indexing='ij')
    r2 = np.power(r, 2)
    maska = (np.power(xv - cx, 2) + np.power(yv - cy, 2)) <= r2
    x, y = np.where(maska)
    points = np.stack([x, y], axis=1)
    hull = ConvexHull(points)
    x = points[hull.vertices, 0]
    y = points[hull.vertices, 1]
    return x.tolist(), y.tolist()


def ellipse2polygon(cx, cy, rx, ry, theta, width, height):
    xv, yv = np.meshgrid(np.arange(width), np.arange(height), indexing='ij')
    maska = np.power((np.cos(theta) * (xv - cx) + np.sin(theta) * (yv - cy)) / rx, 2) + np.power(
        (-np.sin(theta) * (xv - cx) + np.cos(theta) * (yv - cy)) / ry, 2) <= 1
    x, y = np.where(maska)
    points = np.stack([x, y], axis=1)
    hull = ConvexHull(points)
    x = points[hull.vertices, 0]
    y = points[hull.vertices, 1]
    return x.tolist(), y.tolist()


def rect2polygon(x, y, rwidth, rheight, width, height):
    x = [x, x, x + rwidth - 1, x + rwidth - 1]
    y = [y, y + rheight - 1, y + rheight - 1, y]
    x = np.maximum(np.minimum(np.array(x), width), 1).tolist()
    y = np.maximum(np.minimum(np.array(y), height), 1).tolist()
    return [x, y]


def Convert2Polygon1(jsonfile_base64: str, width: int, height: int):
    json_bytes = base64.b64decode(jsonfile_base64)
    json_file = io.StringIO(json_bytes.decode('utf-8'))
    data = json.load(json_file)
    photos = data.keys()
    for photo in photos:
        one_photo = data[photo]
        regions = one_photo['regions']
        new_regions = {}  # utworzenie nowego słownika
        for i, region in enumerate(regions):
            shape_attributes = region['shape_attributes']
            name = shape_attributes['name']
            if name in ['circle', 'ellipse', 'rect']:
                if name == 'circle':
                    x, y = circle2polygon(cx=shape_attributes['cx'],
                                          cy=shape_attributes['cy'],
                                          r=shape_attributes['r'],
                                          width=width, height=height)
                elif name == 'ellipse':
                    x, y = ellipse2polygon(
                        cx=shape_attributes['cx'],
                        cy=shape_attributes['cy'],
                        rx=shape_attributes['rx'],
                        ry=shape_attributes['ry'],
                        theta=shape_attributes['theta'],
                        width=width, height=height)

                elif name == 'rect':
                    x, y = rect2polygon(x=shape_attributes['x'],
                                        y=shape_attributes['y'],
                                        rwidth=shape_attributes['width'],
                                        rheight=shape_attributes['height'],
                                        width=width, height=height)

                region['shape_attributes'] = {'name': 'polygon', 'all_points_x': x,
                                              'all_points_y': y}
            new_regions[str(i)] = region  # dodajemy region do nowego słownika
        one_photo['regions'] = new_regions  # zastępujemy starą listę nowym słownikiem
    json_out = json.dumps(data)
    return base64.b64encode(json_out.encode('utf-8')).decode('utf-8')


def jsonfile_to_base64(jsonfilename: str) -> str:
    with open(jsonfilename, 'r', encoding='utf-8') as json_file:
        json_content = json_file.read()
    return base64.b64encode(json_content.encode('utf-8')).decode('utf-8')


def base64_to_jsonfile(jsoncontent_base64: str, outputfilename: str):
    json_content = base64.b64decode(jsoncontent_base64).decode('utf-8')
    with open(outputfilename, 'w', encoding='utf-8') as json_file:
        json_file.write(json_content)


def infer(image: np.ndarray):
    # Ustawienia
    url = "10.0.20.50:8001"
    model_name = "ClassificationLinden"

    # Inicjalizacja klienta
    client = InferenceServerClient(url)

    image = np.expand_dims(image, axis=0)

    # Konwersja danych na InferInput
    infer_input = InferInput("input_1", image.shape, "FP32")
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


def cropImages(imageRGB: np.ndarray, jsonBase64ImageROIs: str):
    height, width, _ = imageRGB.shape
    jsonBase64ImageROIsPolygon = Convert2Polygon1(jsonBase64ImageROIs, width, height)

    # Dekodowanie base64
    decoded_json = base64.b64decode(jsonBase64ImageROIsPolygon).decode('utf-8')

    # Konwersja na słownik Pythona
    json_data = json.loads(decoded_json)

    # Pierwszy klucz w słowniku
    first_key = list(json_data.keys())[0]

    # Wszystkie regiony
    regions = json_data[first_key]["regions"]

    images_roi = []

    # Przejście przez wszystkie regiony
    for region_key in regions.keys():
        region = regions[region_key]

        # Współrzędne punktów
        all_points_x = region["shape_attributes"]["all_points_x"]
        all_points_y = region["shape_attributes"]["all_points_y"]

        # Obliczanie prostokąta otaczającego
        min_x = min(all_points_x)
        max_x = max(all_points_x)
        min_y = min(all_points_y)
        max_y = max(all_points_y)

        image_roi = imageRGB[min_y:max_y, min_x:max_x]
        images_roi.append(image_roi)

    return images_roi

# def doCrop():
#     with open(
#         'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/example/LindenKlas/via_project_5Aug2023_18h44m_json.json',
#         'r') as f:
#         data = json.load(f)
#
#         # Konwersja danych JSON do stringa
#         data_string = json.dumps(data)
#
# # Konwersja stringa do bajtów
# data_bytes = data_string.encode('utf-8')
#
# # Konwersja bajtów do base64
# jsonBase64ImageROI = base64.b64encode(data_bytes)
#
# imageRGB = Image.open(
#     'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/example/LindenKlas/2022-06-19_02.48.33_class_1.jpg')
# imageRGB = np.array(imageRGB)
#
# croppedImagesList = cropImages(imageRGB, jsonBase64ImageROI)
# croppedImage = croppedImagesList[0]
# img = Image.fromarray(croppedImage)
# img.save('croppedImage.jpg')


def TestImageTriton(dir, filename):
    fullname = os.path.join(dir, filename)
    imageRGB = Image.open(fullname)
    imageRGB = np.array(imageRGB)

    prediction = infer(imageRGB)
    predicted_label = np.argmax(prediction)
    predicted_score = np.max(prediction)
    print(f'Triton: filename{filename}, klasa:{predicted_label},score={predicted_score}, wynik:{prediction}')

def TestImageLocalModel(dir, filename,model):

    fullname = os.path.join(dir, filename)
    imageRGB = Image.open(fullname)
    width = 321
    height = 384
    #img_resized = imageRGB.resize((model.input_shape[1], model.input_shape[2]))
    #img_resized = imageRGB.resize((384, 321))
    img_array = np.expand_dims(np.array(imageRGB), axis=0)  # Convert to (1, height, width, 3) shape

    #img_array=np.array(img_resized)
    #prediction = model.predict(img_array)
    #predicted_class = np.argmax(prediction, axis=1)[0]
    #y_pred_probs = loaded_model.predict(X_test)

    # 3. Make a prediction
    prediction = model.predict(img_array)
    #predicted_class = np.argmax(prediction, axis=1)[0]
    predicted_class = np.argmax(prediction, axis=1)
    predicted_score = np.max(prediction)
    print(f'Triton: filename{filename}, klasa:{predicted_class},score={predicted_score}, wynik:{prediction}')


dir = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/LindenClassification/2023-08-05/Linden_Photos_WellExposed_ROIs/1'

#dir = '/home/kurekj/AI4PhenoEOSC/linden/LindenClassification/2023-08-05/Linden_Photos_WellExposed_ROIs/1'


TestImageTriton(dir, '2022-06-19_04.18.34_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_04.28.35_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_04.38.35_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_04.48.36_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_04.58.35_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_05.18.35_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_05.28.34_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_05.28.34_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_05.38.34_class_1_ROI.jpg')
TestImageTriton(dir, '2022-06-19_05.48.34_class_1_ROI.jpg')

# loaded_model = tf.keras.models.load_model('ClassificationLindenModelv2')
#
# TestImageLocalModel(dir, '2022-06-19_04.18.34_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_04.28.35_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_04.38.35_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_04.48.36_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_04.58.35_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_05.18.35_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_05.28.34_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_05.28.34_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_05.38.34_class_1_ROI.jpg',loaded_model)
# TestImageLocalModel(dir, '2022-06-19_05.48.34_class_1_ROI.jpg',loaded_model)
