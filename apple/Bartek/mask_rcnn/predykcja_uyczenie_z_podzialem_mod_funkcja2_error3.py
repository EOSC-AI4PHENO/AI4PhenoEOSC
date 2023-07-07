import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
# from matplotlib.path import contains_point
# from matplotlib.path import Path
from matplotlib import path
from sklearn.metrics import jaccard_score
from os import walk
import os
from os import walk
import shutil
import json
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

import PIL
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
import pickle
import numpy
from PIL import Image, ImageDraw
# from matplotlib.nxutils import points_inside_poly
# from mrcnn import utils
# from mrcnn import visualize
# from mrcnn.visualize import display_images
# from mrcnn.visualize import display_instances
# import mrcnn.model as modellib
# from mrcnn.model import log
# from mrcnn.config import Config
# from mrcnn import model as modellib, utils
# from mrcnn.visualize import display_images
# from mrcnn.visualize import display_instances

from skimage import draw
import numpy as np

def poly2mask(vertex_row_coords, vertex_col_coords, shape):
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask

def get_file_dict(data, plik):
    wyniki = []
    wyniki_file_dict = []
    for file_dict in data.keys():
        if data[file_dict]['filename'] == plik:
            wyniki.append(data[file_dict])
            wyniki_file_dict.append(file_dict)
    # if len(wyniki)!=1:
    #     print(f"lipa z {file_dict}")
    #     exit()
    return wyniki, wyniki_file_dict


def listuj_sciezke(katalog):
    for (dirpath, katalogi, pliki) in walk(katalog):
        break
    return katalogi, pliki


