# This utility send a pulse to emoncms
#  
# coded by:
# Auteur : Edwin Bontenbal
# Email  : Edwin.Bontenbal@Gmail.COM 
version = "v1.01"
# VERSION    DATE        ADDED FUNCTIONALITY
# 1.01	     03-05-2017  Config file added	

# if errors during executing this scrip make sure you installed phyton and the required modules/libraries
import ConfigParser
import datetime
import requests
import time
import logging
import json
import urllib2
import RPi.GPIO as GPIO
from time import sleep

LogFile              = "/var/log/Pulse2Emoncms.log"
WatchdogFile         = "/tmp/Pulse2Emoncms_Watchdog"

Config = ConfigParser.ConfigParser()
Config.read("/etc/Pulse2Emoncms/Pulse2Emoncms.cfg")

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            logging.debug("Reading config file : " + section + "," + option + " = " +  dict1[option] )
        except:
            dict1[option] = None
    return dict1

# Set emoncms variables
emon_privateKey = ConfigSectionMap("emoncms")['privatekey']
emon_node       = ConfigSectionMap("emoncms")['node']
emon_host       = ConfigSectionMap("emoncms")['host']
emon_protocol   = ConfigSectionMap("emoncms")['protocol']
emon_url        = ConfigSectionMap("emoncms")['url']

# Set puls variables
IOPin           	 = int(ConfigSectionMap("pulsedevice")['iopin'])
minpulseduration	 = ConfigSectionMap("pulsedevice")['minpulseduration']

# define input port for measuring pulses
GPIO.setmode(GPIO.BCM)
#GPIO.setup(IOPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(IOPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

###############################################################################################################
# initialize settings
###############################################################################################################

#Initialize

#Set logging params
logging.basicConfig(filename=LogFile,format='%(asctime)s %(message)s',level=logging.DEBUG)

#Show startup arguments 
logging.warning("IOPin on rapsberry used for counting pulses : %s" % (IOPin))

#Setting variables
NumberOfCountedPulses = 0
EventTime             = 0
OldEventTime          = 0
StateDuration         = 0


###############################################################################################################
# Main program
###############################################################################################################

def FunctionTrigger(channel):
    value     = GPIO.input(IOPin)

    global EventTime   
    EventTime = int(time.time())

    global Stateduration   
    global OldEventTime   
    global NumberOfCountedPulses 
   
    if   value == 0:
      logging.debug("Falling edge detected on pin  : " + str(IOPin))
      logging.debug("Value                         : " + str(value))
      StateDuration = EventTime - OldEventTime
      logging.debug("Rising  edge detected at time : " + str(OldEventTime))
      logging.debug("Falling edge detected at time : " + str(EventTime))
      logging.debug("High duration time            : " + str(StateDuration))

      OldEventTime = EventTime 
  
    elif value == 1: 
      NumberOfCountedPulses += 1

      logging.debug("Rising  edge detected on pin  : " + str(IOPin))
      logging.debug("Value                         : " + str(value))
      StateDuration = EventTime - OldEventTime
      logging.debug("Falling edge detected at time : " + str(OldEventTime))
      logging.debug("Rising  edge detected at time : " + str(EventTime))
      logging.debug("Low duration time             : " + str(StateDuration))

      OldEventTime = EventTime 

GPIO.add_event_detect(IOPin, GPIO.BOTH, callback=FunctionTrigger, bouncetime=1000)

while True:
 # wait 15 sec before updating to emomcms
 sleep (15)

 # write time to watchdog file  
 f3=open(WatchdogFile, "w")
 timestamp = int(time.time())
 f3.write (str(timestamp))
 f3.close()

 DataJson = {}   
 logging.debug("Total number of pulses found  : " + str(NumberOfCountedPulses)) 
 DataJson["WaterPulse"] = int(NumberOfCountedPulses) 

 NumberOfCountedPulses = 0 
 
 url  = emon_protocol + emon_host + emon_url + "node=" + str(emon_node)+ "&apikey=" + emon_privateKey + "&json=" + str( json.dumps(DataJson, separators=(',', ':')))
 logging.debug(url)
 HTTPresult = urllib2.urlopen(url)
 logging.debug("Response code : " +  str(HTTPresult.getcode()))
GPIO.cleanup()
