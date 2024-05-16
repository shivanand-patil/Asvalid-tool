#!/bin/bash

# Function to display usage
display_usage() {
    echo "Usage: asvalid [option] [arguments]"
    echo "Options:"
    echo "	asvalid validate <file>                  Validate a configuration file against the Aerospike schema"
    echo "	asvalid verify                           Validate and compare live cluster values to static conf values"
}

# Function to validate a configuration file
validate_config() {
    local config_file="$1"
    if [ ! -f "$config_file" ]; then
        echo "Error: Configuration file '$config_file' not found"
        exit 1
    fi
    # Execute asvalid validate <file>
    bash /usr/local/bin/asvalid-tool/asvalid_validate.sh "$config_file"
}

# Function to compare configuration values
compare_config() {
    # Execute asvalid compare and capture its output
    local output=$(bash /usr/local/bin/asvalid-tool/asvalid_compare.sh)
    echo "$output"
    if [ $? -eq 0 ] && [ ! -z "$output" ]; then
        log_output "$output"
    fi
}

# Function to log output with timestamps
log_output() {
    local log_file="/opt/asvalid/asvalid.log"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    # Add timestamp to each line of the output
    while IFS= read -r line; do
        echo "[$timestamp] $line" >> "$log_file"
    done <<< "$1"
}

# Display usage if no arguments provided
if [ $# -eq 0 ]; then
    display_usage
    exit 0
fi

# Check options
case "$1" in
    validate)
        if [ $# -ne 2 ]; then
            echo "Error: Missing argument for 'validate'"
            display_usage
            exit 1
        fi
        validate_config "$2"
        ;;
    verify)
        validate_config "/etc/aerospike/aerospike.conf"
        # Check if validation was successful
        if [ $? -eq 0 ]; then
            compare_config
        else
            echo "Validation failed, cannot proceed with comparison"
            log_output "Validation failed, cannot proceed with comparison"
            exit 1
        fi
        ;;
    *)
        echo "Error: Invalid option '$1'"
        display_usage
        exit 1
        ;;
esac

exit 0

