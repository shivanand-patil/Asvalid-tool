import sys
import argparse
import subprocess
import re
import psutil
import os

def parse_memory_size(size, unit):
    size = int(size)
    if unit.upper() == 'K':
        return size * 1024
    elif unit.upper() == 'M':
        return size * 1024**2
    elif unit.upper() == 'G':
        return size * 1024**3
    else:
        raise ValueError(f"Unrecognized unit '{unit}'")

def check_memory_allocation(conf_path):
    with open(conf_path, 'r') as file:
        conf_content = file.read()
    size_patterns = re.findall(r'^(?!#).*\b(data-size|memory-size)\s+(\d+)([KMG])', conf_content, re.IGNORECASE | re.MULTILINE)
    total_allocated_memory = 0
    for param, size, unit in size_patterns:
        try:
            total_allocated_memory += parse_memory_size(size, unit)
        except ValueError as e:
            print(f"Error: {e}")
    total_system_memory = psutil.virtual_memory().total
    total_allocated_memory_gib = total_allocated_memory / (1024**3)
    total_system_memory_gib = total_system_memory / (1024**3)
    if total_allocated_memory > total_system_memory:
        print(f"Warning: Total configured data-size and memory-size ({total_allocated_memory_gib:.2f} GiB) exceeds system memory ({total_system_memory_gib:.2f} GiB)")

def parse_config(file_path):
    with open(file_path, 'r') as file:
        config_lines = file.readlines()

    section_stack = []
    namespace_count = 0
    namespace_names = set()
    warnings = []
    logging_paths = []
    tls_config_found = False
    namespace_rep_factors = {}

    for line_number, line in enumerate(config_lines, start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.endswith('{'):
            section = line.split()[0]
            section_stack.append((section, line_number))
            if section == 'tls':
                tls_config_found = True
        elif line.endswith('}'):
            if not section_stack:
                warnings.append(f"Warning at line {line_number}: Extra closing curly brace '}}'.")
            else:
                last_section, _ = section_stack.pop()
                if last_section == 'namespace' and current_namespace not in namespace_rep_factors:
                    warnings.append(f"Warning: 'replication-factor' is missing for namespace '{current_namespace}'.")

        if line.startswith('namespace'):
            current_namespace = line.split()[1]
            namespace_count += 1
            if current_namespace in namespace_names:
                warnings.append(f"Warning at line {line_number}: Duplicate namespace '{current_namespace}' found.")
                for warning in warnings:
                    print(warning)
                sys.exit(1)
            namespace_names.add(current_namespace)
        if line.startswith('replication-factor'):
            namespace_rep_factors[current_namespace] = line.split()[1]
        if line.startswith('file'):
            path = line.split()[1]
            logging_paths.append(path)

    if not tls_config_found:
        warnings.append("Warning: No TLS configuration block found.")
    if namespace_count > 32:
        warnings.append("Warning: Total namespaces exceed the maximum limit of 32.")
    if section_stack:
        for section_name, line_number in section_stack:
            warnings.append(f"Warning: Section '{section_name}' opened at line {line_number} is not closed.")
            for warning in warnings:
                print(warning)
            sys.exit(1)

    return warnings, logging_paths

def check_log_drive_conflicts(log_paths):
    system_drive = os.path.splitdrive(sys.executable)[0]
    for path in log_paths:
        if "/log/" in path or path.endswith(".log"):  # Check if path is likely a log file
            if os.path.splitdrive(path)[0] == system_drive:
                print(f"Warning: file {path} is on the system drive.")

def check_storage_device_space(conf_path):
    with open(conf_path, 'r') as file:
        conf_content = file.read()

    # Regular expression to match file and filesize under any storage-engine configuration
    device_configs = re.findall(r'namespace\s+\S+.*?storage-engine \S+.*?file\s+(\S+).*?filesize\s+(\d+)([KMG])', conf_content, re.DOTALL | re.IGNORECASE)

    for file_path, size, unit in device_configs:
        required_space = parse_memory_size(size, unit)
        free_space = psutil.disk_usage(os.path.dirname(file_path)).free
        if required_space > free_space:
            print(f"Warning: Not enough space for {file_path} ({required_space} bytes required, {free_space} bytes available).")

def main():
    parser = argparse.ArgumentParser(description='Check Aerospike cluster configuration and system status.')
    parser.add_argument('conf_path', type=str, help='Path to the Aerospike configuration file')
    args = parser.parse_args()

    check_memory_allocation(args.conf_path)
    warnings, log_paths = parse_config(args.conf_path)
    check_log_drive_conflicts(log_paths)
    check_storage_device_space(args.conf_path)

    if warnings:
        for warning in warnings:
            print(warning)

    print("Configuration check complete.")

if __name__ == '__main__':
    main()
