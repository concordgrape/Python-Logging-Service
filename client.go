/*
*	CLIENT.GO
*	CREATED ON      :   02/22/21
*   LAST UPDATED    :   02/23/21
 */

package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {

	//	Source for sockets in Golang: https://golangr.com/socket-client/

	//	Define variables for the socket -> must be changed for ZeroTier
	protocolType := "tcp"
	ip := "127.0.0.1:50000"

	//	Read log entry from keyboard
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Please enter a log: ")

	log, _ := reader.ReadString('\n')

	//	Create client side socket
	conn, _ := net.Dial(protocolType, ip)

	//	Send the log that the user entered into the socket
	fmt.Fprintf(conn, log)

	//	Read message sent back from the server
	message, _ := bufio.NewReader(conn).ReadString('\n')

	//	Display the message
	fmt.Println("Recieved back from server: " + message)
}
