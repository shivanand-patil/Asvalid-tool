# Asvalid Tool

- Asvalid is a tool that helps validate static Aerospike configuration file(.conf) and validates it against aerospike's configuration schema.
- Asvalid also helps compare dynamic configuration values from a running node to the values mentioned in static configuration file. 
- It helps identify any inconsistencies between the dynamic runtime configuration and the static configuration file.


## Use Cases

```bash
Options:
	asvalid compare                          Generate and compare dynamic configuration values with aerospike.conf
	asvalid validate <file>                  Validate a configuration file against the Aerospike schema.
	asvalid verify                           Validate the configuration file against the Aerospike schema and then compare it.
```

