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
from adafruit_fxos8700 import FXOS8700
from winserial import I2C

class Accelerometer(graphene.ObjectType):

    def __init__(self):
        # global UART
        i2c = I2C(bus = 2)
        self.sensor = adafruit_bno055.BNO055(i2c)

        self.slave_address = 0x53

        self.logger = app_api.logging_setup("accelerometer")

################ queries ###################
    def x(self):
        try:
            # should return accelerometer X value
            #self.logger.debug("Requesting x value from accelerometer...")
            #data = self.i2c.read(device = self.slave_address, count = 16)
            #print("data: {}".format(data))
            #print("data unpack: {}".format(struct.unpack(data)))
            #print("data float: {}".format(float(data)))
            #self.logger.debug("Got value x: {}".format(str(data)))
            #return str(data)
            i2c = I2C(board.SCL, board.SDA)
            sensor = adafruit_fxos8700.FXOS8700(i2c)

            while True:
                accel_x, accel_y, accel_z = sensor.accelerometer
                mag_x, mag_y, mag_z = sensor.magnetometer
                print('Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(accel_x, accel_y, accel_z))
                print('Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(mag_x, mag_y, mag_z))
                time.sleep(1.0)

        except Exception as e:
            self.logger.warn("Error retrieving x value from accelerometer: {}".format(str(e)))



