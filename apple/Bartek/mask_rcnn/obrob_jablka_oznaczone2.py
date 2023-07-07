import os
from os import walk
import shutil
import json
import PIL
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
import pickle
def zwroc_maske(cx,cy,r,width,height):
    xv, yv = np.meshgrid(np.arange(width), np.arange(height), indexing='ij')
    r2 = np.power(r, 2)
    maska = (np.power(xv-cx,2)+np.power(yv-cy,2))<=r2
    x, y = np.where(maska)
    points = np.stack([x,y], axis = 1)
    hull = ConvexHull(points)
    x = points[hull.vertices, 0]
    y = points[hull.vertices, 1]
    return x, y

def listuj_sciezke(katalog):
    for (dirpath, katalogi, pliki) in walk(katalog):
        break
    return katalogi, pliki

def get_xml_file(pliki):
    x = []
    for plik in pliki:
        if plik.endswith('.csv'):
            x.append(plik)
    return x


def get_file_dict(data, plik):
    wyniki = []
    wyniki_file_dict = []
    for file_dict in data.keys():
        if data[file_dict]['filename'] == f"{plik}.jpg":
            for file_dict in data.keys():
                if data[file_dict]['filename'] == f"{plik}.jpg":
                    wyniki.append(data[file_dict])
                    wyniki_file_dict.append(file_dict)
    if len(wyniki)!=1:
        print(f"lipa z {file_dict}")
        exit()
    return wyniki[0], wyniki_file_dict[0]


json_folder = '/media/bart/Elements SE/Jablka_oznaczone2/jsony/'
obrazy_folder = '/media/bart/Elements SE/Jablka_oznaczone2/obrazy/'

wynik_json = {}

powiekszenie = 'Zoom'
i = 0
path = '/media/bart/Elements SE/Jablka_oznaczone2/OneDrive_1_5-11-2023/'
katalogi, _ = listuj_sciezke(path)
for katalkog_gatunek in katalogi:
    katalogi_data, _ = listuj_sciezke(path + katalkog_gatunek)
    for katalog_data in katalogi_data:
        katalog_dane = f"{path + katalkog_gatunek}/{katalog_data}/{powiekszenie}/"
        _, pliki = listuj_sciezke(katalog_dane)
        pliki = get_xml_file(pliki)
        for plik in pliki:
            plik = os.path.splitext(plik)[0]
            plik_jpg_src = f"{katalog_dane}/{plik}.jpg"
            plik_json_src = f"{katalog_dane}/{plik}.json"

            plik_jpg_dst = f"{obrazy_folder}/{plik}.jpg"
            plik_json_dst = f"{json_folder}/{plik}.json"

            shutil.copy(plik_jpg_src, plik_jpg_dst)
            shutil.copy(plik_json_src, plik_json_dst)
            i+=1
            # print(katalog_dane)
            # print(plik)
            img = Image.open(plik_jpg_src)
            width, height = img.size

            with open(plik_json_dst) as json_file:
                data = json.load(json_file)
            atrybuty, filename_kod = get_file_dict(data, plik)


            regions = atrybuty['regions']
            # slownik_per_obraz = {filename_kod}
            slownik_per_obraz ={'filename':atrybuty['filename'],
                                'size':atrybuty['size']
                                }
            owoce = []
            for owoc in regions:
                kolko = owoc['shape_attributes']
                all_points_x, all_points_y = zwroc_maske(kolko['cx'], kolko['cy'], kolko['r'], width, height)
                kolko["name"] = "polygon"
                kolko["all_points_x"] = all_points_x.tolist()
                kolko["all_points_y"] = all_points_y.tolist()
                kolko.pop('cx')
                kolko.pop('cy')
                kolko.pop('r')
                owoc['region_attributes'] = {'owoc': 'jablko'}
                owoce.append(owoc)

            # print(owoce)
            slownik_per_obraz['regions']=owoce
            # wynik_json.append(slownik_per_obraz)
            print(f"{filename_kod}, i = {i}")
            wynik_json[filename_kod]=slownik_per_obraz

print(wynik_json)
with open("/media/bart/Elements SE/Jablka_oznaczone2/jablka_oznaczone2.list", "w") as fp:
    json.dump(wynik_json, fp)

# >>> with open("test", "r") as fp:
# ...     b = json.load(fp)

new_file = '/media/bart/Elements SE/Jablka_oznaczone2/jablka_oznaczone2.json'
with open(new_file, 'w') as f:
    json.dump(wynik_json, f)

print(f"{i} plikow, len(wynik_json) = {len(wynik_json)}")











