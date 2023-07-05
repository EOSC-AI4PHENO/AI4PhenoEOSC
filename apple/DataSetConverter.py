import os
import genFlattenRandomSplit
import genFlattenProcess

folderInput = 'oznaczone_jablka_flatten_oryg_input'
train_dir, val_dir, test_dir = genFlattenRandomSplit.split_data('oznaczone_jablka_flatten_oryg_input', 0.7, 0.15, 0.15)

genFlattenProcess.process_json_files(train_dir)
genFlattenProcess.process_json_files(val_dir)
genFlattenProcess.process_json_files(test_dir)