def rysuj_obrazek(path_to_new_image, DETECTION_MIN_CONFIDENCE_, nr_folder):
    from mrcnn import utils
    from mrcnn import visualize
    from mrcnn.visualize import display_images
    from mrcnn.visualize import display_instances
    import mrcnn.model as modellib
    from mrcnn.model import log
    from mrcnn.config import Config
    from mrcnn import model as modellib, utils
    from mrcnn.visualize import display_images
    from mrcnn.visualize import display_instances

    # Root directory of the project
    # ROOT_DIR = "D:\\env_with_tensorflow1.14\\all_maskrcnn\\maskrcnn_truck_car"
    ROOT_DIR = "/home/bart/Mask_RCNN_jeszcze_raz/Pycharm/Mask_RCNN"
    DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")
    # WEIGHTS_PATH = "/home/bart/Mask_RCNN_jeszcze_raz/Pycharm/Mask_RCNN/logs/object20230508T2128/mask_rcnn_object_0020.h5"
    # WEIGHTS_PATH = '/home/bart/Mask_RCNN_jeszcze_raz/Pycharm/Mask_RCNN/logs/object20230509T2304/mask_rcnn_object_0020.h5'

    # WEIGHTS_PATH = '/home/bart/Mask_RCNN_jeszcze_raz/Pycharm/Mask_RCNN/logs/object20230511T0743/mask_rcnn_object_0200.h5'

    WEIGHTS_PATH = '//home/bart/Mask_RCNN_jeszcze_raz/Pycharm/Mask_RCNN/logs/object20230519T1208/mask_rcnn_object_1000.h5'
    class CustomConfig(Config):
        """Configuration for training on the custom  dataset.
        Derives from the base Config class and overrides some values.
        """
        # Give the configuration a recognizable name
        NAME = "object"
        IMAGES_PER_GPU = 1
        NUM_CLASSES = 1 + 1  # Background + Apples
        # Number of training steps per epoch
        STEPS_PER_EPOCH = 10
        # Skip detections with < 90% confidence
        DETECTION_MIN_CONFIDENCE = DETECTION_MIN_CONFIDENCE_



    # Inspect the model in training or inference modes values: 'inference' or 'training'
    TEST_MODE = "inference"
    ROOT_DIR = "/home/bart/Mask_RCNN_jeszcze_raz/zdjecia_jablek"
    CUSTOM_DIR = "/home/bart/Mask_RCNN_jeszcze_raz/zdjecia_jablek"

    config = CustomConfig()
    #LOAD MODEL. Create model in inference mode
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # Load COCO weights Or, load the last model you trained
    weights_path = WEIGHTS_PATH
    # Load weights
    print("Loading weights ", weights_path)
    model.load_weights(weights_path, by_name=True)

    # path_to_new_image ='/home/bart/Mask_RCNN_jeszcze_raz/zdjecia_jablek/wynikowe/3/wejscie3.jpeg'
    # path_to_new_image ='/media/bart/Elements SE/Jablka_Oznaczone/wyniki/train/20220803_1207_0700F136_PIC_111_CAM_2.xml.pi.jpg'
    # path_to_new_image = '/media/bart/Elements SE/Jablka_Oznaczone/wyniki/train/20220907_1137_0700F136_PIC_145_CAM_2.xml.pi.jpg'
    # path_to_new_image = '/media/bart/Elements SE/Jablka_Oznaczone/wyniki/z_podzialem_na_proby/inne/20220904_1158_0700F136_PIC_141_CAM_2.xml.pi.jpg'
    print(f"path_to_new_image = {path_to_new_image}")
    image = mpimg.imread(path_to_new_image)

    results = model.detect([image], verbose=1)
    # print(results)
    r = results[0]

    sciezka_zapisu = '/home/bart/Mask_RCNN_jeszcze_raz/przykladowe_wyniki/_bledy'
    sciezka_zapisu = f"{sciezka_zapisu}/{nr_folder}/"
    if not os.path.isdir(sciezka_zapisu):
        os.makedirs(sciezka_zapisu)

    (dirname, filename) = os.path.split(path_to_new_image)
    fileextension = os.path.splitext(filename)[1]
    # filename = os.path.splitext(filename)[0]
    # filename = filename + f"_th{DETECTION_MIN_CONFIDENCE}"+fileextension
    filename_zapis = f"wyjscie_th{DETECTION_MIN_CONFIDENCE_}" + fileextension
    # print(f"filename to write = {filename}")

    # print(r['masks'])
    # print(r['masks'].shape)

    inne_json = '/media/bart/Elements SE/Jablka_Oznaczone/wyniki/z_podzialem_na_proby/inne/inne.json'
    with open(inne_json) as json_file:
        data = json.load(json_file)
    # print(data.keys())
    head, tail = os.path.split(path_to_new_image)
    # print(tail)

    atrybuty, filename_kod = get_file_dict(data, tail)

    print(f"filename_kod = {filename_kod}")
    poligony= data[filename_kod[0]]['regions']
    img = image.copy().astype(np.float)
    base_mask = np.full(image.shape[:-1], False)

    for polygon in poligony:
        # print(polygon['shape_attributes'])
        x = np.array(polygon['shape_attributes']['all_points_x'])
        y = np.array(polygon['shape_attributes']['all_points_y'])
        mask = poly2mask(vertex_row_coords=y, vertex_col_coords=x, shape=image.shape[:-1])
        base_mask = np.logical_or(base_mask, mask)

    # pomoc = img[:,:,0]
    # pomoc[base_mask]=255
    # img[:,:,0] = pomoc
    #
    # img = np.clip(img, 0, 255).astype(np.uint8)
    #
    # plt.imshow(img)
    # plt.show()
    # exit()

        # poly_verts = np.stack((x,y)).T
        # print(list(poly_verts))
        # exit()

        # p.contains_points([(.5, .5)]

        # p = path.Path([(0, 0), (0, 1), (1, 1), (1, 0)])

        # #
        # x, y = np.meshgrid(np.arange(image.shape[0]), np.arange(image.shape[1]))
        # x, y = x.flatten(), y.flatten()
        # points = np.vstack((x, y)).T
        # grid = plt. contains_points(points, poly_verts)
        # print(grid)
        #
        # print(xy)
        # matplotlib.path.Path.contains_point
        # coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))  # coors.shape is (4000000,2)

        # mask = poly_path.contains_points(coors)

        # print(polygon)
        # ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
    # exit()
    # mask = numpy.array(img)
    # print(np.mean(mask))



    # exit()

    ax = plt.axes()
    # fig, axs = plt.subplots(2)
    visualize.display_instances_mod(image, r['rois'], r['masks'], r['class_ids'],['BG', 'owoc'],r['scores'], ax=ax, title="Predictions1")
    # visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],['BG', 'owoc'],r['scores'], ax=axs[1], title="Predictions1")

    # print(base_mask.shape)
    # print(r['masks'].shape)
    #
    estimated_mask = np.full(image.shape[:-1], False)
    for i in range(r['masks'].shape[2]):
        estimated_mask = np.logical_or(estimated_mask, r['masks'][:,:,i])

    # miou = jaccard_score(y_true = base_mask, y_pred = estimated_mask, pos_label=True)
    # miou = jaccard_score(y_true=base_mask, y_pred = estimated_mask, average='micro', pos_label=True)\
    miou_F = jaccard_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(), pos_label=False)
    miou_T = jaccard_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(), pos_label=True)
    # miou = jaccard_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(), average = 'macro')
    miou = jaccard_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(), average='micro')


    # print(f"miou_T = {miou_T}, miou_F = {miou_F}, miou = {miou}, srednie = {(miou_T + miou_F)/2}")
    # exit()

    # f1 = f1_score(y_true=base_mask, y_pred = estimated_mask, average='micro', pos_label=True)
    f1 = f1_score(y_true=base_mask.flatten(), y_pred=estimated_mask.flatten(), pos_label=True)
    acc = accuracy_score(y_true=base_mask.flatten(), y_pred = estimated_mask.flatten())
    tn, fp, fn, tp = confusion_matrix(y_true=base_mask.flatten(), y_pred = estimated_mask.flatten(), normalize = 'all').ravel()

    # print(f"miou = {miou}, f1 = {f1}, acc = {acc}, tn={tn}, fp={fp}, fn={fn}, tp={tp}")
    # f1  = 2*tp/(2*tp+fp+fn)
    # print(f"f1 = {f1}")
    #
    # licznik = np.sum(np.logical_and(base_mask, estimated_mask))
    # mianownik = np.sum(np.logical_or(base_mask, estimated_mask))
    # print(f"miou_hm  {licznik/mianownik}")
    # exit()
    # miou, f1, acc, tn, fp, fn, tp
    #
    # print(f"miou = {miou}")
    #
    # pomoc = img[:,:,1]
    # pomoc[estimated_mask]=255
    # img[:,:,1] = pomoc
    # img = np.clip(img, 0, 255).astype(np.uint8)
    # plt.imshow(img)
    # plt.show()
    # exit()

    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    ax.axis('tight')
    ax.axis('off')

    zoom = 2
    fig = plt.gcf()
    w, h = fig.get_size_inches()
    fig.set_size_inches(w * zoom, h * zoom)

    plt.savefig(sciezka_zapisu+filename_zapis, bbox_inches = 'tight',pad_inches = 0)
    # plt.show()
    plt.close()

    plt.imshow(image)

    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    zoom = 2
    fig = plt.gcf()
    w, h = fig.get_size_inches()
    fig.set_size_inches(w * zoom, h * zoom)

    plt.savefig(sciezka_zapisu+filename, bbox_inches = 'tight', pad_inches = 0)


    plt.close()
    plt.close('all')
    # plt.show()
    return miou, f1, acc, tn, fp, fn, tp

