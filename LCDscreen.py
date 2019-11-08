import socket
import fcntl
import struct
import netifaces as ni
import time
import I2C_LCD_driver

fontdata0 = [

        [0x1F, 0x1F, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],#0 upper left

        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],#1 null

        [0x1F, 0x1F, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03],#2 per right

        [0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03],#3 center right

        [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],#4 center left

        [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x1F, 0x1F],#5 bottom left

        [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F],#6 Full

        [0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x1F, 0x1F],#7 bottom right
]

displayPosition = [0x80, 0xC0, 0x94, 0xD4]

#FIRST POSITION IN LCD_DISPLAY_STRING AND IN OTHER LCD FUNCTIONS IS RAWS, THE SECOND IS COLUMNS,
#RAWS STARTS AT 1, COLUMNS STARTS AT 0

mylcd =  I2C_LCD_driver.lcd()

class Menu:#to create a menu with an input string list
    def __init__(self, list): # "list" is the string list input
        self.list = list

    def display(self):
        i = 1
        while(i < len(self.list)):#while cycle selects the i+1 raw of the lcd Screen
            for x in self.list:#for cycle selects the string "x" in the string list, and print it on the display in the "i" raw
                mylcd.lcd_display_string(x, i,0)#i = raws, 0 = columns
                i = i+1
    def displayPointer(self, pointer):
        mylcd.lcd_load_custom_chars(fontdata0)
        mylcd.lcd_write(displayPosition[pointer])
        mylcd.lcd_write_char(6)

class SquareImage:#to create the different square simbol, take type for the component type and state for its state
    def __init__(self, type, state):
        self.type = type
        self.state = state

    def display(self):
        if(self.state == "ON" and self.type == "printer" ):
            mylcd.lcd_load_custom_chars(fontdata0) #display the rectangle with the "P" letter inside
            mylcd.lcd_write(0x81)
            mylcd.lcd_write_char(0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(2)
            mylcd.lcd_write(0xC1)
            mylcd.lcd_write_char(4)
            mylcd.lcd_write(0xC3)
            mylcd.lcd_write_char(3)
            mylcd.lcd_write(0x95)
            mylcd.lcd_write_char(5)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(7)
            mylcd.lcd_display_string("P", 2, 2)
        if (self.state == "OFF" and self.type == "printer" ):
            mylcd.lcd_load_custom_chars(fontdata0) #display nothing in the rectangle area(using null char)
            mylcd.lcd_write(0x81)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xC1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xC3)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0x95)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
        if (self.state == "ON" and self.type == "light"):
            mylcd.lcd_load_custom_chars(fontdata0)#display the rectangle with the "L" letter inside
            mylcd.lcd_write(0x86)
            mylcd.lcd_write_char(0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(2)
            mylcd.lcd_write(0xC6)
            mylcd.lcd_write_char(4)
            mylcd.lcd_write(0xC8)
            mylcd.lcd_write_char(3)
            mylcd.lcd_write(0x9A)
            mylcd.lcd_write_char(5)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(7)
            mylcd.lcd_display_string("L", 2, 7)
        if (self.state == "OFF" and self.type == "light"):
            mylcd.lcd_load_custom_chars(fontdata0) #display nothing in the rectangle area(using null char)
            mylcd.lcd_write(0x86)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xC6)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xC8)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0x9A)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
        if (self.state == "ON" and self.type == "cam"):
            mylcd.lcd_load_custom_chars(fontdata0)#display the rectangle with the "C" letter inside
            mylcd.lcd_write(0x8B)
            mylcd.lcd_write_char(0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(2)
            mylcd.lcd_write(0xCB)
            mylcd.lcd_write_char(4)
            mylcd.lcd_write(0xCD)
            mylcd.lcd_write_char(3)
            mylcd.lcd_write(0x9F)
            mylcd.lcd_write_char(5)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(7)
            mylcd.lcd_display_string("C", 2, 12)
        if (self.state == "OFF" and self.type == "cam"):
            mylcd.lcd_load_custom_chars(fontdata0) #display nothing in the rectangle area(using null char)
            mylcd.lcd_write(0x8B)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xCB)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xCD)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0x9F)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
        if (self.state == "ON" and self.type == "buzzer"):
            mylcd.lcd_load_custom_chars(fontdata0)#display the rectangle with the "B" letter inside
            mylcd.lcd_write(0x90)
            mylcd.lcd_write_char(0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(2)
            mylcd.lcd_write(0xD0)
            mylcd.lcd_write_char(4)
            mylcd.lcd_write(0xD2)
            mylcd.lcd_write_char(3)
            mylcd.lcd_write(0xA4)
            mylcd.lcd_write_char(5)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(7)
            mylcd.lcd_display_string("B", 2, 17)
        if (self.state == "OFF" and self.type == "buzzer"):
            mylcd.lcd_load_custom_chars(fontdata0) #display nothing in the rectangle area(using null char)
            mylcd.lcd_write(0x90)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xD0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xD2)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xA4)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)

class standByScreen: #standby screen shows what component is actually active and displays bed and box temperature
    def __init__ (self, temp1, temp2, State0, State1, State2, State3):
        self.temp1 = temp1
        self.temp2 = temp2
        self.State0 = State0
        self.State1 = State1
        self.State2 = State2
        self.State3 = State3
    def display(self): #val is the same as the Menu class

        printerimage = SquareImage("printer", self.State0)
        printerimage.display()
        lightimage = SquareImage("light", self.State1)
        lightimage.display()
        camimage = SquareImage("cam", self.State2)
        camimage.display()
        buzzerimage = SquareImage("buzzer", self.State3)
        buzzerimage.display()
        mylcd.lcd_display_string("BED:"+str(self.temp1), 4, 1)
        mylcd.lcd_display_string("BOX:"+str(self.temp2), 4, 13)

def voidstring():
    voidString = "                    "
    return voidString

def clear():#clear() call the lcd_clear function of I2C_lcd_driver
    mylcd.lcd_clear()

def IpAdress(): #shows the pi ip adress
    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    return ip  # should print "192.168.100.37"

def printTime(posR, posC, shift): #Print time, "shift" argument used to display hours like "12::50" or "12:50"
    while True:
        if (shift == False):
            mylcd.lcd_display_string(time.strftime("%H:%M"),posR,posC)
        else:
            mylcd.lcd_display_string(time.strftime("%H::%M"),posR,posC)
