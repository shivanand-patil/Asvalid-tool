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
```
## Flow

[![](https://mermaid.ink/img/pako:eNqFk9tq20AQhl9l2CsFkjyAC4XEdgxOWrt1WijoZirN2tNIu2IPLibOu3dPiuM2UF0Iaeebw_-P9Cwa3ZKYiK3BYQePsw-1gnDdVGj32HF7AVdXH4_lBdIdHR3hNnO31RqNpfyC6gDXjVYSJHeUMmFaTXfUPIHUBgY02JMjYy9ywjQhs-p7KQu_2e0AbazB2wLNEvS1mhujjc1nHFpor9rY8gybVyvvBu_GSVmrEC-azqQ0ug_zBCV3OXqXlQCS0XbgJ0pKRmGRV3syDpyGHzefHsBbVtvTrKn7okqhgCw3q8-nXIv7UNjCT7TUsaLrXzbNFeOLlAnLakGKTDShPSjsuUkQSKN7MF6p2C1nNJ23wcTXCVhJHeX0odXo7DJVva-mWWWaJ21lBO4TsCmuwru2viUfRmNblpIMqSaVet_bYBTLwxFWObg6LTjP3JJE3zl46926zMpRNcoo8GyHqVAiv41Dc1nPiQOJ3I0S14l-_N-Hk7Ev_344cXUZ-Uu0uBQ9mR65DT_Oc0Rq4XbUUy0m4bGoq0WtXgKK3unNQTVi4oynS-GH6MSMMfxyvZhI7Ozr6bxlp005fPkDHswngg?type=png)](https://mermaid-live-editor.fly.dev/edit#pako:eNqFk9tq20AQhl9l2CsFkjyAC4XEdgxOWrt1WijoZirN2tNIu2IPLibOu3dPiuM2UF0Iaeebw_-P9Cwa3ZKYiK3BYQePsw-1gnDdVGj32HF7AVdXH4_lBdIdHR3hNnO31RqNpfyC6gDXjVYSJHeUMmFaTXfUPIHUBgY02JMjYy9ywjQhs-p7KQu_2e0AbazB2wLNEvS1mhujjc1nHFpor9rY8gybVyvvBu_GSVmrEC-azqQ0ug_zBCV3OXqXlQCS0XbgJ0pKRmGRV3syDpyGHzefHsBbVtvTrKn7okqhgCw3q8-nXIv7UNjCT7TUsaLrXzbNFeOLlAnLakGKTDShPSjsuUkQSKN7MF6p2C1nNJ23wcTXCVhJHeX0odXo7DJVva-mWWWaJ21lBO4TsCmuwru2viUfRmNblpIMqSaVet_bYBTLwxFWObg6LTjP3JJE3zl46926zMpRNcoo8GyHqVAiv41Dc1nPiQOJ3I0S14l-_N-Hk7Ev_344cXUZ-Uu0uBQ9mR65DT_Oc0Rq4XbUUy0m4bGoq0WtXgKK3unNQTVi4oynS-GH6MSMMfxyvZhI7Ozr6bxlp005fPkDHswngg)


