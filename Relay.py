import RPi.GPIO as GPIO
import time

#printerRelay = None
#Buzzer = None
#fanRelay = None
heatbedRelay = 25
#lightRelay = None

GPIO.setmode(GPIO.BCM)
#GPIO.setup(printerRelay, GPIO.OUT)
#GPIO.setup(Buzzer, GPIO.OUT)
#GPIO.setup(fanRelay, GPIO.OUT)
GPIO.setup(heatbedRelay, GPIO.OUT)
#GPIO.setup(lightRelay, GPIO.OUT)
'''
def setPrinter(state):
    if state == 0:
        GPIO.output(printerRelay, True)
    else:
        GPIO.output(printerRelay, False)

def setFan(state):
    if state == 0:
        GPIO.output(fanRelay, True)
    else:
        GPIO.output(fanRelay, False)
'''
def setHeatbed(state):
    if state == 0:
        GPIO.output(heatbedRelay, True)
    else:
        GPIO.output(heatbedRelay, False)
'''
def setLight(state):
    if state == 0:
        GPIO.output(lightRelay, True)
    else:
        GPIO.output(lightRelay, False)

def buzzer(state):
    if state == 0:
        GPIO.output(Buzzer, True)
    else:
        GPIO.output(Buzzer, False)
'''
def turnOffAll():
    #GPIO.output(printerRelay, False)
    #GPIO.output(fanRelay, False)
    GPIO.output(heatbedRelay, True)
    #GPIO.output(lightRelay, False)
    #GPIO.output(Buzzer, False)
