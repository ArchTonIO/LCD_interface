"""
    This script handles the input/output interface of the
    physical 3d printer platform, which is composed of:

    + 4x20 LCD display (driven by I2C_LCD_driver.py )
    + rotary encoder   (driven by Rotary_encoder_driver.py )
    + distance sensor  (driven by Distance_sensor_driver.py )

"""

def initialize():

    # init all drivers
    # check for init errors (missing device, ...)
    # todo ...

    return

def dispose():

    # todo ...

    return

def set_display_text(string):

    # check for input validity (max length 4*20, automatic line feeds...)
    # communicate with the LCD driver to change the display text
    # todo ...

    return

def set_display_clear():

    # todo ...
    return

def set_display_backlighting(value):

    # communicate with the LCD driver to change the display backlighting
    # todo ...

    return

# takes a callback function that takes an integer argument. such callback
# will be invoked with argument -1 or +1 to indicate the rotary encoder's left or right
# turn respectively, or zero 0 to indicate the rotary encoder's button pressed
def set_rotary_callback(callback):

    # todo ...

    return


def get_distance_sensor():

    # todo ...

    return