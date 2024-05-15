# Asvalid Tool

- Asvalid is a tool that helps validate static Aerospike configuration file(.conf) and validates it against aerospike's configuration schema.
- Asvalid also helps compare dynamic configuration values from a running node to the values mentioned in static configuration file. 
- It helps identify any inconsistencies between the dynamic runtime configuration and the static configuration file.


## Use Cases

```bash
Usage: asvalid [option] [arguments]
Options:
	asvalid validate <file>                  Validate a configuration file against the Aerospike schema.
	asvalid verify                           Validate and compare live cluster values to static conf values.
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

2. asvalid verify
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
# Flow

[![](https://mermaid.ink/img/pako:eNptU39r2zAQ_SqHoKBC2w-QwiBN0kDazmPZBoP8c7NPiVZLMvqREZp-98knu15g_sNYd-_u3nsnv4naNSRmYu-xO8C35f3OQn7mEsMRW91cw-3tp_NwAH5jpDM8FNyD_II-UDmgPcFd7awCpVviSljIxYHqV1DOQ4ceDUXy4boULBiylD-GtvBHxwNg6Hvo_QBaMuirXHnvfCgxnUe4ZJt-5AVsJasUuxRHptrZnC-IqyuYX6ipncmUspjHAngsYgDJu9DpV2Ixo7Yeb4_kI0QHP-cvz5CCtvuJLhNYS05lyGZbfZ5qAx5z4wC_MFCrLd39Dkytz6-5EjZyTZZ870Nzsmh0zSBQ3hnwydp-Wqmo2xSyjx8MtFWul2PyqNHcDXd9kouikvnwYkbAEwO2g7HwX2f_RT6P3jZaKfJka241gi69zUZpdTpDVZLVtOOGFKY2DtZcWM0WDsuoeOZ3OS0SFOp2ugBUaDNbVrSz4kYY8gZ1k2_0G8dEPJChnZjlz3Gy2Nn3DMUU3fZkazGLPtGNSF3Pb6kx_wtGzBS24SO6anR0fgi-_wU3OwXI?type=png)](https://mermaid-live-editor.fly.dev/edit#pako:eNptU39r2zAQ_SqHoKBC2w-QwiBN0kDazmPZBoP8c7NPiVZLMvqREZp-98knu15g_sNYd-_u3nsnv4naNSRmYu-xO8C35f3OQn7mEsMRW91cw-3tp_NwAH5jpDM8FNyD_II-UDmgPcFd7awCpVviSljIxYHqV1DOQ4ceDUXy4boULBiylD-GtvBHxwNg6Hvo_QBaMuirXHnvfCgxnUe4ZJt-5AVsJasUuxRHptrZnC-IqyuYX6ipncmUspjHAngsYgDJu9DpV2Ixo7Yeb4_kI0QHP-cvz5CCtvuJLhNYS05lyGZbfZ5qAx5z4wC_MFCrLd39Dkytz6-5EjZyTZZ870Nzsmh0zSBQ3hnwydp-Wqmo2xSyjx8MtFWul2PyqNHcDXd9kouikvnwYkbAEwO2g7HwX2f_RT6P3jZaKfJka241gi69zUZpdTpDVZLVtOOGFKY2DtZcWM0WDsuoeOZ3OS0SFOp2ugBUaDNbVrSz4kYY8gZ1k2_0G8dEPJChnZjlz3Gy2Nn3DMUU3fZkazGLPtGNSF3Pb6kx_wtGzBS24SO6anR0fgi-_wU3OwXI)


