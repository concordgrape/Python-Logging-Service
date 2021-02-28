# Python Logging Service

## General info
This project is a logging service tool, it will start a server that can be configured and wait for logging information from the client.
The server allows for multiple clients to connect to the server, the amount of total clients can be configured in the 'config.ini' file.

## Available Logging Flags
* [FATAL] - Fatal error, something went horribly wrong and server cannot continue, client will be disconnected
* [ERROR] - Error, something went wrong, server may continue, client may be disconnected
* [WARN] - Warning, there's an error somewhere, this may lead to a FATAL error, should be fixed ASAP
* [INFO] - Information, confirmation that things are working as they should
* [DEBUG] - Debug, detailed information used for diagnostics
* [TRACE] - Trace, like debug but with more detailed information

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
