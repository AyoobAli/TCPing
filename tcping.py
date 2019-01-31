#!/usr/bin/env python3

###
### Project: TCPing
### Version: 0.1.3 (Beta)
### Creator: Ayoob Ali ( www.AyoobAli.com )
### License: MIT
###


from time import sleep
from optparse import OptionParser
import signal
import datetime
import socket
import sys, os
import subprocess

settings = {}
settings['success']         = 0
settings['failed']          = 0
settings['verbose']         = 0
settings['timeout']         = 3
settings['sleep']           = 1000
settings['limit']           = 5
settings['quite']           = False
settings['ip']              = "127.0.0.1"
settings['port']            = "80"
settings['version']         = "v0.1.3 (Beta)"
settings['log']             = ""
settings['startTimestamp']  = ""
settings['endTimestamp']    = ""
settings['onCMD']           = ""
settings['offCMD']          = ""

###
### Signal Handler to exit the application after pressing CTRL+C
###
def signal_handler(signal, frame):
    print("\nScan stopped by user.")
    sys.stdout.flush()
    os._exit(0)
signal.signal(signal.SIGINT, signal_handler)

###
### Write application messages based on verbose level
###
def msg(message, vLevel = 0, gvLevel = 0):
    if int(gvLevel) == 0:
        gvLevel = int(settings['verbose'])
    if vLevel <= gvLevel and gvLevel >= 0:
        if settings['quite'] == False:
            print(str(message))
        logData(message)

###
### Write Error messages based on verbose level
###
def err(message, errFrom = "",  vLevel = 3, gvLevel = 0):
    if int(gvLevel) == 0:
        gvLevel = int(settings['verbose'])
    if vLevel <= gvLevel and gvLevel >= 3:
        if settings['quite'] == False:
            print("Error[" + str(errFrom) + "]: " + str(message))
        logData(message)

###
### Log output to file
###
def logData(message):
    try:
        if settings['log'] != "":
            logFile = settings['log']
            message = message + "\n"
            fileHandler=open(logFile, "a+")
            fileHandler.write(str(message))
            fileHandler.close()
            return True
    except Exception as ErrMs:
        print(ErrMs)
        return False

###
### Check if port is Open
###
def tcping():
    connected = False
    try:
        tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tsock.settimeout(settings['timeout'])
        tsock.connect((settings['ip'], int(settings['port'])))
        connected = True
        tsock.shutdown(socket.SHUT_RDWR)
        tsock.close()
        return connected
    except Exception as ErrMs:
        return connected

###
### Check if IP Address is Valid
###
def validIP(ipAddr):
    try:
        socket.inet_aton(ipAddr)
        return True
    except socket.error:
        return False

###
### Send a command to the OS, and return array of returnCode, stdout, and stderr
###
def cmd(command = None):
    returnArr = {}
    returnArr.update({"returnCode": 99})
    try:
        if command == None or command == "":
            return returnArr
        stdout = ""
        stderr = ""
        reCode = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stData = reCode.communicate()
        returnArr.update({"stdout": stData[0].decode("utf-8")})
        returnArr.update({"stderr": stData[1].decode("utf-8")})
        returnArr.update({"returnCode": reCode.returncode})
        reCode.terminate()
        return returnArr
    except Exception as ErrMs:
        returnArr.update({"error": ErrMs})
        err(ErrMs, "CMD")
        return returnArr

###
### Write the program Banner
###
def banner():
    try:
        msg("TCPing " + settings['version'])
        msg("---------------------", 1)
        msg("Started at: " + str(settings['startTimestamp'].strftime("%Y-%m-%dT%H:%M:%S")), 1)
        msg("Pinging IP address " + str(settings['ip']) + " on port " + str(settings['port']))
        msg("---------------------", 1)
        msg("")
        ipLen = len(str(settings['ip'])) - 2
        portLen = len(str(settings['port'])) - 4
        pMSG = "No.  "
        pMSG = pMSG + "Date" + ' '*19
        pMSG = pMSG + "IP" + ' '*ipLen + "         "
        if portLen > 0:
            pMSG = pMSG + "Port" + ' '*portLen + "    "
        else:
            pMSG = pMSG + "Port    "
        
        pMSG = pMSG + "Status  "
        pMSG = pMSG + "Response Time"

        msg(pMSG, 2)

    except Exception as ErrMs:
        err(ErrMs, "banner")

