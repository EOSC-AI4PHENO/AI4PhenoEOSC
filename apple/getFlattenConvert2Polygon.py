import json
import math

# Załadowanie pliku JSON
with open('oznaczone_jablka_flatten_merged/merged.json') as f:
    data = json.load(f)

output_data = {}

# Konwersja elipsy na wielokąt
for filename, file_data in data.items():
    output_data[filename] = {
        "fileref": "",
        "size": file_data['size'],
        "filename": file_data['filename'],
        "base64_img_data": "",
        "file_attributes": file_data.get('file_attributes', {}),
        "regions": {}
    }

    for idx, region in enumerate(file_data['regions']):
        shape_attributes = region['shape_attributes']
        if shape_attributes['name'] != 'circle':
            continue

        cx = shape_attributes['cx']
        cy = shape_attributes['cy']
        r = shape_attributes['r']

        # Obliczanie punktów wielokąta
        all_points_x = []
        all_points_y = []
        for theta in range(0, 360, 5):  # zmień 10 na mniejszą wartość, aby uzyskać więcej punktów
            theta_rad = math.radians(theta)
            x = cx + r * math.cos(theta_rad)
            y = cy + r * math.sin(theta_rad)
            all_points_x.append(int(x))
            all_points_y.append(int(y))

        output_data[filename]['regions'][str(idx)] = {
            "shape_attributes": {
                "name": "polygon",
                "all_points_x": all_points_x,
                "all_points_y": all_points_y
            },
            "region_attributes": region.get('region_attributes', {})
        }

# Zapisywanie wynikowego pliku JSON
with open('oznaczone_jablka_flatten_merged/merged-converted.json', 'w') as f:
    json.dump(output_data, f, indent=4)
