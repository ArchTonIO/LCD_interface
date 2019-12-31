import socket
import fcntl
import struct
import os
import I2C_LCD_driver
import netifaces as ni
from time import sleep
from RPi import GPIO
from Test import *
from LCD2 import *
from Sensor import *
from Relay import *
from Serial import *
from Automate import *
from Notifications import*

#temporary variables, queste varabili verranno sostituite con l'implementazione di tutto l'hardware necessario

boxTemp = 34 #box max temperature
pTimeH = 1 #printing time (hours)
pTimeM = 10 #printing time (minutes)
maxBoxTemp = 34

clk = 17
dt = 18
sw = 26

Trigger = 23
Echo = 24
MaxDistance = 300

class VariableValue: #un valore variabile può essere settato ad un nuovo stato o letto al suo stato precedente
    def __init__(self, value):
        self.value = value

    def set(self, newValue):
        self.value = newValue

    def check(self):
        return self.value

#liste per le varie schermate
list1 = ["  ON/OFF MENU", "  SETTINGS", "  MATERIAL SETTINGS", "  SHUTDOWN"]  #menuscreen list
staticList2 = ["   PRINTER", "   FAN", "   CAM  ", "   LIGHT ", "   BUZZER"] #staticOnoffscreen list
staticList3 = ["  FIL. ALERT ", "  TEMP. ALERT ", "  ENDED PRINT ", voidstring()] #settingscreen list
staticList4 = ["  PLA (TEMP 50)", "  ABS (TEMP 80)", voidstring(), voidstring()] #materialscreen list
List5 = ["TURN OFF THE SYSTEM?", "        SURE        ", voidstring(), "         NO         "] #shutdownscreen list

#oggetti sensore
Encoder = Rotary(dt, clk, sw)
distanceSensor = Sensor(Trigger, Echo, MaxDistance)

#oggetti schermate(Menu, DynamicMenu)
menuscreen = Menu(list1)
onoffscreen = DynamicMenu(staticList2)
settingscreen = DynamicMenu(staticList3)
materialscreen = DynamicMenu(staticList4)
shutdownscreen = Menu(List5)

#oggetti flag
minBedTemp = VariableValue(18) #la temperatura minima del piatto è settata a 18 (prova)
printerState = VariableValue("OFF")
fanState = VariableValue("OFF")
camState = VariableValue("OFF")
lightState = VariableValue("OFF")
buzzerState = VariableValue("OFF")
filAlert = VariableValue("OFF")
tempAlert = VariableValue("OFF")
endedPrint = VariableValue("OFF")

def back():
    if distanceSensor.readDistanceCentimeters() < 20:
        clear()
        return True

def stdbyScreen(temp1, temp2, State0, State1, State2, State3):
    list4 = [temp1, temp2, State0, State1, State2, State3]
    stdbyScreen = standByScreen(temp1, temp2, State0, State1, State2, State3)
    stdbyScreen.display()

def mainScreen(hours, minutes):
    list0 = ["  PRINTER  CONTROL  ", voidstring(), " PRINTING TIME "+str(hours)+":"+str(minutes)," IP "+  IpAdress()+" "]
    mainscreen = Screen(list0)
    mainscreen.display()

