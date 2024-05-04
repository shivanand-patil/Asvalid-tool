import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_json(json1, json2, path=""):
    differences = []
    # Compare only keys that exist in both dictionaries
    common_keys = json1.keys() & json2.keys()
    for key in common_keys:
        full_path = f"{path}{key}"  # Create a full path for the current key
        if isinstance(json1[key], dict) and isinstance(json2[key], dict):
            # Recurse into nested dictionaries
            deeper_diff = compare_json(json1[key], json2[key], full_path + ".")
            if deeper_diff:
                differences.extend(deeper_diff)
        elif json1[key] != json2[key]:
            # Base case: differing values
            difference_description = f"{full_path}: > {json1[key]} < {json2[key]}"
            differences.append(difference_description)
    return differences

# Paths to JSON files
file1_path = '/etc/aerospike/baseline.json'
file2_path = '/etc/aerospike/dynamic_config.json'

# Load JSON data from files
json1 = load_json(file1_path)
json2 = load_json(file2_path)

# Compare the JSON data
differences = compare_json(json1, json2)

# Print the differences in a concise format
if differences:
    print("Differences found:")
    for diff in differences:
        print(diff)