path_to_inne = '/media/bart/Elements SE/Jablka_Oznaczone/wyniki/z_podzialem_na_proby/inne/'
katalogi, pliki = listuj_sciezke(path_to_inne)
df_results = pd.DataFrame(columns = ['file','miou0k5','f10k5','acc0k5','tn0k5','fp0k5','fn0k5','tp0k5',
                                     'miou0k95','f10k95','acc0k95','tn0k95','fp0k95','fn0k95','tp0k95'])
for nr_folder, plik in enumerate(pliki):
    path_to_new_image = path_to_inne + plik
    miou0k5, f10k5, acc0k5, tn0k5, fp0k5, fn0k5, tp0k5 = rysuj_obrazek(path_to_new_image, DETECTION_MIN_CONFIDENCE_=0.5, nr_folder=nr_folder+1)
    miou0k95, f10k95, acc0k95, tn0k95, fp0k95, fn0k95, tp0k95 = rysuj_obrazek(path_to_new_image, DETECTION_MIN_CONFIDENCE_=0.9, nr_folder=nr_folder+1)
    rekord = [plik,miou0k5, f10k5, acc0k5, tn0k5, fp0k5, fn0k5, tp0k5,miou0k95, f10k95, acc0k95, tn0k95, fp0k95, fn0k95, tp0k95]
    df_results.loc[df_results.shape[0]]=rekord
    df_results.to_csv('metryki_1000.csv', index = False)
    print(df_results)

# path_to_new_image = '/media/bart/Elements SE/Jablka_Oznaczone/wyniki/z_podzialem_na_proby/inne/20220702_1452_0700F136_PIC_76_CAM_2.xml.pi.jpg'
#