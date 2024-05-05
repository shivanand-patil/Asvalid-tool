#!/bin/bash

# Directory to store output files of the compareConfig.py
output_directory="/etc/aerospike/conf_change_history"
base_path="/usr/local/bin"

# Create the output directory if it does not exist
mkdir -p "$output_directory"

# Run createYaml.sh
$base_path/createYaml.sh
if [ $? -ne 0 ]; then
  echo "Failed to run createYaml.sh"
  exit 1
fi

# Run yamlParser.py using Python interpreter
python3 $base_path/yamlParser.py
if [ $? -ne 0 ]; then
  echo "Failed to run yamlParser.py"
  exit 1
fi

# Run generateDynamicConf.py using Python interpreter
python3 $base_path/generateDynamicConf.py
if [ $? -ne 0 ]; then
  echo "Failed to run generateDynamicConf.py"
  exit 1
fi

# Run compareConfig.py using Python interpreter and capture its output
output=$(python3 $base_path/compareConfig.py)
if [ $? -ne 0 ]; then
  echo "Failed to run compareConfig.py"
  exit 1
fi

# Display the output
echo "$output"

# Save the output to a file only if it is not empty
if [ ! -z "$output" ]; then
  output_file="${output_directory}/$(date +"%Y-%m-%d_%H-%M-%S").txt"
  echo "$output" > "$output_file"
  echo "Output stored in $output_file"
else
  echo "No output to save."
fi


