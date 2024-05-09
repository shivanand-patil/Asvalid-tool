import subprocess
import json

def run_asinfo_command(command):
    """ Run the asinfo command with specified parameters and return the output. """
    try:
        result = subprocess.check_output(['asinfo', '-v', command], text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to run command {command}: {e}")
        return None

def parse_info_to_dict(info_str):
    """ Convert asinfo string output to a nested dictionary based on prefixes,
        supporting multiple values for the same keys. """
    info_dict = {}
    for pair in info_str.split(';'):
        if '=' in pair:
            key, value = pair.split('=', 1)
            key_parts = key.strip().split('.')
            sub_dict = info_dict
            # Traverse/create sub-dictionaries except for the last part
            for part in key_parts[:-1]:
                if part not in sub_dict or not isinstance(sub_dict[part], dict):
                    sub_dict[part] = {}
                sub_dict = sub_dict[part]
            # Handle the last key part
            last_key_part = key_parts[-1]
            # Special handling for storage-engine
            if last_key_part == "storage-engine":
                storage_engine_type = value.strip().split('/')[-1]  # Extracting the last part after splitting by '/'
                sub_dict[last_key_part] = {"type": storage_engine_type}
            elif last_key_part in sub_dict:
                existing_value = sub_dict[last_key_part]
                if isinstance(existing_value, list):
                    # If it's already a list, append to it
                    existing_value.append(value.strip())
                else:
                    # If it's not a list, create a new list with the old and new value
                    sub_dict[last_key_part] = [existing_value, value.strip()]
            else:
                # If the key does not exist, just set it
                sub_dict[last_key_part] = value.strip()
    return info_dict

def get_cluster_config():
    """ Get the entire cluster configuration and return it as a dictionary. """
    config = {}

    # Get service configuration
    service_info = run_asinfo_command('get-config:context=service')
    if service_info:
        config['service'] = parse_info_to_dict(service_info)

    # Get network configuration
    network_info = run_asinfo_command('get-config:context=network')
    if network_info:
        config['network'] = parse_info_to_dict(network_info)

    # Get namespaces and their configuration
    namespaces_info = run_asinfo_command('namespaces')
    if namespaces_info:
        namespaces = namespaces_info.split(';')
        config['namespaces'] = {}
        for namespace in namespaces:
            namespace_config = run_asinfo_command(f'get-config:context=namespace;id={namespace}')
            if namespace_config:
                config['namespaces'][namespace] = parse_info_to_dict(namespace_config)

    return config

def main():
    # Retrieve configuration
    cluster_config = get_cluster_config()

    # Convert to JSON string
    json_data = json.dumps(cluster_config, indent=4)

    # Output to a file
    with open('/opt/asvalid/dynamic_config.json', 'w') as file:
        file.write(json_data)

if __name__ == "__main__":
    main()

