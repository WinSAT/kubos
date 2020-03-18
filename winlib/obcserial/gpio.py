#!/usr/bin/env python3

"""
Winsat gpio library for interacting with BBB GPIO pins
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import time
import app_api
import os

class GPIO:

    def __init__(self, pin):
        self.pin = pin
        self.logger = app_api.logging_setup("gpio-service-pin{}".format(self.pin))

    def attach(self):
        try:
            if os.system("echo {} > /sys/class/gpio/export".format(self.pin)) == 0:
                return True
            else:
                self.logger.warning("Error attaching GPIO pin {}. Using fake GPIO...".format(self.pin))
                return False
        except Exception as e:
            self.logger.warning("Error attaching GPIO pin {}: {}. Using fake GPIO...".format(self.pin), str(e))
            return False
    
    def release(self):
        try:
            os.system("echo {} > /sys/class/gpio/unexport".format(self.pin))
            return True
        except Exception as e:
            self.logger.warning("Error releasing GPIO pin {}: {}".format(self.pin), str(e))
            return False

    def on(self):
        try:
            os.system("echo 1 > /sys/class/gpio/gpio{}/value".format(self.pin))
            return True
        except Exception as e:
            self.logger.warning("Error turning on GPIO pin {}: {}".format(self.pin), str(e))
            return False

    def off(self):
        try:
            os.system("echo 0 > /sys/class/gpio/gpio{}/value".format(self.pin))
            return True
        except Exception as e:
            self.logger.warning("Error turning off of GPIO pin {}: {}".format(self.pin), str(e))
            return False

    def direction(self, direction):
        if direction:
            try:
                os.system("echo out > /sys/class/gpio/gpio{}/direction".format(self.pin))
                return True
            except Exception as e:
                self.logger.warning("Error setting direction of GPIO pin {}: {}".format(self.pin), str(e))
                return False
        else:
            try:
                os.system("echo in > /sys/class/gpio/gpio{}/direction".format(self.pin))
                return True
            except Exception as e:
                self.logger.warning("Error setting direction of GPIO pin {}: {}".format(self.pin), str(e))
                return False