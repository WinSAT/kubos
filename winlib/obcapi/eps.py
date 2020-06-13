#!/usr/bin/env python3

'''
API for interacting with EPS subsystem
'''

import time
import re
from obcserial import gpio
import logging

class EPS:

    def __init__(self):

        self.logger = logging.getLogger("eps-service")

        # initialize GPIO pins
        self.PORT1 = gpio.GPIO(66)
        self.PORT2 = gpio.GPIO(69)
        self.PORT3 = gpio.GPIO(45)

        self.fake_GPIO = True

        self.PORT1.release()
        self.PORT2.release()
        self.PORT3.release()

        # attach GPIO pins
        if self.PORT1.attach():
            if self.PORT2.attach():
                if self.PORT3.attach():
                    self.fake_GPIO = False

        if self.fake_GPIO == False:
            # set GPIO direction
            self.PORT1.direction(1)
            self.PORT2.direction(1)
            self.PORT3.direction(1)    

            # make sure everything is off
            self.PORT1.off()
            self.PORT2.off()
            self.PORT3.off()

        self.power1 = False # power to output 1 off
        self.power2 = False # power to output 2 off
        self.power3 = False # power to output 3 off

        self.battery_level = 0  # initialize battery as emtpy (full is 100)

    # control power of ports
    def controlPort(self, controlPortInput):
        if self.fake_GPIO:
            if (controlPortInput.power == 1):
                self.power1 = True
            elif (controlPortInput.power == 2):
                self.power2 = True
            elif (controlPortInput.power == 3):
                self.power3 = True
            return True
          
        if (controlPortInput.port == 1):
            if (controlPortInput.power == 1):
                self.PORT1.on()
                self.power1 = True
            else:
                self.PORT1.off()
                self.power1 = False
            return True
        elif (controlPortInput.port == 2):
            if (controlPortInput.power == 1):
                self.PORT2.on()
                self.power2 = True
            else:
                self.PORT2.off()
                self.power2 = False
            return True
        elif (controlPortInput.port == 3):
            if (controlPortInput.power == 1):
                self.PORT3.on()
                self.power3= True
            else:
                self.PORT3.off()
                self.power3 = False
            return True
        else:
            return False

    # get power state of all ports
    def power(self):
        return self.power1, self.power2, self.power3

    # get current battery level as percentage
    def battery(self):

        # read ADC to get current battery level
        self.battery_level = 100

        return self.battery_level

    # release GPIO pins
    def __exit__(self):
        if self.fake_GPIO == False:
            self.PORT1.release()
            self.PORT2.release()
            self.PORT3.release()