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

