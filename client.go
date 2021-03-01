/*
*	FILENAME        :   client.go
*   PROJECT         :   SENG2040_A3
*   DESCRIPTION     :   This program allows the user to connect to the logging service and send logs.
*						This can be done manually if no command switches are used, if -test is used
*						the program will autmatically send 10 test logs for each log level before the
*						connection is closed, if -noise <count> is used the program will send fatal
*						logs *count times in order to test the services noise handling.
*   AUTHORS         :   Sky Roth, Liam Schoel
*	CREATED ON      :   02/22/21
*   LAST UPDATED    :   02/28/21
 */

package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
)

const (
	testArg  = "-test"
	noiseArg = "-noise"
)

func createTestString(flag, msg string) string {
	return fmt.Sprintf("[%s]%s\r\n", strings.ToUpper(flag), msg)
}

func main() {

	//	Source for sockets in Golang: https://golangr.com/socket-client/

	// Get arguments from the command line
	argv := os.Args[1:]

	//	Define variables for the socket -> must be changed for ZeroTier
	if len(argv) == 0 {
		fmt.Println("Error: The first argument must be the IP address of the server")
		return
	}
	protocolType := "tcp"
	ip := argv[0] + ":50000"

	//	Create client side socket
	conn, err := net.Dial(protocolType, ip)
	if err != nil {
		fmt.Println(err)
	}

	// Check if '-test' command line arg is given for automated testing
	if len(argv) == 2 && argv[1] == testArg {

		fmt.Println("Starting automated tests...")
		// RUN THROUGH TESTS HERE ******

		// 10 debug test messages
		fmt.Println("DEBUG TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("all", "All test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
		}

		// 10 trace test messages
		fmt.Println("TRACE TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("trace", "Trace test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
		}

		// 10 debug test messages
		fmt.Println("DEBUG TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("debug", "Debug test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
		}

		// 10 info test messages
		fmt.Println("INFO TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("info", "Info test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
		}

		// 10 warn test messages
		fmt.Println("WARN TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("warn", "Warn test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
		}

		// 10 error test messages
		fmt.Println("ERROR TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("error", "Error test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
		}

		// 10 fatal test messages
		fmt.Println("FATAL TEST MESSAGES***************************************************")
		for i := 0; i < 10; i++ {
			fmt.Fprintf(conn, createTestString("fatal", "Fatal test message"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
		}

		//	Stop testing
		fmt.Fprintf(conn, "end/r/n")
		fmt.Println("END TESTING***************************************************")

		// Noisy client
	} else if len(argv) == 3 && argv[1] == noiseArg {
		count, err := strconv.Atoi(argv[2])
		fmt.Println(count)
		fmt.Println(err)

		if err != nil {
			count = 100 // default loop value
		}

		for i := 0; i < count; i++ {
			fmt.Println(i)
			fmt.Fprintf(conn, createTestString("FATAL", "SPAM MESSAGE"))
			message, _ := bufio.NewReader(conn).ReadString('\n')
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
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

			// Stop sending logs on 'end' send
			if log == "end\r\n" {
				break
			}

			//	Display the message
			fmt.Println("Received back from server: " + message)
			if message == "" {
				return
			}
		}
	} // End if
} // End main
