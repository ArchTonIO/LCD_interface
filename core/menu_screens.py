from platforms.printer3d.rotary_encoder_driver import *
from core.LCDscreen import *
from RPi import GPIO
from platforms.printer3d.distance_sensor_driver import *
#temporary variables
sensorState = 1 #state of distance sensor
plateTemp = 43 #heatbed temperature
boxTemp = 34 #box temperature
printerState = "ON"
lightState = "ON"
camState = "ON"
buzzerState = "ON"
pTimeH = 1 #printing time (hours)
pTimeM = 10 #printing time (minutes)


clk = 17
dt = 18
sw = 26

Trigger = 23
Echo = 24
MaxDistance = 300

rotaryEncoder = Rotary(clk, dt, sw)
distanceSensor = Sensor(Trigger, Echo, MaxDistance)

#this functions create the objects and take value to put in it


def stdbyScreen(temp1, temp2, State0, State1, State2, State3):
    list4 = [temp1, temp2, State0, State1, State2, State3]
    stdbyScreen = standByScreen(temp1, temp2, State0, State1, State2, State3)
    stdbyScreen.display()

def mainScreen(hours, minutes):
    list0 = ["  PRINTER  CONTROL  ", voidstring(), "PRINTING TIME "+str(hours)+":"+str(minutes), "   "+"IP "+ IpAdress()+"   "]
    mainscreen = Menu(list0)
    mainscreen.display()

def menuScreen(pointer):
    list1 = ["  ON/OFF MENU", "  SETTINGS", "  MATERIAL SETTINGS", "  SHUTDOWN"]
    menuscreen = Menu(list1)
    menuscreen.display()
    menuscreen.displayPointer(pointer)
    sleep(0.3)

def onoffScreen(State0, State1, State2, State3, State4 ):
    list2 = ["PRINTER  "+State0, "FAN      "+State1, "CAM      "+State2, "LIGHT    "+State3, "BUZZER  "+State4]
    onoffscreen = Menu(list2)
    onoffscreen.display()

def settingsScreen(State5, State6, State7):
    list3 = ["OUT OF FILAMENT "+State5, "TEMP. ALERT "+State6, "ENDED PRINT "+State7]
    settingsscreen = Menu(list3)
    settingsscreen.display()

def materialScreen(selection, val):
    list4a = ["=> PLA (H 50)", "   ABS (H 80)", "   CUSTOM (H " + str(val) + ")"]
    list4b = ["   PLA (H 50)", "=> ABS (H 80)", "   CUSTOM (H " + str(val) + ")"]
    list4c = ["   PLA (H 50)", "   ABS (H 80)", "=> CUSTOM (H " + str(val) + ")"]

    if (selection == "PLA"):
        materialscreen = Menu(list4a)
    if (selection == "ABS"):
        materialscreen = Menu(list4b)
    if (selection == "CUSTOM"):
        materialscreen = Menu(list4c)

    materialscreen.display()

def shutdownScreen():
    list5 = ["TURN OFF THE SYSTEM ?", "        SURE        ", "         NO         "]
    shutdownscreen = Menu(list5)
    shutdownscreen.display()


def runInterface():
    rotaryEncoder.enable()
    while True:
        print (distanceSensor.readDistanceCentimeters())
        if(distanceSensor.readDistanceCentimeters() <= 20):
            while True:
                mainScreen(10, 10)
                if(rotaryEncoder.readSwitch() == 0):
                    clear()
                    rotaryEncoder.enable()
                    while True:
                        print(rotaryEncoder.readRotation())
                        menuScreen(rotaryEncoder.readRotation())

        else:
            stdbyScreen(plateTemp, boxTemp, printerState, lightState, camState, buzzerState)
            
try:
    runInterface()
except:
    GPIO.cleanup()

#runInterface()
