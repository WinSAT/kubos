#!/usr/bin/env python3

"""
Winsat i2c library built on top of built-in Kubos i2c library
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
import serial
import time
import app_api
import smbus

class I2C:

    def __init__(self, bus, slave_address):
        self.slave_address = slave_address
        self.bus = smbus.SMBus(bus)

    def write(self, register_address, data):
	    return self.bus.write_byte_data(self.slave_address, register_address, data)

    def read(self, register_address):
        return self.bus.read_byte_data(self.slave_address, register_address)

class I2C_fake:

    def __init__(self, bus, slave_address):
        pass

    def write(self, register_address, data):
	    return

    def read(self, register_address):
        return 0x00