###
### Write the program footer
###
def footer():
    try:
        timeDif = settings['endTimestamp'] - settings['startTimestamp']
        timeDif = timeDif.total_seconds()
        stDays    = divmod(timeDif, 86400)
        stHours   = divmod(stDays[1], 3600)
        stMinutes = divmod(stHours[1], 60)
        stSeconds = divmod(stMinutes[1], 1)

        msg("")
        msg("---------------------",1)
        msg("Stopped at: " + str(settings['endTimestamp'].strftime("%Y-%m-%dT%H:%M:%S")), 1)
        msg("Success: " + str(settings['success']))
        msg("Failed:  " + str(settings['failed']))
        msg("---------------------", 1)
        msg("Ping Completed in: %d Days, %d Hour, %d Minute, %d Second." % (stDays[0], stHours[0], stMinutes[0], stSeconds[0]), 1)
        msg("")
    except Exception as ErrMs:
        err(ErrMs, "footer")

###
### Setup Option Parser
###
def getOp():
    try:
        global settings
        versionTxt = "TCPing " + settings['version']
        versionC = len(versionTxt)
        vertionHead = "╔════" + '═'*versionC + "════╗\n"
        vertionHead = vertionHead + "║    " + versionTxt + "    ║\n"
        vertionHead = vertionHead + "╚════" + '═'*versionC + "════╝\n"

        parser = OptionParser(usage="%prog -i <Host> -p <Port>", version=vertionHead)
        parser.add_option("-i", "--ip", dest="ipAddr", metavar="IP", help="Target IP Address or Hostname to ping")
        parser.add_option("-p", "--port", dest="portNum", type="int", metavar="Port", help="Port Number to ping (Default 80)")
        parser.add_option("-n", "--number", dest="limit", type="int", metavar="Num", help="Limit number of ping requests (Default 5)")
        parser.add_option("-s", "--sleep", dest="pingSleep", type="int", metavar="Num", help="Sleep for x milliseconds after ping request (Default 1000)")
        parser.add_option("-t", "--timeout", dest="pingTimeout", type="int", metavar="Num", help="Connection timeout (Default 3)")
        parser.add_option("-v", "--verbose", action="count", dest="verboseLevel", help="Show more information (-vvv to show error messages)")
        parser.add_option("-q", "--quite", action="store_true", dest="quite", help="Don't print any output")
        parser.add_option("-l", "--log", dest="logFile", metavar="File", help="Log output to a file (Will log even with option -q)")
        parser.add_option("--online-cmd", dest="onCMD", metavar="Command", help="Execute shell command for each online status (Use with caution). Available variables ({#NO#}, {#DATE#}, {#IP#}, {#PORT#}, {#STATUS#} and {#RESPONSE#})")
        parser.add_option("--offline-cmd", dest="offCMD", metavar="Command", help="Execute shell command for each offline status (Use with caution). Available variables ({#NO#}, {#DATE#}, {#IP#}, {#PORT#}, {#STATUS#} and {#RESPONSE#})")

        (options, args) = parser.parse_args()

        if options.verboseLevel != None and int(options.verboseLevel) > 0:
            settings['verbose'] = int(options.verboseLevel)

        if options.ipAddr != None:
            if validIP(options.ipAddr) == True:
                settings['ip'] = str(options.ipAddr)
            else:
                hipAddr = socket.gethostbyname(str(options.ipAddr))
                if validIP(hipAddr) == True:
                    settings['ip'] = str(hipAddr)
                else:
                    err(ErrMs, "Can't resolve Hostname " + str(options.ipAddr) + "[" + str(hipAddr) + "]")
                    sys.exit(1)

        if options.portNum != None and int(options.portNum) > 0:
            settings['port'] = int(options.portNum)

        if options.limit != None and int(options.limit) > -1:
            settings['limit'] = int(options.limit)

        if options.pingSleep != None and int(options.pingSleep) >= 0:
            settings['sleep'] = int(options.pingSleep)

        if  options.pingTimeout != None and int(options.pingTimeout) > 0:
            settings['timeout'] = int(options.pingTimeout)

        if options.quite == True:
            settings['quite'] = True

        if options.logFile != None:
            settings['log'] = str(options.logFile)

        if options.onCMD != None:
            settings['onCMD'] = str(options.onCMD)

        if options.offCMD != None:
            settings['offCMD'] = str(options.offCMD)

    except Exception as ErrMs:
        err(ErrMs, "GetOp")
        sys.exit(1)


