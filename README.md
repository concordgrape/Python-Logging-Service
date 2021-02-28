# Python Logging Service

## General info
This project is a logging service tool, it will start a server that can be configured and wait for logging information from the client.

## Technologies
Project is created with:
* Python 3.9.0
* Golang 1.11.7
	
## Setup
To run this project, enable logging flags in the config file, then start the server
To run tests, enter '-test' as a command line argument on the client side

```
$ 'cd ../SENG2040-A2'
$ open config.ini
$ edit server IP information
$ enable flag(s)
$ run the server with 'py service.py'
$ connect the client, client will connect to the IP in the config.ini file
