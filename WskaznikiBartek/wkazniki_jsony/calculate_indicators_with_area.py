from pathlib import Path
import os
from os import walk
import shutil
import json
import PIL
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
import cv2
from skimage import draw
import pandas as pd

images_path = 'D:/DataMining/SETH/Jablka_Sparsowane/preprocess/images/'
jsons_path = 'D:/DataMining/SETH/Jablka_Sparsowane/preprocess/jsons/'
n_pref = len(images_path)

def make_mask(img, data_json):
    height, width, _ = img.shape

    mask_all = np.full((height, width), False)
    regions=data_json['regions']
    for region in regions:
        shape_attributes = region['shape_attributes']
        x = shape_attributes['all_points_x']
        y = shape_attributes['all_points_y']

        polygon = np.stack((y, x), axis=1)
        mask = draw.polygon2mask((height, width), polygon)
        mask_all = np.logical_or(mask_all, mask)

    return mask_all



def make_mask_with_calculation(img, data_json):
    height, width, _ = img.shape
    width_all, height_all, area_all = [], [], []
    mask_all = np.full((height, width), False)
    regions=data_json['regions']
    for region in regions:
        shape_attributes = region['shape_attributes']
        x = shape_attributes['all_points_x']
        y = shape_attributes['all_points_y']

        local_width = np.ptp(np.array(x))
        local_height = np.ptp(np.array(y))

        width_all.append(local_width)
        height_all.append(local_height)

        polygon = np.stack((y, x), axis=1)
        mask = draw.polygon2mask((height, width), polygon)
        mask_all = np.logical_or(mask_all, mask)
        area_all.append(np.sum(mask))

    width_all, height_all =  np.array(width_all), np.array(height_all)

    avg_witdh, avg_height = np.mean(width_all), np.mean(height_all)
    avg_area = np.mean(np.array(area_all))
    number_of_apples = len(width_all)
    return mask_all, avg_witdh, avg_height, number_of_apples, avg_area

def calculate_indicators_for_mask(I, mask):
    I = I.astype(float)
    pos_dic = {0:'r',1:'g', 2:'b'}
    results = {}

    Ix = []
    for i in range(3):
        color_tmp = pos_dic[i]
        I_tmp = I[:,:,i]
        w_mean = np.nanmean(I_tmp[mask])
        w_std = np.nanstd(I_tmp[mask])
        results[f'{color_tmp}.av'] = w_mean
        results[f'{color_tmp}.sd'] = w_std
        Ix.append(I_tmp[mask])

    Ix = np.stack(Ix, axis = 1)

    Bi = np.sum(Ix, axis = 1)
    results['bri.av'] = np.nanmean(Bi)
    results['bri.sd'] = np.nanstd(Bi)

    for i in range(3):
        color_tmp = pos_dic[i]
        results[f'{color_tmp}i.av'] = np.nanmean(Ix[:,i]/Bi)
        results[f'{color_tmp}i.sd'] = np.nanstd(Ix[:,i]/Bi)

    results['gei.av'] = np.nanmean(2 * Ix[:, 1] - (Ix[:, 0]+Ix[:, 2]))
    results['gei.sd'] = np.nanstd(2 * Ix[:, 1] - (Ix[:, 0] + Ix[:, 2]))

    for key in results.keys():
        results[key] = [results[key]]

    df = pd.DataFrame.from_dict(results)
    df = df[['r.av','g.av','b.av','r.sd','g.sd','b.sd','bri.av','bri.sd',
              'gi.av','gi.sd','gei.av','gei.sd','ri.av','ri.sd','bi.av','bi.sd']]

    return df

def calculate_indicators(img, apple_data_json, ROI_data_json = None):
    mask_apples, avg_witdh, avg_height, number_of_apples, avg_area = make_mask_with_calculation(img, apple_data_json)
    df = calculate_indicators_for_mask(img, mask_apples)

    df['avg_witdh'] =avg_witdh
    df['avg_height'] = avg_height
    df['avg_area'] = avg_area
    df['number_of_apples'] = number_of_apples

    return df

df_all = []
for i, image_path in enumerate(Path(images_path).rglob('*.*')):
    print(f"i = {i+1}, image_path = {image_path}")
    img_file_short = f"{image_path}"[n_pref:]

    base_file = os.path.splitext(img_file_short)[0]
    json_file = jsons_path + base_file + '.json'
    img_file = f"{images_path}{img_file_short}"
    json_file = f"{json_file}"

    img = cv2.imread(img_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with open(json_file) as json_file:
        apple_data_json = json.load(json_file)

    df_local = calculate_indicators(img, apple_data_json)
    df_local['img_file'] = img_file_short

    df_all.append(df_local)

df_all = pd.concat(df_all, ignore_index=True).reset_index(inplace = False, drop = True)
columns = list(df_all)
columns = [columns[-1]]+columns[:-1]
df_all = df_all[columns]

df_all.to_csv('wyniki_with_area.csv', index = False)