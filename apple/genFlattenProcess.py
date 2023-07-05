import os
import genFlattenCleared
import genFlattenValidation
import getFlattenMerge
import getFlattenConvert2Polygon

def process_json_files(input_folder):
    print('Before clearing')
    genFlattenValidation.validation_json_files(input_folder)
    genFlattenCleared.clearing_json_files(input_folder)
    print('After clearing')
    genFlattenValidation.validation_json_files(input_folder)
    print('Merging')
    getFlattenMerge.merge_json_files(input_folder)
    print('Convertion Elipse to Polygon')

    filepathIN = os.path.join(input_folder, 'merged.json')
    filepathOUT = os.path.join(input_folder, 'via_region_data.json')
    getFlattenConvert2Polygon.convert_circle_to_polygon(filepathIN, filepathOUT, angle_step=1)
