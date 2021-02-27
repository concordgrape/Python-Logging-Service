#
#	SERVER.PY
#	CREATED ON      :   02/22/21
#   LAST UPDATED    :   02/25/21
#


import socket
import os
import logging
from configparser import ConfigParser
from datetime import datetime

# CONSTANT DEFINITIONS
END_SERVICE = "end\r\n"

######################################################################################
#
#   DEFINE SERVER PROPERTIES
#
######################################################################################

config_object = ConfigParser()
config_object.read("config.ini")

#   Define the IP information for the server socket
HOST = config_object["SERVER-DETAILS"]["HOST"]
PORT = int(config_object["SERVER-DETAILS"]["PORT"])

DIR = config_object["LOG-DETAILS"]["DIR"]
FILE_NAME = config_object["LOG-DETAILS"]["FILE_NAME"]

######################################################################################
#
#   LOAD LOG FILE FLAGS
#
######################################################################################

appendLog = config_object["APPEND"]

fatalLog = config_object["FATAL"]

errorLog = config_object["ERROR"]

warnLog =  config_object["WARN"]

infoLog = config_object["INFO"]

debugLog = config_object["DEBUG"]

traceLog = config_object["TRACE"]

allLog = config_object["ALL"]

enableLog = int(config_object["OFF"]["isEnabled"])


#   Create a variable that will determine if the file should be appended or not
if appendLog["shouldAppend"] == '0;':   #   For some reason this config var adds a semicolon?
    fileType = "w"  #   Delete and create new log file
else:
    fileType = "a"  #   Append the log file


######################################################################################
#
#   CREATE LOG FILE
#
######################################################################################

#   Check if directory exists, if not, create it
if not os.path.isdir(DIR):
    #   Create the logs directory
    os.mkdir(DIR)

#   Check if file exists, if not, create it
if not os.path.isfile(DIR+FILE_NAME):
    f = open(DIR+FILE_NAME, fileType)





######################################################################################
#
#   CREATE CUSTOM LOG LEVELS
#
######################################################################################

#   ALL LEVEL
ALL = 1
logging.addLevelName(ALL, "ALL")
def all(self, message, *args, **kws):
    self.log(ALL, message, *args, **kws) 
logging.Logger.all = all


#   FATAL LEVEL
FATAL = 2
logging.addLevelName(FATAL, "FATAL")
def fatal(self, message, *args, **kws):
    self.log(FATAL, message, *args, **kws) 
logging.Logger.fatal = fatal


#   TRACE LEVEL
TRACE = 3
logging.addLevelName(TRACE, "TRACE")
def trace(self, message, *args, **kws):
    self.log(TRACE, message, *args, **kws) 
logging.Logger.trace = trace




######################################################################################
#
#   OPEN AND WRITE TO LOG FILE
#
######################################################################################
logging.basicConfig(
format='%(asctime)s %(levelname)-8s %(message)s',
datefmt='%Y-%m-%d %H:%M:%S',
filename=DIR+FILE_NAME, 
filemode=fileType, 
level=logging.DEBUG)


######################################################################################
#
#   START THE SERVER
#
######################################################################################

#   Create the socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except e:
    if enableLog == 0:
        logging.critical('Error: Creating socket failed: %s' %e)
    sys.exit(1)

s.bind((HOST, PORT))

#   Prompts that the server is running
if enableLog == 0:
    logging.info(('Starting Log server on IP: ', HOST, PORT))
    logging.debug('Current Version: 1.2')




######################################################################################
#
#   WAIT TO RECEIVE DATA FROM CLIENT
#
######################################################################################
while 1:
    
    #   Listen for a client connection
    s.listen(1)

    #   Accept the connection
    try:
        conn, addr = s.accept()
        logging.info('Client connected')
    except e:
        if enableLog == 0:
            logging.critical('Error: Accepting client failed: %s' %e)
        sys.exit(1)


    try:
        data = conn.recv(1024)
    except e:
        if enableLog == 0:
            logging.critical('Error: Receiving data failed: %s' %e)
        sys.exit(1)

    #   Check if data was recieved
    if not data:
        break

    #   Display message
    if enableLog == 0:
        #   Check for 'end' message, if received then exit loop
        if data.decode("utf-8") == END_SERVICE:
            logging.info('End message received - shutting down server')
            logging.info('Client disconnected')
            print( "ENDING LOGGER.")
            break
        
        logging.debug(('Received: ', data))

    #   Send the message back to the client
    conn.sendall(data)

    #   Close the socket connection
    logging.info('Client disconnected')
    conn.close()
    