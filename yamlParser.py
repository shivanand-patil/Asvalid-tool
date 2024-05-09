import yaml
import json

def convert_to_str(obj):
    if isinstance(obj, dict):
        return {str(k): convert_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_str(item) for item in obj]
    elif isinstance(obj, bool):  # Handle boolean values separately
        return str(obj).lower()
    else:
        return str(obj)

# Function to load a YAML configuration file into a Python dictionary
def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load the YAML configuration
config_path = '/opt/asvalid/aerospike.yaml'  # Path to your aerospike.conf file
aerospike_config = load_yaml_config(config_path)

# Extract namespaces
namespaces = aerospike_config.pop('namespaces', [])

# Convert namespaces list to a dictionary
namespaces_dict = {ns['name']: ns for ns in namespaces}

# Update aerospike_config with modified namespaces dictionary
aerospike_config['namespaces'] = namespaces_dict

# Convert all values to strings and enclose them in double quotes
aerospike_config_str = convert_to_str(aerospike_config)

# Open a file where you want to store the output in double-quoted JSON format
with open('/opt/asvalid/baseline.json', 'w') as f:
    # Dump the dictionary to a file with JSON formatting, ensuring it's pretty-printed
    json.dump(aerospike_config_str, f, indent=4)
