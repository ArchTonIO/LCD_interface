import socket
import fcntl
import struct
import netifaces as ni
from time import sleep
import I2C_LCD_driver
from  Test import *
from NewLCDscreen import *
from RPi import GPIO
from Sensor import *
#temporary variables
sensorState = 1 #state of distance sensor
plateTemp = 43 #heatbed temperature
boxTemp = 34 #box temperature
printerState = "ON"
fanState = "ON"
lightState = "ON"
camState = "ON"
buzzerState = "ON"
outOfFilament = "ON"
tempAlert = "ON"
endedPrint = "ON"
customval = 60 #value of custom material temperature
pTimeH = 1 #printing time (hours)
pTimeM = 10 #printing time (minutes)

clk = 17
dt = 18
sw = 26

Trigger = 23
Echo = 24
MaxDistance = 300

list1 = ["  ON/OFF MENU", "  SETTINGS", "  MATERIAL SETTINGS", "  SHUTDOWN"]  #menuscreen list

#msterialscreen lists
fasullalist = ["ON", "ON", "ON", "ON", "ON"]

list5 = ["TURN OFF THE SYSTEM ?", "        SURE        ", "         NO         "] #shutdownscreen list

def staticOnoffString(): #onoffString function put the State0-State4 value into the onoffscreen list
    staticList2 = ["   PRINTER", "   FAN", "   CAM", "   LIGHT", "   BUZZER"] #staticOnoffscreen list
    return staticList2

def dynamciOnoffList(position, status): #funciton to change the dynamicOnofflist content, accordingly to user input
    value0 = "OFF"
    value1 = "OFF"
    value2 = "OFF"
    value3 = "OFF"
    value4 = "OFF"

    if position == 0:
        if status == "ON":
            value0 = "ON"
        else:
             value0 = "OFF"

    if position == 1:
        if status == "ON":
            value1 = "ON"
        else:
             value1 = "OFF"

    if position == 2:
        if status == "ON":
            value2 = "ON"
        else:
             value2 = "OFF"

    if position == 3:
        if status == "ON":
            value3 = "ON"
        else:
             value3 = "OFF"

    if position == 4:
        if status == "ON":
            value4 = "ON"
        else:
             value4 = "OFF"

    dynamicList = [value0, value1, value2, value3]
    return dynamicList




def settingsString(State5, State6, State7): #settingsString function put value into the settingsscreen list
    list3 = ["OUT OF FILAMENT "+State5, "TEMP. ALERT "+State6, "ENDED PRINT "+State7] #settingscreen list
    return list3

def materialscreenString(selection, customval): #materialscreenString function chooses different list according to "selection" val

    list4a = ["=> PLA (H 50)", "   ABS (H 80)", "   CUSTOM (H " + str(customval) + ")"]
    list4b = ["   PLA (H 50)", "=> ABS (H 80)", "   CUSTOM (H " + str(customval) + ")"]
    list4c = ["   PLA (H 50)", "   ABS (H 80)", "=> CUSTOM (H " + str(customval) + ")"]

    materialStringList = []

    if (selection == "PLA"):
        materialStringList = list4a
    if (selection == "ABS"):
        materialStringList = list4b
    if (selection == "CUSTOM"):
        materialStringList = list4c

    return materialStringList

Encoder = Rotary(dt, clk, sw)
distanceSensor = Sensor(Trigger, Echo, MaxDistance)
menuscreen = Menu(list1)
onoffscreen = DynamicMenu(staticOnoffString())
settingscreen = Menu(settingsString(outOfFilament, tempAlert, endedPrint))
materialscreen = Menu(materialscreenString("PLA", customval))
shutdownscreen = Menu(list5)

def back():
    if distanceSensor.readDistanceCentimeters() < 20:
        clear()
        return True

def stdbyScreen(temp1, temp2, State0, State1, State2, State3):
    list4 = [temp1, temp2, State0, State1, State2, State3]
    stdbyScreen = standByScreen(temp1, temp2, State0, State1, State2, State3)
    stdbyScreen.display()

def mainScreen(hours, minutes):
    list0 = ["  PRINTER  CONTROL  ", voidstring(), "PRINTING TIME "+str(hours)+":"+str(minutes), "   "+"IP "+ IpAdress()+"   "]
    mainscreen = Menu(list0)
    mainscreen.run(0)

def runInterface():
    while True:
        stdbyScreen(plateTemp, boxTemp, printerState, lightState, camState, buzzerState)
        if back() == True:#checking sensor
            clear()
            while True:
                #mainscreen running
                    mainScreen(1, 10)

                    if back() == True:
                        runInterface()

                    if Encoder.button() == 0:
                        cursor = 0
                        clear()
                        Encoder.enable()
                        sleep(0.5)
                        while True:
                            #menuscreen running
                            if Encoder.read()!= None:
                                cursor = Encoder.read()
                                menuscreen.run(cursor)

                            #menuscreen selection block 0
                            if menuscreen.read(Encoder.button(), cursor)== 0:
                                cursor = 0
                                clear()
                                Encoder.enable()
                                sleep(0.5)
                                state = 0
                                while True:
                                    if Encoder.read()!= None:
                                        cursor = Encoder.read()
                                        onoffscreen.run(fasullalist, cursor)


                                    if back() == True:
                                        runInterface()


                                    if onoffscreen.read(Encoder.button(), cursor) == 0:
                                        state = 1

                                    if onoffscreen.read(Encoder.button(), cursor) == 1:
                                        state = 2

                                    if onoffscreen.read(Encoder.button(), cursor) == 2:
                                        state = 3

                                    if onoffscreen.read(Encoder.button(), cursor) == 3:
                                        state = 4




                            #menuscreen selection block 1
                            if menuscreen.read(Encoder.button(), cursor)== 1:
                                clear()
                                Encoder.enable()
                                cursor = 0
                                while True:
                                    if Encoder.read()!= None:
                                        cursor = Encoder.read()
                                        settingscreen.run(cursor)

                                    if back() == True:
                                        runInterface()

                            #menuscreen selection block 2
                            if menuscreen.read(Encoder.button(), cursor)== 2:
                                clear()
                                Encoder.enable()
                                cursor = 0
                                while True:
                                    if Encoder.read()!= None:
                                        cursor = Encoder.read()
                                        materialscreen.run(cursor)

                                    if back() == True:
                                        runInterface()

                            #menuscreen selection block 3
                            if menuscreen.read(Encoder.button(), cursor)== 3:
                                clear()
                                Encoder.enable()
                                cursor = 0
                                while True:
                                    if Encoder.read()!= None:
                                        cursor = Encoder.read()
                                        shutdownscreen.run(cursor)

                                    if back() == True:
                                        runInterface()

#runInterface()
#GPIO.cleanup()
def runScreen():
    try:
        Encoder.enable()
        while True:
            if Encoder.read()!= None:
                menuscreen.run(Encoder.read())


    finally:
        GPIO.cleanup()


runInterface()
GPIO.cleanup()
