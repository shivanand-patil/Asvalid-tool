# Asvalid Tool

- Asvalid is a tool that helps validate static Aerospike configuration file against aerospike's versioned schemas.
- Asvalid also helps compare dynamic configuration values from a running node to the values mentioned in configuration file. 
- It helps identify any inconsistencies adn  report differences between the dynamic runtime configuration and the static file.

# Installation
Clone the repository
  ```bash
  git clone https://github.com/shivanand-patil/Asvalid-tool.git
  ```
Move to cloned directory and run installation script
  ```bash
  sudo ./install.sh
  ```  
## Use Cases

```bash
Usage: asvalid [option] [arguments]
Options:
	asvalid validate <file>                  Validate a configuration file against the Aerospike schema.
	asvalid verify                           Validate and compare live cluster values to values mentioned in config file.
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
# Flow of the tool

<img width="1009" alt="Screenshot 2024-05-19 at 8 06 11 PM" src="https://github.com/shivanand-patil/Asvalid-tool/assets/70444072/d3287539-55f7-4b25-996b-6fb647d7a2e7">



# SaltStack Flow

![image](https://github.com/shivanand-patil/Asvalid-tool/assets/70444072/4329973b-6ff8-4700-a6db-21830e3858c1)




