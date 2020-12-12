import RPi.GPIO as GPIO
import datetime
import time
import os
import logging

#logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
#logging.basicConfig(filename='/var/log/motionDetectDisplayControl.log',format='%(asctime)s %(message)s')


# This monitors a PIR on PIR_PIN. If motion is not detected for TIME_TO_TURN_OFF in seconds, turns off the HDMI.
# HDMI commands tested on pi v3. If motion is detected, turns it back on. Signals sent to LED_PIN to indicate motion detected
# or HDMI commands used. Between LIGHTS_OUT_START_HOUR and LIGHTS_ON_END_HOUR times, HDMI is left off whether motion is detected or not.

# references used
# https://www.modmypi.com/blog/raspberry-pi-gpio-sensing-motion-detection
# http://www.raspberry-pi-geek.com/Archive/2015/10/Raspberry-Pi-IR-remote
# https://learn.sparkfun.com/tutorials/transistors
# https://www.raspberrypi.org/forums/viewtopic.php?t=7570

GPIO.setmode(GPIO.BCM)

LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)

## defined in lirc config: IR_OUT_PIN = 22
## GPIO.setup(IR_OUT_PIN, GPIO.OUT)

SLEEP_TIME = 60                 # seconds
TIME_TO_TURN_OFF = 60 * 60      # turn off after 1 hour of no activity
LIGHTS_OUT_START_HOUR = 23
LIGHTS_ON_END_HOUR = 6

powerOn = True
timeSinceLastMotion = 0


def motion( PIR_PIN ):
    global powerOn
    global timeSinceLastMotion
    timeSinceLastMotion = 0
    blinkyLight( 1, 0.25 )

    if isLightsOutTime():
        logging.debug( "Motion during lights out, NOT turning on" )
        return
    else:
        logging.debug( "Motion Detected!" )

    if powerOn != True and not isLightsOutTime():
        logging.info( "Turning ON TV" )
        toggleMonitorPower()

def toggleMonitorPower():
    global powerOn
    if powerOn == True:
      os.system( "tvservice -o" )
      powerOn = False
      blinkyLight( 3, 0.75 )
      logging.debug( "Power turned OFF" )
    else:
      os.system( "tvservice -p" )
      # the following is needed to refresh x: xrefresh didn't seem to work, but below commands do
      os.system( "chvt 6" )
      os.system( "chvt 7" )
      powerOn = True
      blinkyLight( 3, 0.25 )
      logging.debug( "Power turned ON" )

# old TV IR control
#def sendIrPowerCommand( ledBlinkRate ):
#    os.system( "irsend -#5 SEND_ONCE seiki.conf KEY_POWER" )
#    global LED_PIN
#    blinkyLight( 3, ledBlinkRate )


def blinkyLight( blinkCount, ledBlinkRate ):
    for x in range( blinkCount ):
        GPIO.output( LED_PIN, True )
        time.sleep( ledBlinkRate )
        GPIO.output( LED_PIN, False )
        time.sleep( ledBlinkRate )


def todayAt( hr, min=0, sec=0, micros=0 ):
    now = datetime.datetime.now()
    return now.replace( hour=hr, minute=min, second=sec, microsecond=micros )


def isLightsOutTime():
    now = datetime.datetime.now()
    lightsOutStartTime = todayAt( LIGHTS_OUT_START_HOUR )
    lightsOutEndTime = todayAt( LIGHTS_ON_END_HOUR )
    isLightsOut = not ( lightsOutEndTime < now and lightsOutStartTime > now )
    if( isLightsOut ):
        logging.info( "during lights out time: %s", now )
    return not ( lightsOutEndTime < now and lightsOutStartTime > now )

logging.info( "Configuration: SLEEP_TIME: %s, TIME_TO_TURN_OFF: %s, LIGHTS_OUT_START_HOUR: %s, LIGHTS_ON_END_HOUR: %s", SLEEP_TIME, TIME_TO_TURN_OFF, LIGHTS_OUT_START_HOUR, LIGHTS_ON_END_HOUR )

try:
    GPIO.add_event_detect( PIR_PIN, GPIO.RISING, callback=motion )
    logging.info( "Ready" )
    while 1:
        time.sleep( SLEEP_TIME )
        timeSinceLastMotion += SLEEP_TIME
        logging.debug( "Time since last motion: %ds" % timeSinceLastMotion )
        if (powerOn == True) and ((timeSinceLastMotion >= TIME_TO_TURN_OFF) or isLightsOutTime()):
            logging.info( "TIME_TO_TURN_OFF reached (%ds): Turning OFF TV" % TIME_TO_TURN_OFF )
            toggleMonitorPower()

except KeyboardInterrupt:
    logging.info( "Quit" )
    GPIO.cleanup()
