import os
import json
import shutil


def copy_jpg_and_json(input_dir: str):
    """
    Copies jpg files and their associated json files from an input directory to an output directory.
    In the copied json, keeps only those entries with a "filename" that points to an existing jpg.
    Both filenames will be prefixed by the combined folder's name.
    The output directory will be the input directory with "_output" appended.

    Parameters:
    - input_dir: Directory containing the json and jpg files.
    """

    output_dir = f"{input_dir}_output"

    # Remove the output directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Ensure the output directory exists
    os.makedirs(output_dir)

    parent_folder_name = os.path.basename(input_dir)

    # Traverse the directory recursively
    for dirpath, _, filenames in os.walk(input_dir):
        relative_path = os.path.relpath(dirpath, input_dir)
        folder_prefix = f"{parent_folder_name}_{relative_path.replace(os.sep, '_')}"

        for filename in filenames:
            # If the file is a json
            if filename.endswith('.json'):
                with open(os.path.join(dirpath, filename), 'r') as f:
                    data = json.load(f)

                    valid_entries = {}

                    # Iterate through each entry in the json
                    for key, item in data.items():
                        jpg_filename = item.get('filename', '')

                        # If there's a jpg file associated and it exists
                        if jpg_filename.endswith('.jpg') and os.path.exists(os.path.join(dirpath, jpg_filename)):
                            new_jpg_filename = f"{folder_prefix}_{jpg_filename}"
                            item['filename'] = new_jpg_filename
                            valid_entries[key] = item
                            shutil.copy2(os.path.join(dirpath, jpg_filename),
                                         os.path.join(output_dir, new_jpg_filename))

                    # Continue only if there are valid entries
                    if valid_entries:
                        new_json_filename = f"{folder_prefix}_{filename}"
                        json_output_path = os.path.join(output_dir, new_json_filename)
                        counter = 1
                        while os.path.exists(json_output_path):
                            base, ext = os.path.splitext(new_json_filename)
                            json_output_path = os.path.join(output_dir, f"{base}_{counter}{ext}")
                            counter += 1

                        # Write only valid entries to the new json file
                        with open(json_output_path, 'w') as outfile:
                            json.dump(valid_entries, outfile, indent=4)

    print("Process completed!")

# Usage
copy_jpg_and_json('images/0700F133_Golden3')
copy_jpg_and_json('images/0700F136_Gala3')
copy_jpg_and_json('images/Apple_DataSet_1')
copy_jpg_and_json('images/Apple_DataSet_2')
copy_jpg_and_json('images/Apple_DataSet_3')
copy_jpg_and_json('oznaczone_jablka')
copy_jpg_and_json('Photos_Jabłonie_Gala')
copy_jpg_and_json('Photos_Jabłonie_Golden')
copy_jpg_and_json('Przybroda')