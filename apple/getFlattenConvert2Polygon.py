import json
import math

def convert_circle_to_polygon(input_path, output_path, angle_step=1):
    # Załadowanie pliku JSON
    with open(input_path) as f:
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
            points = set()  # Zbiór par punktów

            for theta in range(0, 360, angle_step):
                theta_rad = math.radians(theta)
                x = cx + r * math.cos(theta_rad)
                y = cy + r * math.sin(theta_rad)
                points.add((int(x), int(y)))

            all_points_x, all_points_y = zip(*points)  # Rozpakowanie par do osobnych tablic

            output_data[filename]['regions'][str(idx)] = {
                "shape_attributes": {
                    "name": "polygon",
                    "all_points_x": list(all_points_x),
                    "all_points_y": list(all_points_y)
                },
                "region_attributes": region.get('region_attributes', {})
            }

    # Zapisywanie wynikowego pliku JSON
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=4)
