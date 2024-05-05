import argparse
import subprocess
import re
import psutil

def get_configured_nodes(conf_path):
    with open(conf_path, 'r') as file:
        conf_content = file.read()
    seed_nodes = re.findall(r'^(?!#).*mesh-seed-address-port\s+(\d+\.\d+\.\d+\.\d+)\s+\d+', conf_content, re.MULTILINE)
    return set(seed_nodes)

def get_online_nodes():
    result = subprocess.run(['asadm', '-e', 'info'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Failed to execute asadm: " + result.stderr)
    online_nodes = re.findall(r'(\d+\.\d+\.\d+\.\d+):\d+', result.stdout)
    return set(online_nodes)

def check_memory_allocation(conf_path):
    with open(conf_path, 'r') as file:
        conf_content = file.read()
    data_sizes = re.findall(r'^(?!#).*storage-engine memory\s*{\s*data-size (\d+)([KMG])', conf_content, re.IGNORECASE | re.MULTILINE)
    total_allocated_memory = 0
    for size, unit in data_sizes:
        size = int(size)
        if unit.upper() == 'K':
            size *= 1024
        elif unit.upper() == 'M':
            size *= 1024**2
        elif unit.upper() == 'G':
            size *= 1024**3
        total_allocated_memory += size
    total_system_memory = psutil.virtual_memory().total
    total_allocated_memory_gib = total_allocated_memory / (1024**3)
    total_system_memory_gib = total_system_memory / (1024**3)
    if total_allocated_memory > total_system_memory:
        print(f"Warning: Total configured data-size ({total_allocated_memory_gib:.2f} GiB) exceeds system memory ({total_system_memory_gib:.2f} GiB)")

def main():
    parser = argparse.ArgumentParser(description='Check Aerospike cluster configuration and system status.')
    parser.add_argument('conf_path', type=str, help='Path to the Aerospike configuration file')
    args = parser.parse_args()

    conf_path = args.conf_path
    configured_nodes = get_configured_nodes(conf_path)
    online_nodes = get_online_nodes()
    missing_nodes = configured_nodes.difference(online_nodes)
    if missing_nodes:
        print("Warning: The following nodes are configured but not participating in the cluster:")
        for node in missing_nodes:
            print(node)
    else:
        print("All configured nodes are participating in the cluster.")
    check_memory_allocation(conf_path)

if __name__ == '__main__':
    main()
