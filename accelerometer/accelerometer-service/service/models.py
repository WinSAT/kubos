#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
import serial
import time
import app_api
import struct
from i2c import I2C

class Accelerometer(graphene.ObjectType):

    def __init__(self):
        # global UART
        self.i2c = I2C(bus = 2)
        self.slave_address = 0x53

        self.logger = app_api.logging_setup("accelerometer")

################ queries ###################
    def x(self):
        try:
            # should return accelerometer X value
            self.logger.debug("Requesting x value from accelerometer...")
            data = self.i2c.read(device = self.slave_address, count = 16)
            print("data: {}".format(data))
            print("data unpack: {}".format(struct.unpack(data)))
            print("data float: {}".format(float(data)))
            self.logger.debug("Got value x: {}".format(str(data)))
            return str(data)
        except Exception as e:
            self.logger.warn("Error retrieving x value from accelerometer: {}".format(str(e)))