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
import base64
import io

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
    #regions=data_json['regions']
    photos = data_json.keys()
    for photo in photos:
        one_photo = data_json[photo]
        regions = one_photo['regions']
        for region in regions.values():
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

    avg_width, avg_height = np.mean(width_all), np.mean(height_all)
    avg_area = np.mean(np.array(area_all))
    number_of_apples = len(width_all)
    return mask_all, avg_width, avg_height, number_of_apples, avg_area

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

def calculate_indicatorsold(img, apple_data_json, ROI_data_json = None):
    mask_apples, avg_width, avg_height, number_of_apples, avg_area = make_mask_with_calculation(img, apple_data_json)
    df = calculate_indicators_for_mask(img, mask_apples)

    df['avg_width'] =avg_width
    df['avg_height'] = avg_height
    df['avg_area'] = avg_area
    df['number_of_apples'] = number_of_apples

    return df


def calculate_indicators(img, apple_data_json_base64, ROI_data_json_base64=None):
    #img_data = base64.b64decode(img_base64)
    #nparr = np.frombuffer(img_data, np.uint8)
    #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR oznacza, że chcemy załadować obraz jako BGR
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # następnie konwertujemy go na RGB

    apple_data_json_data = base64.b64decode(apple_data_json_base64)
    apple_data_json = json.loads(apple_data_json_data.decode('utf-8'))

    mask_apples, avg_width, avg_height, number_of_apples, avg_area = make_mask_with_calculation(img, apple_data_json)
    df = calculate_indicators_for_mask(img, mask_apples)

    df['avg_width'] =avg_width
    df['avg_height'] = avg_height
    df['avg_area'] = avg_area
    df['number_of_apples'] = number_of_apples

    return df

# fullnameIMG='E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/WskaznikiBartek/20220914_1207_0700F136_PIC_150_CAM_2.xml.pi.jpg'
# fullnameJSON='E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/WskaznikiBartek/20220914_1207_0700F136_PIC_150_CAM_2.xml.pi.json'
#
# filename = os.path.basename(fullnameIMG)
#
# df_all = []
#
# # Przygotuj dane wejściowe do funkcji calculate_indicators
# with open(fullnameIMG, "rb") as img_file:
#     img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
#
# with open(fullnameJSON, "rb") as json_file:
#     apple_data_json_base64 = base64.b64encode(json_file.read()).decode('utf-8')
#
# # Wywołaj funkcję calculate_indicators z danymi wejściowymi
# df_local = calculate_indicators(img_base64, apple_data_json_base64)

# r_av = float(df_local["r.av"].iloc[0])
# g_av = float(df_local["g.av"].iloc[0])
# b_av = float(df_local["b.av"].iloc[0])
# r_sd = float(df_local["r.sd"].iloc[0])
# g_sd = float(df_local["g.sd"].iloc[0])
# b_sd = float(df_local["b.sd"].iloc[0])
# bri_av = float(df_local["bri.av"].iloc[0])
# bri_sd = float(df_local["bri.sd"].iloc[0])
# gi_av = float(df_local["gi.av"].iloc[0])
# gei_av = float(df_local["gei.av"].iloc[0])
# gei_sd = float(df_local["gei.sd"].iloc[0])
# ri_av = float(df_local["ri.av"].iloc[0])
# ri_sd = float(df_local["ri.sd"].iloc[0])
# bi_av = float(df_local["bi.av"].iloc[0])
# bi_sd = float(df_local["bi.sd"].iloc[0])
# avg_width = float(df_local["avg_width"].iloc[0])
# avg_height = float(df_local["avg_height"].iloc[0])
# avg_area = float(df_local["avg_area"].iloc[0])
# number_of_apples = int(df_local["number_of_apples"].iloc[0])

# output = AutomaticAppleSegmentationWithIndicatorsOutput(
#     task_id = 'your_task_id',  # zamień na prawdziwe ID zadania
#     status = 'your_status',  # zamień na prawdziwy status
#     filename = 'your_filename',  # zamień na prawdziwą nazwę pliku
#     jsonBase64AppleROIs = 'your_json',  # zamień na prawdziwy JSON
#     r_av = r_av,
#     g_av = g_av,
#     b_av = b_av,
#     r_sd = r_sd,
#     g_sd = g_sd,
#     b_sd = b_sd,
#     bri_av = bri_av,
#     bri_sd = bri_sd,
#     gi_av = gi_av,
#     gei_av = gei_av,
#     gei_sd = gei_sd,
#     ri_av = ri_av,
#     ri_sd = ri_sd,
#     bi_av = bi_av,
#     bi_sd = bi_sd,
#     avg_width = avg_width,
#     avg_height = avg_height,
#     avg_area = avg_area,
#     number_of_apples = number_of_apples
# )

# df_local['img_file'] = filename
# df_all.append(df_local)
#
# df_all = pd.concat(df_all, ignore_index=True).reset_index(inplace = False, drop = True)
# columns = list(df_all)
# columns = [columns[-1]]+columns[:-1]
# df_all = df_all[columns]
#
# # Zapisz DataFrame do pliku Excela
# df_all.to_excel('wyniki_with_area2.xlsx', index=False)