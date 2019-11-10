#Pwm suitable pin:
    #GPIO.1_______(BCM 18)
    #GPIO.23______(BCM 13) [Distance sensor]
    #GPIO.24______(BCM 24)
    #GPIO.26______(BCM 12)

from RPi import GPIO
from time import sleep


class Rotary:
    def __init__(self, clk, dt, sw):
        self.clk = clk
        self.dt = dt
        self.sw = sw
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def enable(self):
        self.clkLastState = GPIO.input(self.clk)
        self.counter = 0

    def readRotation(self):
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)

        if self.clkLastState != clkState:
            sleep(0.04)
            if clkState == dtState:

                self.counter = self.counter + 1
            else:

                self.counter = self.counter - 1


        if self.counter < 0:
             self.counter = 0


        if self.counter > 3:
             self.counter = 3

        return self.counter



    def readSwitch(self):
        return GPIO.input(self.sw)

def TestRotary():
    rotary = Rotary(17, 18, 26)
    rotary.enable()
    sleep(1)
    while True:
        print(rotary.readRotation())
