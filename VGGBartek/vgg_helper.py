import base64
import json
def is_json_structure_with_0_1_2_3(json_string_b64):
    decoded_str = base64.b64decode(json_string_b64).decode('utf-8')
    json_dict = json.loads(decoded_str)

    # Get the first key
    first_key = next(iter(json_dict))

    # Check the type of the 'regions' field
    regions_type = type(json_dict[first_key]['regions'])

    if regions_type is dict:
        return True
    elif regions_type is list:
        return False
    else:
        return 'Unknown structure'

def convert_json_to_structure_with_0_1_2_3(input_base64):
    # Dekoduj base64 string do normalnego stringu
    decoded_str = base64.b64decode(input_base64).decode('utf-8')

    # Wczytaj string jako JSON
    data = json.loads(decoded_str)

    # Iteruj przez każdy klucz w głównym obiekcie
    for key in data:
        # Sprawdź, czy 'regions' jest listą
        if type(data[key]['regions']) is list:
            # Konwertuj listę 'regions' na słownik
            data[key]['regions'] = {i: value for i, value in enumerate(data[key]['regions'])}

    # Konwertuj dane z powrotem na string JSON
    json_str = json.dumps(data, indent=4)

    # Koduj string JSON do base64
    output_base64 = base64.b64encode(json_str.encode('utf-8'))

    # Zwróć base64 string
    return output_base64.decode('utf-8')
