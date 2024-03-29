#
#	FILENAME        :   service.py
#   PROJECT         :   SENG2040_A3
#   DESCRIPTION     :   This program reads log configuration details from config.ini which determine
#                       network details, log format, log levels etc. It then listens for and connects
#                       to clients via tcp, reads a message from them, sends a response, and logs the 
#                       message according to the settings.
#   AUTHORS         :   Sky Roth, Liam Schoel
#	CREATED ON      :   02/22/21
#   LAST UPDATED    :   02/28/21
#


import socket
import os
import logging
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from _thread import *

#   CONSTANT DEFINITIONS
END_SERVICE = "end\r\n"
MAX_MESSAGES = 100
MAX_READABLE_BYTES = 2048
TIMEOUT = 10

#   How many clients are connected
clientCount = 0
FORMAT_DEFAULT = '%(asctime)s %(levelname)-8s %(message)s'

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
MAX_CLIENTS = int(config_object["SERVER-DETAILS"]["MAX_CLIENTS"])

DIR = config_object["LOG-DETAILS"]["DIR"]
FILE_NAME = config_object["LOG-DETAILS"]["FILE_NAME"]
_DEFAULT = config_object["LOG-DETAILS"]["FORMAT"]

#   If user entered 'DEFAULT' allow the format to be in the default format
if _DEFAULT == 'DEFAULT':
    _DEFAULT = FORMAT_DEFAULT


#   Format the customer format that the user inputted in config.ini
customFormat = True
try:
    formatted = ''
    if _DEFAULT != DEFAULT or _DEFAULT != FORMAT_DEFAULT:
        for char in _DEFAULT:
            if char == '(' or char == ')':
                if char == '(':
                    formatted = formatted + '%' + char
                if char == ')':
                    formatted = formatted + char + 's'
            else:
                formatted = formatted + char
    else:
        _DEFAULT = FORMAT_DEFAULT
        customFormat = False
    if formatted != '':
        _DEFAULT = formatted
        customFormat = True
except:
    _DEFAULT = FORMAT_DEFAULT
    customFormat = False

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
format=_DEFAULT,
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
    if customFormat:
        if traceLog["isEnabled"] == '1':
            logging.getLogger().setLevel(TRACE)
            logging.log(TRACE, 'Custom format successfully configured')
        elif debugLog["isEnabled"] == '1':
            logging.debug("Custom format successfully configured")
    else:
        if traceLog["isEnabled"] == '1':
            logging.info('Custom format NOT configured, using default')
        elif debugLog["isEnabled"] == '1':
            logging.debug("Custom format NOT configured, using default")
        

######################################################################################
#
#   START THE SERVER
#
######################################################################################

#   Create the socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        logging.info('Starting Log server on IP: %s:%s', HOST, PORT)
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
    global clientCount
    timeoutCounter = time.perf_counter()    # get start time
    msgCounter = 0

    while 1:
        try:
            #   Recieve the passed data
            data = conn.recv(MAX_READABLE_BYTES)
            response = data.decode('utf-8')

            #   Check if the data is equal to the ending variable
            if response == END_SERVICE:
                break
            if not data:
                break

            msgCounter += 1
            #   Checks how much time has elapsed for 100 messages
            if msgCounter > MAX_MESSAGES:
                #   If the 100 messages were sent in under 2 seconds do something (disconnect from client)
                if (time.perf_counter() - timeoutCounter) < TIMEOUT:
                    if enableLog == 0:
                        if fatalLog["isEnabled"] == '1':
                            logging.getLogger().setLevel(FATAL)
                            logging.log(FATAL, "Error: Too many messages were sent in a short period of time, closing connection to client")
                        elif traceLog["isEnabled"] == '1':
                            logging.getLogger().setLevel(TRACE)
                            logging.log(TRACE, "Too many messages were sent in a short period of time, closing connection to client")
                    conn.close()
                    clientCount -= 1
                else:
                    #   Reset variables if no timeout is needed
                    msgCounter = 0
                    timeoutCounter = time.perf_counter()

            #   Send the passed data back to the client
            conn.send(str.encode(response))

            #   Custom log entries
            flag = response[response.find('[') + 1 : response.find(']')]
            if (response.find('[') + 1) > 0 and (response.find(']')) > 0:
                if enableLog == 0:
                    if traceLog["isEnabled"] == '1':
                        logging.getLogger().setLevel(TRACE)
                        logging.log(TRACE, "Custom log entry received: " + str(data))
                    try:
                        msg = (response[response.find(']') + 1 : len(response)]).replace('\r\n', '')
                        if flag == "DEBUG" and debugLog["isEnabled"] == '1':
                            logging.debug(msg)
                        elif flag == "FATAL":
                            logging.getLogger().setLevel(FATAL)
                            logging.log(FATAL, msg)
                        elif flag == "ERROR":
                            logging.error(msg)
                        elif flag == "WARN":
                            logging.warning(msg)
                        elif flag == "INFO":
                            logging.info(msg)
                        elif flag == "TRACE":
                            logging.getLogger().setLevel(TRACE)
                            logging.log(TRACE, msg)
                        else:
                            logging.getLogger().setLevel(ERROR)
                            logging.log(ERROR, "Entered flag doesn't exist: " + flag)
                    except:
                        logging.log(FATAL, "Error: Flag not found: " + flag)
            else:
                #   Log the passed data
                if debugLog["isEnabled"] == '1':
                    logging.debug("received data: " + str(data) + " from client: [" + str(id) + "]")
                elif traceLog["isEnabled"] == '1':
                    logging.getLogger().setLevel(TRACE)
                    logging.log(TRACE, "received data: " + str(data) + " from client: [" + str(id) + "]")
        #   If something FATAL happens
        except Exception as e:
            clientCount -= 1
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
                logging.debug('End message received - closing connection with client')
            elif infoLog["isEnabled"] == '1':
                logging.info('Client disconnected')
            elif traceLog["isEnabled"] == '1':
                logging.getLogger().setLevel(TRACE)
                logging.log(TRACE, 'End message received - closing connection with client')
                logging.log(TRACE, 'Client disconnected')

    #   Close the socket connection
    if enableLog == 0:
        if infoLog["isEnabled"] == '1':
            logging.info('Client disconnected')
        elif traceLog["isEnabled"] == '1':
            logging.getLogger().setLevel(TRACE)
            logging.log(TRACE, 'Client disconnected')
    conn.close()
    #   Grab the clientCount variable
    clientCount -= 1







######################################################################################
#
#   WAIT FOR CLIENT CONNECTION(S)
#
######################################################################################

#   Listen for a client connection
s.listen(5)

#   Accept the connection
try:
    while 1:
        conn, addr = s.accept()
        if clientCount < MAX_CLIENTS:
            clientCount += 1
            start_new_thread(acceptClient, (conn, clientCount, ))
            if enableLog == 0:
                if debugLog["isEnabled"] == '1':
                    logging.debug("Starting new client thread, with ID: " + str(clientCount))
                elif traceLog["isEnabled"] == '1':
                    logging.getLogger().setLevel(TRACE)
                    logging.log(TRACE, "Starting new client thread, with ID: " + str(clientCount))
        else:
            if fatalLog["isEnabled"] == '1':
                logging.getLogger().setLevel(FATAL)
                logging.log(FATAL, 'Error: Accepting client failed, Max clients have been reached')
            elif traceLog["isEnabled"] == '1':
                logging.getLogger().setLevel(TRACE)
                logging.log(TRACE, 'Error: Accepting client failed, Max clients have been reached')
            conn.close()
            clientCount -= 1
            break
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