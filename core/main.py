# NOTE: SELECT THE PLATFORM-DEPENDENT DRIVERS BEFORE RUNNING THE CODE.
# EVERY OTHER CODE SHOULD BE UNAWARE OF THE CURRENT PLATFORM.

import sys
from platforms import mockup
from platforms import printer3d

# application's entry point #
if __name__ == "__main__":

    # process command arguments to select which
    # platform dependencies must be used
    if len(sys.argv) < 2:
        platform = printer3d

    elif sys.argv[1] == "-mockup":
        platform = mockup

    else:
        print("unrecognized parameter \"" + sys.argv[1] + "\".")
        exit(-1)

    # use platform
    platform.initialize()
    platform.set_display_text("hello world.")
    platform.set_display_backlighting(False)

    # todo ...
    # intialize menu screens

    # use menu screens

    exit(0)

