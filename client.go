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
	"strings"
)

const (
	testArg = "-test"
)

func createTestString(flag, msg string) string {
	return fmt.Sprintf("[%s]%s\r\n", strings.ToUpper(flag), msg)
}

func main() {

	//	Source for sockets in Golang: https://golangr.com/socket-client/

	//	Define variables for the socket -> must be changed for ZeroTier
	protocolType := "tcp"
	ip := "127.0.0.1:50000"

	// Get arguments from the command line
	argv := os.Args[1:]

	//	Create client side socket
	conn, _ := net.Dial(protocolType, ip)

	// Check if '-test' command line arg is given for automated testing
	if len(argv) == 1 && argv[0] == testArg {

		fmt.Println("Starting automated tests...")
		// RUN THROUGH TESTS HERE ******

		// 10 debug test messages
		fmt.Println("DEBUG TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("all", "All test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
		}

		// 10 trace test messages
		fmt.Println("TRACE TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("trace", "Trace test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
		}

		// 10 debug test messages
		fmt.Println("DEBUG TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("debug", "Debug test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
		}

		// 10 info test messages
		fmt.Println("INFO TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("info", "Info test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
		}

		// 10 warn test messages
		fmt.Println("WARN TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("warn", "Warn test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
		}

		// 10 error test messages
		fmt.Println("ERROR TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("error", "Error test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
		}

		// 10 fatal test messages
		fmt.Println("FATAL TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("fatal", "Fatal test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
		}


		// Manual log testing
	} else {
		for {
			//	Read log entry from keyboard
			reader := bufio.NewReader(os.Stdin)

			fmt.Println("Please enter a log: ")
			fmt.Println("Log file format: [FLAG]<log>")

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
