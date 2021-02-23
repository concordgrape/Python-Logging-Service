#
#	SERVER.PY
#	CREATED ON      :   02/22/21
#   LAST UPDATED    :   02/23/21
#

#   Source  :   https://realpython.com/python-sockets/
import socket
import os
import logging

#   Define the IP information for the server socket
HOST = '127.0.0.1'
PORT = 50000

#   Name of the log file
path = "./logs/test_log_file.txt"

#   Check if the file exists in the directory, if not, create it
if not os.path.isfile(path):

    #   Create the logs directory
    os.mkdir("./logs")

    #   Create the logging file
    logging.basicConfig(filename=path, level=logging.WARNING)

#   Start a log message
logging.debug("Debug information")

#   Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

#   Listen for a client connection
s.listen(1)

#   Accept the connection
conn, addr = s.accept()

#   Wait until data has been recieved from the client
while 1:

    data = conn.recv(1024)

    #   Check if data was recieved
    if not data:
        break

    #   Display message
    print('Recieved', data)

    #   Send the message back to the client
    conn.sendall(data)

    #   Close the socket connection
    conn.close()
    break