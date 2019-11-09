# NOTE: SELECT THE PLATFORM DEPENDENT DRIVERS BEFORE RUNNING THE CODE.
# EVERY OTHER CODE SHOULD BE UNAWARE OF THE CURRENT PLATFORM.

import sys
from platforms.mockup import mockup_platform

# application's entry point #
if __name__ == "__main__":

    # target platform selection
    myPlatform = mockup_platform

    # test
    myPlatform.initialize_platform()
    myPlatform.display_write("hello world.")

    # todo ...

