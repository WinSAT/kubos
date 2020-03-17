#!/usr/bin/env python3

'''
API for interacting with EPS subsystem
'''

import time
import re
from obcserial import gpio
import app_api

class EPS:

    def __init__(self):

        self.logger = app_api.logging_setup("eps-service")

        # initialize GPIO pins
        self.PORT1 = gpio.GPIO(66)
        self.PORT2 = gpio.GPIO(69)
        self.PORT3 = gpio.GPIO(45)

        # attach GPIO pins
        self.PORT1.attach()
        self.PORT2.attach()
        self.PORT3.attach()

        # set GPIO direction
        self.PORT1.direction(1)
        self.PORT2.direction(1)
        self.PORT3.direction(1)    

    # turn on output voltage sources
    def turnON1(self):
        self.PORT1.on()
    def turnON2(self):
        self.PORT2.on()
    def turnON3(self):
        self.PORT3.on()

    # turn off output voltage sources
    def turnOFF1(self):
        self.PORT1.off()
    def turnOFF2(self):
        self.PORT2.off()
    def turnOFF3(self):
        self.PORT3.off()

    # release GPIO pins
    def __exit__(self):
        self.PORT1.release()
        self.PORT2.release()
        self.PORT3.release()