import json
from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull

def circle2polygon(cx,cy,r,width,height):
    xv, yv = np.meshgrid(np.arange(width), np.arange(height), indexing='ij')
    r2 = np.power(r, 2)
    maska = (np.power(xv-cx,2)+np.power(yv-cy,2))<=r2
    x, y = np.where(maska)
    points = np.stack([x,y], axis = 1)
    hull = ConvexHull(points)
    x = points[hull.vertices, 0]
    y = points[hull.vertices, 1]
    return x.tolist(), y.tolist()

def ellipse2polygon(cx,cy,rx, ry, theta,width,height):
    xv, yv = np.meshgrid(np.arange(width), np.arange(height), indexing='ij')
    maska = np.power((np.cos(theta)*(xv-cx)+np.sin(theta)*(yv-cy))/rx,2)+np.power((-np.sin(theta)*(xv-cx)+np.cos(theta)*(yv - cy))/ry,2) <= 1
    x, y = np.where(maska)
    points = np.stack([x,y], axis = 1)
    hull = ConvexHull(points)
    x = points[hull.vertices, 0]
    y = points[hull.vertices, 1]
    return x.tolist(), y.tolist()

def rect2polygon(x,y,rwidth,rheight,width,height):
    x = [x, x,              x+rwidth-1,     x+rwidth-1]
    y = [y, y+rheight - 1,  y+rheight - 1,  y ]
    x = np.maximum(np.minimum(np.array(x),width),1).tolist()
    y = np.maximum(np.minimum(np.array(y), height), 1).tolist()
    return [x,y]


image_file = 'obraz_wejscie.png'
json_file = 'json_wejscie.json'
img = Image.open(image_file)
width, height = img.size


with open(json_file) as json_file:
    data = json.load(json_file)
    photos = data.keys()
    for photo in photos:
        one_photo = data[photo]
        regions = one_photo['regions']
        for region in regions:
            shape_attributes = region['shape_attributes']
            name = shape_attributes['name']
            if name in ['circle','ellipse','rect']:
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
                        width=width,height=height)

                elif name == 'rect':
                    x, y =  rect2polygon(x=shape_attributes['x'],
                                         y=shape_attributes['y'],
                                         rwidth=shape_attributes['width'],
                                         rheight=shape_attributes['height'],
                                         width=width, height=height)

                region['shape_attributes'] = {'name':'polygon', 'all_points_x':x,
                                        'all_points_y':y}


new_file = 'json_wyjscie.json'
with open(new_file, 'w') as f:
    json.dump(data, f)

# print(f"sprawdzenie")
# photos = data.keys()
# for photo in photos:
#     one_photo = data[photo]
#     regions = one_photo['regions']
#     for region in regions:
#         shape_attributes = region['shape_attributes']
#         print(shape_attributes)