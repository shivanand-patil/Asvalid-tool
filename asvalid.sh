#!/bin/bash

# Display description only when no arguments are provided
if [ $# -eq 0 ]; then
    echo "Usage: asvalid [option] [arguments]"
    echo "Options:"
    echo "  compare             Generates and  Compare dynamic configuration values with aerospike.conf "
    echo "  validate <file>     Validate a configuration file against the Aerospike schema."
    exit 0
fi

# Check if the first argument is "compare"
if [ "$1" == "compare" ]; then
    # Execute asvalid compare
    bash /usr/local/bin/asvalid_compare.sh
elif [ "$1" == "validate" ]; then
    # Check if the number of arguments is correct for "validate"
    if [ $# -ne 2 ]; then
        echo "Usage: asvalid validate <file>"
        exit 1
    fi
    # Execute asvalid validate <file>
    bash /usr/local/bin/asvalid_validate.sh "$2"
else
    echo "Invalid option: $1"
    exit 1
fi

