#
#	SERVER.PY
#	CREATED ON      :   02/22/21
#   LAST UPDATED    :   02/27/21
#


import socket
import os
import logging
import sys
from configparser import ConfigParser
from datetime import datetime
from _thread import *

#   CONSTANT DEFINITIONS
END_SERVICE = "end\r\n"

#   How many conns are connected
clientCount = 0

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
if appendLog["shouldAppend"] == '0':
    fileType = "w"  #   Delete and create new log file
else:
    fileType = "a"  #   Append the log file

#   If the ALL level log is set, enable everything else
#   If this is set, we DO NOT need to check allLog['isEnabled']
if allLog["isEnabled"] == '1':
    fatalLog["isEnabled"] = '1'
    errorLog["isEnabled"] = '1'
    warnLog["isEnabled"] = '1'
    infoLog["isEnabled"] = '1'
    debugLog["isEnabled"] = '1'
    traceLog["isEnabled"] = '1'

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
level=logging.DEBUG)    #   DEBUG will allow all levels to be logged, this will be changed

if enableLog == 0:
    if traceLog["isEnabled"] == '1':
        logging.getLogger().setLevel(TRACE)
        logging.log(TRACE, 'Completed basic logging config')
        logging.log(TRACE, 'Log file directory: %s', DIR)
        logging.log(TRACE, 'Log file name: %s', FILE_NAME)
        

######################################################################################
#
#   START THE SERVER
#
######################################################################################

#   Create the socket
try:
    s = socket.socket()
    s.bind((HOST, PORT))
except Exception as e:
    if enableLog == 0:
        if fatalLog["isEnabled"] == '1':
            logging.getLogger().setLevel(FATAL)
            logging.log(FATAL, 'Error: Creating socket failed: %s' %e)
        elif traceLog["isEnabled"] == '1':
            logging.getLogger().setLevel(TRACE)
            logging.log(TRACE, 'Error: Creating socket failed: %s' %e)
    sys.exit(1)

#   Prompts that the server is running
if enableLog == 0:
    if infoLog["isEnabled"] == '1':
        logging.info('Starting Log server on IP: %s%s', HOST, PORT)
    elif debugLog["isEnabled"] == '1':
        logging.debug('Current Version: 1.2')
    elif traceLog["isEnabled"] == '1':
        logging.getLogger().setLevel(TRACE)
        logging.log(TRACE, ('Starting Log server on IP: ', HOST, PORT))
        logging.log(TRACE, 'Current Version: 1.2')




######################################################################################
#
#   MULTI-THREADING FUNCTION (ALLOWS MULTIPLE connS)
#
######################################################################################
def acceptClient(conn, id):
    while 1:
        try:
            #   Recieve the passed data
            data = conn.recv(2048)
            response = data.decode('utf-8')

            #   Check if the data is equal to the ending variable
            if response == END_SERVICE:
                break
            if not data:
                break

            #   Send the passed data back to the client
            conn.send(str.encode(response))

            #   Log the passed data
            if debugLog["isEnabled"] == '1':
                logging.debug("Recieved data: " + str(data) + " from client: [" + str(id) + "]")
            elif traceLog["isEnabled"] == '1':
                logging.getLogger().setLevel(TRACE)
                logging.log("Recieved data: " + str(data) + " from client: [" + str(id) + "]")
        #   If something FATAL happens
        except Exception as e:
            if enableLog == 0:
                if fatalLog["isEnabled"] == '1':
                    logging.getLogger().setLevel(FATAL)
                    logging.log(FATAL, 'Error: Receiving data failed: %s' %e)
                elif traceLog["isEnabled"] == '1':
                    logging.getLogger().setLevel(TRACE)
                    logging.log(TRACE, 'Error: Receiving data failed: %s' %e)
                    logging.log(TRACE, 'Server is shutting down...')
            sys.exit(1)

    if enableLog == 0:
        #   Check for 'end' message, if received then exit loop
        if data.decode("utf-8") == END_SERVICE:
            if debugLog["isEnabled"] == '1':
                logging.debug('End message received - shutting down server')
            elif infoLog["isEnabled"] == '1':
                logging.info('Client disconnected')
            elif traceLog["isEnabled"] == '1':
                logging.getLogger().setLevel(TRACE)
                logging.log(TRACE, 'End message received - shutting down server')
                logging.log(TRACE, 'Client disconnected')

    #   Close the socket connection
    if enableLog == 0:
        if infoLog["isEnabled"] == '1':
            logging.info('conn disconnected')
        elif traceLog["isEnabled"] == '1':
            logging.getLogger().setLevel(TRACE)
            logging.log(TRACE, 'conn disconnected')
    conn.close()
    #   Subtract one from the client count as this only counts connected clients
    clientCount -= 1







######################################################################################
#
#   WAIT FOR conn CONNECTION(S)
#
######################################################################################

#   Listen for a conn connection
s.listen(5)

#   Accept the connection
try:
    while 1:
        conn, addr = s.accept()
        clientCount += 1
        start_new_thread(acceptClient, (conn, clientCount, ))
        if enableLog == 0:
            if infoLog["isEnabled"] == '1':
                logging.info("Client connected")
                logging.info("Total clients connected: " + str(clientCount))
            elif traceLog["isEnabled"] == '1':
                logging.getLogger().setLevel(TRACE)
                logging.log(TRACE, 'Client connected')
                logging.log(TRACE, 'Total clients connected: ' + str(clientCount))
except Exception as e:
    if enableLog == 0:
        if fatalLog["isEnabled"] == '1':
            logging.getLogger().setLevel(FATAL)
            logging.log(FATAL, 'Error: Accepting client failed: %s' %e)
        elif traceLog["isEnabled"] == '1':
            logging.getLogger().setLevel(TRACE)
            logging.log(TRACE, 'Error: Accepting client failed: %s' %e)
    sys.exit(1)