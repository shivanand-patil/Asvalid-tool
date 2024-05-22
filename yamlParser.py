import yaml
import json

def convert_to_str(obj):
    """
    Recursively convert all values in a dictionary or list to strings.
    
    Args:
        obj (dict or list): The input dictionary or list to be converted.
        
    Returns:
        dict or list: The converted dictionary or list with all values as strings.
    """
    if isinstance(obj, dict):
        return {str(k): convert_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_str(item) for item in obj]
    elif isinstance(obj, bool):  # Handle boolean values separately
        return str(obj).lower()
    else:
        return str(obj)

def load_yaml_config(file_path):
    """
    Load a YAML configuration file into a Python dictionary.
    
    Args:
        file_path (str): The path to the YAML configuration file.
        
    Returns:
        dict: The loaded configuration as a dictionary.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load the YAML configuration
config_path = '/opt/asvalid/aerospike.yaml'
aerospike_config = load_yaml_config(config_path)

# Extract namespaces
namespaces = aerospike_config.pop('namespaces', [])
namespaces_dict = {ns['name']: ns for ns in namespaces}
aerospike_config['namespaces'] = namespaces_dict

# Extracting and sorting IPs without ports for cluster-nodes
if 'network' in aerospike_config and 'heartbeat' in aerospike_config['network'] and 'mesh-seed-address-ports' in aerospike_config['network']['heartbeat']:
    ips = [ip.split(':')[0] for ip in aerospike_config['network']['heartbeat']['mesh-seed-address-ports']]
    aerospike_config['cluster-nodes'] = sorted(set(ips))  # Remove duplicates and sort

# Convert all values to strings
aerospike_config_str = convert_to_str(aerospike_config)

# Output JSON
with open('/opt/asvalid/baseline.json', 'w') as f:
    json.dump(aerospike_config_str, f, indent=4)
