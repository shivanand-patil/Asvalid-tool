# Asvalid Tool

- Asvalid is a tool that helps validate static Aerospike configuration and compare dynamic configuration values from a running node to the static aerospike.conf file. 
- It helps identify any inconsistencies between the dynamic runtime configuration and the static configuration file.


## Use Cases

```bash
Usage: asvalid [option] [arguments]
Options:
  compare                          Generate and compare dynamic configuration values with aerospike.conf
  validate <file>                  Validate a configuration file against the Aerospike schema.
  verify                           Validate the configuration file against the Aerospike schema and then compare it.
```