###
### Initiate the Application
###
if __name__ == "__main__":
    try:
        getOp() 
        settings['startTimestamp'] = datetime.datetime.now()
        banner()

        i = 1
        while True:

            pNo = str(format(i, '03'))
            pSTime = datetime.datetime.now()
            pStat = tcping()
            pETime = datetime.datetime.now()
            pingTime = pETime - pSTime
            pSTime = str(pSTime.strftime("%Y-%m-%dT%H:%M:%S"))
            pingTime = pingTime.total_seconds()
            pingTime = "{:.3f}".format(pingTime)

            pMSG = pNo + ". "
            pMSG = pMSG + pSTime
            pMSG = pMSG + " IP " + str(settings['ip'])
            pMSG = pMSG + " on port "
            if len(str(settings['port'])) < 4:
                pLen = 4 - len(str(settings['port']))

                pMSG = pMSG + str(settings['port']) + ' '*pLen
            else:
                pMSG = pMSG + str(settings['port'])

            cmdRes = ""
            if pStat == True:
                pMSG = pMSG + " is online "
                settings['success'] += 1

                if str(settings['onCMD']) != "":
                    cmdStr = str(settings['onCMD'])
                    cmdStr = cmdStr.replace("{#NO#}", pNo)
                    cmdStr = cmdStr.replace("{#DATE#}", pSTime)
                    cmdStr = cmdStr.replace("{#IP#}", str(settings['ip']))
                    cmdStr = cmdStr.replace("{#PORT#}", str(settings['port']))
                    cmdStr = cmdStr.replace("{#STATUS#}", "Online")
                    cmdStr = cmdStr.replace("{#RESPONSE#}", str(pingTime))
                    cmdRes = cmd(str(cmdStr))
            else:
                pMSG = pMSG + " is offline"
                settings['failed'] += 1

                if str(settings['offCMD']) != "":
                    cmdStr = str(settings['offCMD'])
                    cmdStr = cmdStr.replace("{#NO#}", pNo)
                    cmdStr = cmdStr.replace("{#DATE#}", pSTime)
                    cmdStr = cmdStr.replace("{#IP#}", str(settings['ip']))
                    cmdStr = cmdStr.replace("{#PORT#}", str(settings['port']))
                    cmdStr = cmdStr.replace("{#STATUS#}", "Offline")
                    cmdStr = cmdStr.replace("{#RESPONSE#}", str(pingTime))
                    cmdRes = cmd(str(cmdStr))

            pMSG = pMSG + " (" + str(pingTime) + " Second)"

            msg(pMSG)
            if isinstance(cmdRes, dict) and 'stdout' in cmdRes:
                msg(cmdRes['stdout'], 2)

            if int(settings['limit']) > 0:
                if int(settings['limit']) <= i:
                    break
            i += 1

            if settings['sleep'] > 0:
                sleep(settings['sleep']/1000)

        settings['endTimestamp'] = datetime.datetime.now()
        footer()
    except Exception as ErrMs:
        err(ErrMs, "root")
