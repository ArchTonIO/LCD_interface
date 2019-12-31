#Pwm suitable pin:
    #GPIO.1_______(BCM 18) [Distance sensor trigger for plate movement]
    #GPIO.23______(BCM 13) [Distance sensor trigger for lcd interface]
    #GPIO.24______(BCM 24) [Distance sensor echo for lcd interface]
    #GPIO.26______(BCM 12) [Distance sensor echo for plate movement]

#in questo file i due moduli più importanti sono Temporizer e TemperatureController,sono i moduli che rendono possibile
#l'automazione del controllo dei tempi di stampa e dei controlli delle temperature.



import time
import RPi.GPIO as GPIO
from Relay import *
from Sensor import *
from Notifications import *

movementSensor_trig = 23
movementSensor_echo = 24
maxDistance = 300

sensor = Sensor(movementSensor_trig, movementSensor_echo, maxDistance)

#oggetti alert (notifications)
alert0 = Notification("Filament Alert !")
alert1 = Notification("Temperature Alert !")
alert2 = Notification("The printer has stopped !")


def getCurrentTime(): #questa funzione restituisce l'ora attuale nel formato (ad esempio) 14,30
    timeHours = time.strftime("%H")
    timeMinutes = time.strftime("%M")
    timeStr = timeHours + "." + timeMinutes
    timeFloat = float(timeStr)
    return timeFloat

class Temporizer: #il temporizer restutuisce a fine stampa il tempo di stampa totale
    def __init__(self, sensor):

        self.movementSensor = sensor#il sensore usato per leggere la distanza del piatto
        self.lastDistance = 0#ultima distanza registrata dal sensore
        self.startTime = 0#tempo registrato all'inizio della stampa
        self.stopTime = 0#tempo registrato alla fine della stampa
        self.totalTime = 0#tempo totale di stampa
        self.startSemaphore = 0#semaforo di inizio stampa: se è = 0 la stampa non è iniziata, se è = 1, sì

    def enable(self):#enable inizializza i valori del temporizer: la prima distanza letta del piatto e il semaforo di inizio stampa
        self.lastDistance = self.movementSensor.readDistanceCentimeters()
        self.startSemaphore = 0

    def check(self):
        #se la stampa non era ancora partita e la distanza registrata è diversa dall'ultima, allora la stampa è iniziata,
        #assegna a startTime l'ora corrente nel formato di getCurrentTime()
        if self.startSemaphore != 1:
            if self.movementSensor.readDistanceCentimeters() != self.lastDistance  or self.movementSensor.readDistanceCentimeters() != (self.lastDistance + 2) or self.movementSensor.readDistanceCentimeters() != (self.lastDistance - 2):
                self.startTime = getCurrentTime()
                self.startCounter = 1

        #se la stampa è iniziata e il valore cambia di nuovo, tornando quello iniziale, il piatto è di nuovo al suo posto:
        #la stampa è finita, assegna stopTime al tempo corrente nel formato di getCurrentTime() e calcola il tempo di stampa
        #totale con tempo finale - tempo iniziale
        if self.startSemaphore == 1:
            if self.movementSensor.readDistanceCentimeters() == self.lastDistance or self.movementSensor.readDistanceCentimeters() == (self.lastDistance + 2) or self.movementSensor.readDistanceCentimeters() == (self.lastDistance - 2):
                self.stopTime = getCurrentTime()
                self.totalTime = self.stopTime - self.startTime
                alert2.send()  #invia la notifica di fine stampa tramite mail

        output = str(self.totalTime)
        if len(output) > 4:
            shifted = output[0] + output[1] + output[2] + output[3]

        else:
            shifted = output

        return shifted

class TemperatureController :
    def __init__(self, relay0, relay1, activationTemp0, activationTemp1):#prende i due relay attivatori, e le loro relative
        self.relay0 = relay0                                             #temperature d'attivazione
        self.relay1 = relay1
        self.activationTemp0 = activationTemp0
        self.activationTemp1 = activationTemp1
        self.counter0 = 0 #i contatori hanno lo scopo di tenere conto della quantità di volte che uno o l'altro relay è stato attivato
        self.counter1 = 0

    def reset(self): #reset class function reset counters
        self.counter0 = 0
        self.counter1 = 0

    def checkAndEnable(self, temp0, temp1): #questa funzione effettua l'attivazione o meno dei relay
        if self.relay0 != "heatbed" and self.relay0 != "fan":
            print("Error: relay must be heatbed or fan type!")

        if self.relay1 != "heatbed" and self.relay1 != "fan":
            print("Error: relay must be heatbed or fan type!")

        if self.relay0 == "heatbed":

            if temp0 < self.activationTemp0:
                setHeatbed(1)
                self.counter0 += 1

            else:
                setHeatbed(0)

        if self.relay0 == "fan":

            if temp1 > self.activationTemp1:
                #setFan(1)
                self.counter1 += 1

            else:
                #setFan(0)
                pass

        if self.relay1 == "heatbed":

            if temp0 < self.activationTemp0:
                setHeatbed(1)
                self.counter0 += 1

            else:
                setHeatbed(0)

        if self.relay1 == "fan":

            if temp1 > self.activationTemp1:
                #setFan(1)
                self.counter1 += 1

            else:
                #setFan(0)
                pass

    def checkTimes(self):#questa funzione torna i contatori degli utilizzi relay
        return str(self.counter0) + str(self.counter1)

def testTemporizer():
    temporizer = Temporizer(sensor)
    temporizer.enable()
    while True:
        print(temporizer.check())
        time.sleep(1)
