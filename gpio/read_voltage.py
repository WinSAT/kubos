#!/usr/bin/env python3

import os
import time

try:
    while 1:
        time.sleep(1)
        # turn off led
        os.system("/sys/bus/iio/devices/iio\:device0/in_voltage{n}_raw")

except KeyboardInterrupt:
    pass

/sys/bus/iio/devices/iio\:device0/in_voltage{n}_raw