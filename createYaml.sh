#!/bin/bash

version=$(asd --version | awk '{print $5}' )

asconfig convert --aerospike-version "$version" --output /etc/aerospike/aerospike.yaml /etc/aerospike/aerospike.conf
