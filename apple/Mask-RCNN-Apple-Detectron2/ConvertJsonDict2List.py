import base64
import json

def ConvertJsonDict2ListJarek(json_file: str):
    data = json.loads(json_file)
    photos = data.keys()
    for photo in photos:
        one_photo = data[photo]
        regions = one_photo['regions']
        new_regions = {}  # utworzenie nowego słownika
        for i, region in enumerate(regions):
            shape_attributes = region['shape_attributes']
            name = shape_attributes['name']
            new_regions[str(i)] = region  # dodajemy region do nowego słownika
        one_photo['regions'] = new_regions  # zastępujemy starą listę nowym słownikiem
    json_out = json.dumps(data)
    return json_out