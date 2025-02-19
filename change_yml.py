import ruamel.yaml
from input_data import list_of_inputs  # Importing the input data from input_data.py
import argparse
import os

yaml = ruamel.yaml.YAML()  
yaml.preserve_quotes = True

def update_nested_dict(d, keys, value):
    """
    Recursively updates the value of a nested dictionary key.
    """
    if isinstance(d, dict) and keys:
        key = keys[0]
        if len(keys) == 1 and key in d:
            d[key] = value
            return True
        elif key in d:
            return update_nested_dict(d[key], keys[1:], value)
    return False

def modify_yaml_document(yaml_content, key, new_value):
    """
    Modifies the specified key in the YAML document.
    """
    keys = tuple(key.split("."))  # Split the key path into individual keys
    modified = False
    for doc in yaml_content:
        if isinstance(doc, dict):
            if update_nested_dict(doc, keys, new_value):
                modified = True
    return yaml_content, modified

def modify_yaml_file(file_path, key, new_value):
    """
    Modifies the YAML file at the given path by updating the specified key's value.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Skipping.")
        return  # Skip if the file doesn't exist

    try:
        with open(file_path, 'r') as file:
            yaml_content = list(yaml.load_all(file))  # Load all YAML documents

        yaml_content, modified = modify_yaml_document(yaml_content, key, new_value)

        if modified:
            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                yaml.dump_all(yaml_content, file)
            print(f"Modifying file: {file_path} with key: {key}")
        else:
            print(f"Key '{key}' not found in file: {file_path}. Skipping.")

    except ruamel.yaml.YAMLError as e:
        print(f"Error processing file {file_path}: {e}. Skipping.")
    except Exception as e:
        print(f"Unexpected error occurred with file {file_path}: {e}. Skipping.")

def main(scale_type):
    # Iterate through the list_of_inputs and apply the changes
    for input_item in list_of_inputs:
        file_path = input_item["filepath"]
        key = input_item["key"]

        # Select the appropriate replica count based on the scale_type
        new_value = input_item[f"{scale_type}_replicas_count"]

        modify_yaml_file(file_path, key, new_value)

    print("Modification complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modify YAML files with scale-up or scale-down values.")
    parser.add_argument("--scale-type", choices=["scale_up", "scale_down"], required=True,
                        help="Specify whether to scale up or scale down replicas.")

    args = parser.parse_args()

    # Call the main function with the selected scale type (either 'scale_up' or 'scale_down')
    main(args.scale_type)
