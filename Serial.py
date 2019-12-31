import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 9600


def getTemp():
    ser.close()
    ser.open()
    ser.write(b"A")#carattere di start per leggere le temperature da arduino
    Temp = int(ser.readline().strip())
    return Temp
