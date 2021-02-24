#
#	SERVER.PY
#	CREATED ON      :   02/22/21
#   LAST UPDATED    :   02/24/21
#



import socket
import os
import logging
from configparser import ConfigParser



######################################################################################
#
#   DEFINE SERVER PROPERTIES
#
######################################################################################



#   Define the IP information for the server socket
HOST = '127.0.0.1'
PORT = 50000


#   Prompts that the server is running
print("Starting Log server on IP: ", HOST, PORT)
print("Current version: 1.0")



######################################################################################
#
#   LOAD LOG FILE FLAGS
#
######################################################################################
config_object = ConfigParser()

config_object.read("config.ini")

appendLog = config_object["APPEND"]

fatalLog = config_object["FATAL"]

errorLog = config_object["ERROR"]

warnLog =  config_object["WARN"]

infoLog = config_object["INFO"]

debugLog = config_object["DEBUG"]

traceLog = config_object["TRACE"]

allLog = config_object["ALL"]

enableLog = config_object["OFF"]


#   Check if the program should log information, this variable will be used throughout the program
if enableLog == 0:
    print("Log file ENABLED")
else:
    print("Log file DISABLED")


#   Create a variable that will determine if the file should be appended or not
if appendLog["shouldAppend"] == '0;':   #   For some reason this config var adds a semicolon?
    fileType = "w"  #   Delete and create new log file
else:
    fileType = "a"  #   






######################################################################################
#
#   CREATE LOG FILE
#
######################################################################################
logPath = "./logs/test_log_file.txt"
path = "./logs/"

#   Check if directory exists, if not, create it
if not os.path.isdir(path):
    #   Create the logs directory
    os.mkdir(path)


#   Check if file exists, if not, create it
if not os.path.isfile(logPath):
    f = open(logPath, fileType)





######################################################################################
#
#   OPEN AND WRITE TO LOG FILE
#
######################################################################################
logging.basicConfig(filename=logPath, filemode=fileType, level=logging.DEBUG)

#   Start a log message -> These are examples and will be changed
logging.debug('This is a test log')
logging.info('This is a test log')
logging.warning('This is a test log')
logging.error('This is a test log')
logging.critical('This is a test log')





######################################################################################
#
#   START THE SERVER
#
######################################################################################

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