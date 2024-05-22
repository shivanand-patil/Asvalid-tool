import json

def load_json(file_path):
    """
    Load JSON data from a file.
    
    Args:
        file_path (str): The path to the JSON file.
        
    Returns:
        dict: The loaded JSON data as a dictionary.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_json(json1, json2, path=""):
    """
    Compare two JSON objects and find differences.
    
    Args:
        json1 (dict): The first JSON object.
        json2 (dict): The second JSON object.
        path (str): The current path within the JSON objects (used for nested keys).
        
    Returns:
        list: A list of differences between the JSON objects.
    """
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
           difference_description = f"{full_path}:\n"\
                         f"\t- aerospike.conf = {json1[key]}\n"\
                         f"\t- live cluster value = {json2[key]}"
           differences.append(difference_description)
    return differences

# Paths to JSON files
file1_path = '/opt/asvalid/baseline.json'
file2_path = '/opt/asvalid/dynamic_config.json'

# Load JSON data from files
json1 = load_json(file1_path)
json2 = load_json(file2_path)

# Compare the JSON data
differences = compare_json(json1, json2)

# Print the differences in a concise format
if differences:
    print("Configuration differences found:")
    for diff in differences:
        print(diff)
else:
    print("No differences found between static and dynamic values")
