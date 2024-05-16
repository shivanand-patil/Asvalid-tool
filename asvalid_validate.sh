#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <config_file>"
    exit 1
fi

python3 "$(dirname "$(realpath "$0")")/validate.py" "$1"

if [ $? -ne 0 ]; then
    echo "Structure not good, asvalid encountered errors. Exiting...."
    exit 1
fi

file_path="$1"

version=$(asd --version | awk '{print $5}' )

echo "Evaluating $file_path against version $version config schema."

if asconfig validate --aerospike-version "$version" "$file_path"; then
   	
	echo "Validation successful for Aerospike version $version"
else
  	echo "Validation failed for Aerospike version $version"
	exit 1
fi
