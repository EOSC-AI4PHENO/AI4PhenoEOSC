import os
import genFlattenCleared
import genFlattenValidation1
import getFlattenMerge
import getFlattenConvert2Polygon
import getFlattenConvert2PolygonBartek1


def process_json_files(input_folder):
    print('Before clearing')
    genFlattenValidation1.validation_json_files1(input_folder)
    genFlattenCleared.clearing_json_files(input_folder)
    print('After clearing')
    genFlattenValidation1.validation_json_files1(input_folder)
    print('Merging')
    getFlattenMerge.merge_json_files(input_folder)
    print('Convertion Elipse to Polygon')

    filepathIN = os.path.join(input_folder, 'merged.json')
    filepathOUT = os.path.join(input_folder, 'via_region_data.json')
    getFlattenConvert2PolygonBartek1.convert_circle_to_polygon(filepathIN, filepathOUT)
