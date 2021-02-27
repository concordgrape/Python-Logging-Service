/*
*	CLIENT.GO
*	CREATED ON      :   02/22/21
*   LAST UPDATED    :   02/27/21
 */

package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

const (
	testArg = "-test"
)

func main() {

	//	Source for sockets in Golang: https://golangr.com/socket-client/

	//	Define variables for the socket -> must be changed for ZeroTier
	protocolType := "tcp"
	ip := "127.0.0.1:50000"

	// Get arguments from the command line
	argv := os.Args[1:]

	// Check if '-test' command line arg is given for automated testing
	if len(argv) == 1 && argv[0] == testArg {

		fmt.Println("Starting automated tests...")
		// RUN THROUGH TESTS HERE ******

		// Manual log testing
	} else {

		//	Create client side socket
		conn, _ := net.Dial(protocolType, ip)

		for {
			//	Read log entry from keyboard
			reader := bufio.NewReader(os.Stdin)

			fmt.Println("Please enter a log: ")

			log, _ := reader.ReadString('\n')

			//	Send the log that the user entered into the socket
			fmt.Fprintf(conn, log)

			//	Read message sent back from the server
			message, _ := bufio.NewReader(conn).ReadString('\n')

			//	Display the message
			fmt.Println("Received back from server: " + message)
		}
	} // End if
} // End main
