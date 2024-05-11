# Asvalid Tool

- Asvalid is a tool that helps validate static Aerospike configuration file(.conf) and validates it against aerospike's configuration schema.
- Asvalid also helps compare dynamic configuration values from a running node to the values mentioned in static configuration file. 
- It helps identify any inconsistencies between the dynamic runtime configuration and the static configuration file.


## Use Cases

```bash
Options:
	asvalid validate <file>                  Validate a configuration file against the Aerospike schema
	asvalid compare                          Generate and compare dynamic configuration values with aerospike.conf
	asvalid verify                           Validates the configuration file against the Aerospike schema
 					         and then compares its static values to values from running node
```

# Examples

1. asvalid validate 'file-path'
```bash
	root@VM-1:/home/ubuntu# asvalid validate /etc/aerospike/aerospike.conf

	Warning: Total configured data-size and memory-size (8.00 GiB) exceeds system memory (0.94 GiB)
	Warning: No TLS configuration block found.
	Configuration check complete.
	Evaluating /etc/aerospike/aerospike.conf against version 7.0.0.7 config schema.
	Validation successful for Aerospike version 7.0.0.7.
```

2. asvalid compare
```bash
	root@VM-1:/home/ubuntu# asvalid compare

	Configuration differences found:
	service.proto-fd-max:
		- aerospike.conf = 15000
		- live cluster value = 1500
	namespaces.test-new.replication-factor:
		- aerospike.conf = 2
		- live cluster value = 6
	Output stored in /opt/asvalid/conf_change_history/2024-05-12_02-25-43.txt
```

3. asvalid verify
```bash
	root@VM-1:/home/ubuntu# asvalid verify

	Warning: Total configured data-size and memory-size (8.00 GiB) exceeds system memory (0.94 GiB)
	Warning: No TLS configuration block found.
	Configuration check complete.
	Evaluating /etc/aerospike/aerospike.conf against version 7.0.0.7 config schema.
	Validation successful for Aerospike version 7.0.0.7.

	Configuration differences found:
	namespaces.test-new.replication-factor:
		- aerospike.conf = 2
		- live cluster value = 6
	service.proto-fd-max:
		- aerospike.conf = 15000
		- live cluster value = 1500
	Output stored in /opt/asvalid/conf_change_history/2024-05-12_02-27-15.txt
