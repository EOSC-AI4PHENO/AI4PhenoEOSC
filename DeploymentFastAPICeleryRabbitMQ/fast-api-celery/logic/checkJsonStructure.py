import json
import base64
import Convert2Polygon

def read_json_file(json_filepath):
    """
    Wczytuje plik JSON i zwraca jego zawartość jako obiekt Pythona.
    """
    with open(json_filepath, 'r') as f:
        data = json.load(f)
    return data

def encode_to_base64(data):
    """
    Zakodowuje dane JSON do formatu Base64.
    """
    data_str = json.dumps(data)
    data_bytes = data_str.encode('utf-8')
    base64_encoded = base64.b64encode(data_bytes)
    return base64_encoded


def is_json_structure_shouldbe_converted(base64_encoded_json_data):
    # Dekodowanie danych z Base64
    decoded_json_str = base64.b64decode(base64_encoded_json_data).decode('utf-8')

    # Konwersja dekodowanego ciągu znaków na słownik Pythona
    json_data = json.loads(decoded_json_str)

    # Odczytanie głównego klucza
    main_key = list(json_data.keys())[0]
    json_data = json_data[main_key]

    regions = json_data['regions']

    # Sprawdzenie, czy "regions" jest słownikiem
    if isinstance(regions, dict):
        return False

    # Sprawdzenie, czy "regions" jest listą
    elif isinstance(regions, list):
        return True

    # Zwróć None, jeśli "regions" nie jest ani słownikiem, ani listą
    else:
        return None


json_filepath_slownik = 'D:/!Dysk_E_Firma/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/linden/LindenClassification/2023-08-05/ODUPP_2022.06.28.05.54.35._json.json'
json_filepath_lista = 'C:/Users/kurekj/Desktop/file_roi.json'


# Wczytanie pliku JSON
data_slownik = read_json_file(json_filepath_slownik)
data_lista = read_json_file(json_filepath_lista)

# Kodowanie danych do Base64
base64_encoded_slownik = encode_to_base64(data_slownik)
base64_encoded_lista = encode_to_base64(data_lista)

#wynik_slownik=is_json_structure_with_indx_integer(base64_encoded_slownik)
#wynik_lista=is_json_structure_with_indx_integer(base64_encoded_lista)

#print(wynik_slownik)
#print(wynik_lista)

jsonfile_base64_slownik=Convert2Polygon.Convert2Polygon2(base64_encoded_slownik, 2048, 2048)
jsonfile_base64_lista=Convert2Polygon.Convert2Polygon2(base64_encoded_lista, 2048, 2048)

Convert2Polygon.base64_to_jsonfile(jsoncontent_base64=jsonfile_base64_slownik,outputfilename="d:/jsonfile_base64_slownik.json")
Convert2Polygon.base64_to_jsonfile(jsoncontent_base64=jsonfile_base64_lista,outputfilename="d:/jsonfile_base64_lista.json")

