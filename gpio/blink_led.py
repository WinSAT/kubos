#!/usr/bin/env python3

import os
import time

try:
    # setup P8.11
    os.system("echo 45 > /sys/class/gpio/export")
    # set pin direction
    os.system("echo out > /sys/class/gpio/gpio45/direction")

    while 1:
        time.sleep(1)
        # turn on led
        os.system("echo 1 > /sys/class/gpio/gpio45/value")
        time.sleep(1)
        # turn off led
        os.system("echo 0 > /sys/class/gpio/gpio45/value")

except KeyboardInterrupt:
    # release pin
    os.system("echo 45 > /sys/class/gpio/unexport")

# get pin value
# cat /sys/class/gpio/gpio45/value

