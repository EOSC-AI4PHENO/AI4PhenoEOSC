import os
import json
import shutil
import pandas as pd
from PIL import Image


def copy_jpg_and_json(input_dir):
    # Create output directory
    modified_input_dir = input_dir.replace("/", "_")
    output_dir = f"{modified_input_dir}_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Lists for tracking unused files
    unused_images = set()
    unused_jsons = set()

    for subdir, _, files in os.walk(input_dir):
        # Skip the 'Wide' subdirectory
        if 'Wide' in subdir.split(os.sep):
            continue

        for file in files:
            # Skip files with 'roi' in their name
            if 'roi' in file.lower():
                continue

            # Handle JSON files
            if file.endswith('.json'):
                json_path = os.path.join(subdir, file)
                with open(json_path, 'r') as jf:
                    data = json.load(jf)

                for key, value in data.items():
                    filename = value['filename']
                    ext = filename.split('.')[-1].lower()

                    if ext in ['jpg', 'jpeg', 'png']:
                        image_path = os.path.join(subdir, filename)

                        if not os.path.exists(image_path):
                            unused_jsons.add(json_path)
                            continue

                        # Convert PNG to JPG if necessary
                        if ext == "png":
                            img = Image.open(image_path)
                            if img.mode in ('RGBA', 'LA'):
                                background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
                                background.paste(img, img.split()[-1])
                                img = background
                            filename = filename.rsplit('.', 1)[0] + ".jpg"
                            image_path_new = os.path.join(subdir, filename)
                            img.save(image_path_new, "JPEG")
                            image_path = image_path_new

                        parent_folder_name = subdir.split(os.sep)[-1]
                        new_filename = parent_folder_name + "_" + filename

                        shutil.copy2(image_path, os.path.join(output_dir, new_filename.lower()))

                        # Update JSON data to reflect the new filename
                        data[key]['filename'] = new_filename.lower()
                        new_json_filename = parent_folder_name + "_" + file

                        with open(os.path.join(output_dir, new_json_filename), 'w') as jf_out:
                            json.dump(data, jf_out, indent=4)

                        unused_images.discard(image_path)
                        unused_jsons.discard(json_path)
                    else:
                        unused_images.add(os.path.join(subdir, filename))

            elif any(file.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                unused_images.add(os.path.join(subdir, file))

    # Export statistics to Excel
    max_len = max(len(unused_images), len(unused_jsons))
    df = pd.DataFrame({
        'Unused Images': list(unused_images) + [''] * (max_len - len(unused_images)),
        'Unused JSONs': list(unused_jsons) + [''] * (max_len - len(unused_jsons))
    })

    df.to_excel(os.path.join(output_dir, 'statistics.xlsx'), index=False)


# Example usage:
copy_jpg_and_json('images/0700F133_Golden3')
copy_jpg_and_json('images/0700F136_Gala3')
copy_jpg_and_json('images/Apple_DataSet_1')
copy_jpg_and_json('images/Apple_DataSet_2')
copy_jpg_and_json('images/Apple_DataSet_3')
copy_jpg_and_json('oznaczone_jablka')
copy_jpg_and_json('Photos_Jabłonie_Gala')
copy_jpg_and_json('Photos_Jabłonie_Golden')
copy_jpg_and_json('Przybroda')
