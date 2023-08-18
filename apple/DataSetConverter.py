import os
import genFlattenRandomSplit1
import genFlattenProcess

#folderInput = 'oznaczone_jablka_flatten_oryg_input'
folderInput = 'oznaczone_jablka_2023_08_18'
train_dir, val_dir, test_dir = genFlattenRandomSplit1.split_data1(folderInput, 0.7, 0.15, 0.15)

genFlattenProcess.process_json_files(train_dir)
genFlattenProcess.process_json_files(val_dir)
genFlattenProcess.process_json_files(test_dir)
