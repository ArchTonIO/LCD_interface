"""
    This script provides a mock-up GUI that simulates the physical input/output interface
    of the 3d printer, with the purpose of testing other modules without having
    the actual printer's hardware available.

    NOTE: this is my best attempt to execute a QApplication outside the main thread (which is usually
          not recommended by Qt) that keeps automatically updating in response of the main thread calls.
          This was necessary since for non-mockup platforms, the platform itself is supposed to be
          controlled by the main thread, and not the opposite.

    NOTE 2: not quite sure about thread-safety of the global context.

"""

import threading
from time import sleep

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# display state variables #
__DISPLAY_SIZE   = (4, 20)  # display size in (rows, columns)
__display_cursor = (0,  0)  # display cursor coordinates in (row, column)
__display_string = ""
__display_backlighting = True

# rotary encoder state variables #
# todo ...

# sonar sensor state variables #
# todo ...

# global context lock
# todo ...

# internal function that initializes the GUI via Qt libraries.
def __async_exec_gui__():

    app = QApplication([])

    # window
    window = QWidget()
    window.setWindowTitle("mockup")
    window.setFixedSize(230, 130)

    # 20x4 lcd display with a monospace font
    display = QPlainTextEdit()
    display.setFixedWidth(170)
    display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    display.setEnabled(False)
    font = QFont()
    font.setFamily("Courier")
    display.setFont(font)
    display.setPlainText("")

    # rotary encoder
    rotary_left   = QPushButton('<-')
    rotary_center = QPushButton(' ')
    rotary_right  = QPushButton('->')

    # layout
    layout = QGridLayout()           # y  x  h  w
    layout.addWidget(display,       0, 0, 1, 3)
    layout.addWidget(rotary_left,   1, 0, 1, 1)
    layout.addWidget(rotary_center, 1, 1, 1, 1)
    layout.addWidget(rotary_right,  1, 2, 1, 1)
    window.setLayout(layout)
    window.show()

    # function that updates the view according to the various state variables
    def update_view():
        global __display_cursor, __display_string, __display_backlighting

        # todo incomplete ...

        display.setPlainText(__display_string)
        return

    # create timer for continuous updates during the event loop
    timer = QTimer()
    timer.timeout.connect(update_view)
    timer.start()

    # execute application's event loop (code doesn't execute past there)
    app.exec_()
    return


# initializes platform
def initialize_platform():

    # initialize and execute gui in side thread
    x = threading.Thread(target=__async_exec_gui__, args=())
    x.start()
    return

# ...
def display_write(s):
    global __display_string
    __display_string = s
    # todo incomplete ...

def display_clear(string):
    global __display_string
    __display_string = ""
    # todo incomplete ...

def set_on_rotary_left_callback(callback):
    # todo ...
    return

def set_on_rotary_rigth_callback(callback):
    # todo ...
    return

def set_on_rotary_center_callback(callback):
    # todo ...
    return

