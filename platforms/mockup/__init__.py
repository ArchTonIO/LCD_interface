"""
    This package provides a mock-up GUI that simulates the input/output interface
    of the physical 3d printer, with the purpose of testing other modules without
    requiring the actual printer platform to be connected.

    NOTE: this is my best attempt to execute a QApplication outside the main thread (which is usually
          not recommended by Qt) that keeps automatically updating in response of the main thread calls.
          This was necessary since for non-mockup platforms, the platform itself is supposed to be
          controlled by the main thread, and not the opposite.
"""

from threading import Thread, Lock

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

__mutex = Lock()           # mutex must be acquired before read/write any of the following
                            # global context variables

__is_view_updated = True  # flag that represents if the GUI view needs to be updated

# display state variables #
__DISPLAY_SIZE_ROWS    = 4
__DISPLAY_SIZE_COLUMNS = 20
__display_string = ""
__display_backlighting = True
__display_custom_chars = []

# rotary encoder state variables #
# todo ...

# sonar sensor state variables #
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
    display.setStyleSheet("background-color: rgb(255, 255, 255);")

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
        global __mutex, __is_view_updated
        global __display_cursor, __display_string, __display_backlighting

        __mutex.acquire()

        # update view (display's text & backlighting)
        if not __is_view_updated:

            display.setPlainText(__display_string)

            # todo: string formatting

            if __display_backlighting:
                display.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                display.setStyleSheet("background-color: rgb(0, 0, 0);")

        __is_view_updated = True

        __mutex.release()
        return

    # create timer for continuous updates during the event loop
    timer = QTimer()
    timer.timeout.connect(update_view)
    timer.start()

    # execute application's event loop (code doesn't execute past there)
    app.exec_()
    return


# initializes interface
def initialize():

    # initialize and execute gui in side thread
    x = Thread(target=__async_exec_gui__, args=())
    x.start()

    return


def set_display_text(s):
    global __mutex, __is_view_updated, __display_string

    __mutex.acquire()

    if __display_string != s:
        __display_string = s
        __is_view_updated = False

    __mutex.release()
    return

def display_clear(string):
    set_display_text("")
    return

def set_display_backlighting(value):
    global __mutex, __is_view_updated, __display_backlighting

    __mutex.acquire()

    if __display_backlighting != value:
        __display_backlighting = value
        __is_view_updated = False

    __mutex.release()
    return

def set_on_rotary_left_callback(callback):
    # todo ...
    return

def set_on_rotary_rigth_callback(callback):
    # todo ...
    return

def set_on_rotary_center_callback(callback):
    # todo ...
    return

