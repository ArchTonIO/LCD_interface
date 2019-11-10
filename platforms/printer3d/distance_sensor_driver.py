import RPi.GPIO as GPIO
import time

GPIO_TRIGGER = 23
GPIO_ECHO = 24

class Sensor:
    def __init__(self, Trigger, Echo, MaxDistance):
        self.Trigger = Trigger
        self.Echo = Echo
        self.MaxDistance = MaxDistance
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Trigger, GPIO.OUT)
        GPIO.setup(self.Echo, GPIO.IN)

    def readDistanceCentimeters(self):
        GPIO.output(self.Trigger, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.Trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.Echo) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.Echo) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        if distance > self.MaxDistance:
            distance = self.MaxDistance

        return int(distance)

    def readDistancePrecise(self): # to improve
        GPIO.output(self.Trigger, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.Trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.Echo) == 0:
            StartTime = time.time()

        # save arrival time
        while GPIO.input(self.Echo) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance

def TestSensor():
    while True:
        print(distanceSensor.readDistanceCentimeters())
        time.sleep(0.2)
