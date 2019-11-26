import socket
import fcntl
import struct
import netifaces as ni
from time import sleep
import I2C_LCD_driver
from  Test import *
from LCD2 import *
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

list5 = ["TURN OFF THE SYSTEM?", "        SURE        ", voidstring(), "         NO         "] #shutdownscreen list

def staticOnoffString(): #onoffString function put the State0-State4 value into the onoffscreen list
    staticList2 = ["   PRINTER", "   FAN", "   CAM  ", "   LIGHT ", "   BUZZER"] #staticOnoffscreen list
    return staticList2

def staticSettingsString(): #settingsString function put value into the settingsscreen list
    list3 = ["  FIL. ALERT ", "  TEMP. ALERT ", "  ENDED PRINT ", voidstring()] #settingscreen list
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
settingscreen = DynamicMenu(staticSettingsString())
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
    list0 = ["  PRINTER  CONTROL  ", voidstring(), " PRINTING TIME "+str(hours)+":"+str(minutes),"   IP "+  IpAdress()+" "]
    mainscreen = Screen(list0)
    mainscreen.display()

def runInterface():
    while True:
        stdbyScreen(plateTemp, boxTemp, printerState, lightState, camState, buzzerState)
        if back() == True:#checking sensor
            clear()
            sleep(1)
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
                                dynamicList = ["OFF", "OFF", "OFF", "OFF", "OFF"]
                                clear()
                                Encoder.enable()
                                sleep(0.5)
                                while True:
                                    if Encoder.read()!= None:
                                        cursor = Encoder.read()
                                        onoffscreen.run(dynamicList, cursor)


                                    if back() == True:
                                        runInterface()


                                    if onoffscreen.read(Encoder.button(), cursor) == 0:
                                        if dynamicList[0] == "OFF":
                                            dynamicList[0] = "ON "

                                        elif dynamicList[0] == "ON ":
                                            dynamicList[0] = "OFF"

                                        onoffscreen.run(dynamicList, cursor)

                                    if onoffscreen.read(Encoder.button(), cursor) == 1:
                                        if dynamicList[1] == "OFF":
                                            dynamicList[1] = "ON "

                                        elif dynamicList[1] == "ON ":
                                            dynamicList[1] = "OFF"

                                        onoffscreen.run(dynamicList, cursor)

                                    if onoffscreen.read(Encoder.button(), cursor) == 2:
                                        if dynamicList[2] == "OFF":
                                            dynamicList[2] = "ON "

                                        elif dynamicList[2] == "ON ":
                                            dynamicList[2] = "OFF"

                                        onoffscreen.run(dynamicList, cursor)

                                    if onoffscreen.read(Encoder.button(), cursor) == 3:
                                        if dynamicList[3] == "OFF":
                                            dynamicList[3] = "ON "

                                        elif dynamicList[3] == "ON ":
                                            dynamicList[3] = "OFF"

                                        onoffscreen.run(dynamicList, cursor)

                                    if onoffscreen.read(Encoder.button(), cursor) == 4:
                                        if dynamicList[4] == "OFF":
                                            dynamicList[4] = "ON "

                                        elif dynamicList[4] == "ON ":
                                            dynamicList[4] = "OFF"

                                        onoffscreen.run(dynamicList, cursor)




                            #menuscreen selection block 1
                            if menuscreen.read(Encoder.button(), cursor)== 1:
                                cursor = 0
                                dynamicList = ["OFF", "OFF", "OFF", "   "]
                                clear()
                                Encoder.enable()
                                sleep(0.5)
                                while True:
                                    if Encoder.read()!= None:
                                        cursor = Encoder.read()
                                        settingscreen.run(dynamicList ,cursor)

                                    if back() == True:
                                        runInterface()

                                    if settingscreen.read(Encoder.button(), cursor) == 0:
                                        if dynamicList[0] == "OFF":
                                            dynamicList[0] = "ON "

                                        elif dynamicList[0] == "ON ":
                                            dynamicList[0] = "OFF"

                                        settingscreen.run(dynamicList ,cursor)

                                    if settingscreen.read(Encoder.button(), cursor) == 1:
                                        if dynamicList[1] == "OFF":
                                            dynamicList[1] = "ON "

                                        elif dynamicList[1] == "ON ":
                                            dynamicList[1] = "OFF"

                                        settingscreen.run(dynamicList ,cursor)

                                    if settingscreen.read(Encoder.button(), cursor) == 2:
                                        if dynamicList[2] == "OFF":
                                            dynamicList[2] = "ON "

                                        elif dynamicList[2] == "ON ":
                                            dynamicList[2] = "OFF"

                                        settingscreen.run(dynamicList ,cursor)


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
                                cursor = 0
                                clear()
                                Encoder.enable()
                                sleep(0.5)
                                while True:
                                    if Encoder.read()!= None:
                                        cursor = Encoder.read()
                                        shutdownscreen.run(cursor)

                                    if back() == True:
                                        runInterface()

                                    if cursor == 0:
                                        cursor = 1
                                        shutdownscreen.run(cursor)

                                    if cursor == 2:
                                        cursor = 3
                                        shutdownscreen.run(cursor)

                                    if shutdownscreen.read(Encoder.button(), cursor) == 1:
                                        print("shutdown")

                                    if shutdownscreen.read(Encoder.button(), cursor) == 3:
                                        clear()
                                        runInterface()

runInterface()
GPIO.cleanup()