def runInterface():
    turnOffAll()
    while True:

        Controller = TemperatureController("heatbed", "fan", minBedTemp.check(), maxBoxTemp)#viene creato un nuovo controller delle temperature
        plateTemp = getTemp() #heatbed temperature
        Controller.checkAndEnable(plateTemp, boxTemp)
        stdbyScreen(plateTemp, boxTemp, printerState.check(), lightState.check(), camState.check(), buzzerState.check())#la schermata di standby è creata e aggiornata
        print ("executing the non-interactive block")

        if back() == True:#checking sensor
            clear()
            sleep(1)
            while True:
                    print("the interactive execution has started")
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
                                dynamicList = [printerState.check(), fanState.check(), camState.check(), lightState.check(), buzzerState.check()]
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
                                            printerState.set("ON ")
                                            #setPrinter(1)

                                        elif dynamicList[0] == "ON ":
                                            dynamicList[0] = "OFF"
                                            #setPrinter(0)
                                            printerState.set("OFF")

                                        onoffscreen.run(dynamicList, cursor)

                                    if onoffscreen.read(Encoder.button(), cursor) == 1:
                                        if dynamicList[1] == "OFF":
                                            dynamicList[1] = "ON "
                                            fanState.set("ON ")

                                        elif dynamicList[1] == "ON ":
                                            dynamicList[1] = "OFF"
                                            fanState.set("OFF")

                                        onoffscreen.run(dynamicList, cursor)

                                    if onoffscreen.read(Encoder.button(), cursor) == 2:
                                        if dynamicList[2] == "OFF":
                                            dynamicList[2] = "ON "
                                            camState.set("ON ")

                                        elif dynamicList[2] == "ON ":
                                            dynamicList[2] = "OFF"
                                            camState.set("OFF")

                                        onoffscreen.run(dynamicList, cursor)

                                    if onoffscreen.read(Encoder.button(), cursor) == 3:
                                        if dynamicList[3] == "OFF":
                                            dynamicList[3] = "ON "
                                            lightState.set("ON ")

                                        elif dynamicList[3] == "ON ":
                                            dynamicList[3] = "OFF"
                                            lightState.set("OFF")

                                        onoffscreen.run(dynamicList, cursor)

                                    if onoffscreen.read(Encoder.button(), cursor) == 4:
                                        if dynamicList[4] == "OFF":
                                            dynamicList[4] = "ON "
                                            buzzerState.set("ON ")

                                        elif dynamicList[4] == "ON ":
                                            dynamicList[4] = "OFF"
                                            buzzerState.set("OFF")

                                        onoffscreen.run(dynamicList, cursor)




                            #menuscreen selection block 1
                            if menuscreen.read(Encoder.button(), cursor)== 1:
                                cursor = 0
                                dynamicList = [filAlert.check(), tempAlert.check(), endedPrint.check(), "   "]
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
                                            filAlert.set("ON ")

                                        elif dynamicList[0] == "ON ":
                                            dynamicList[0] = "OFF"
                                            filAlert.set("OFF")

                                        settingscreen.run(dynamicList ,cursor)

                                    if settingscreen.read(Encoder.button(), cursor) == 1:
                                        if dynamicList[1] == "OFF":
                                            dynamicList[1] = "ON "
                                            tempAlert.set("ON ")

                                        elif dynamicList[1] == "ON ":
                                            dynamicList[1] = "OFF"
                                            tempAlert.set("OFF")

                                        settingscreen.run(dynamicList ,cursor)

                                    if settingscreen.read(Encoder.button(), cursor) == 2:
                                        if dynamicList[2] == "OFF":
                                            dynamicList[2] = "ON "
                                            endedPrint.set("ON ")

                                        elif dynamicList[2] == "ON ":
                                            dynamicList[2] = "OFF"
                                            endedPrint.set("OFF")

                                        settingscreen.run(dynamicList ,cursor)


                            #menuscreen selection block 2
                            if menuscreen.read(Encoder.button(), cursor)== 2:
                                dynamicList = ["   ", "   ", "   ", "   "]
                                clear()
                                Encoder.enable()
                                cursor = 0
                                while True:
                                    if Encoder.read()!= None:
                                        cursor = Encoder.read()
                                        materialscreen.run(dynamicList, cursor)

                                    if back() == True:
                                        runInterface()

                                    if materialscreen.read(Encoder.button(), cursor) == 0:
                                        if dynamicList[0] == "   ":
                                            dynamicList[0] = "<=="
                                            dynamicList[1] = "   "
                                            minBedTemp.set(25)

                                        elif dynamicList[0] == "<==":
                                            dynamicList[0] = "   "

                                        materialscreen.run(dynamicList ,cursor)

                                    if materialscreen.read(Encoder.button(), cursor) == 1:
                                        if dynamicList[1] == "   ":
                                            dynamicList[1] = "<=="
                                            dynamicList[0] = "   "
                                            minBedTemp.set(10)

                                        elif dynamicList[1] == "<==":
                                            dynamicList[1] = "   "

                                        materialscreen.run(dynamicList ,cursor)

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
                                        clear()
                                        mylcd.lcd_display_string("  SHUTTING DOWN", 2, 0)
                                        i = 0
                                        while i < 3:
                                            mylcd.lcd_display_string(".", 2, 15 + i)
                                            i = i + 1
                                            sleep(1)
                                        clear()
                                        mylcd.backlight(0)
                                        os.system("shutdown -h now");

                                    if shutdownscreen.read(Encoder.button(), cursor) == 3:
                                        clear()
                                        runInterface()

runInterface()
GPIO.cleanup()
