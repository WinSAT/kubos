#!/usr/bin/env python3

import serial
import time
import argparse
from i2c import I2C
import struct

# get address name from arguments
parser = argparse.ArgumentParser()
#parser.add_argument('address', type=str, help='address number to read from')
#parser.add_argument('num_read', type=int, help='number of bytes to read')
args = parser.parse_args()

# i2c setup
i2c_device = I2C(bus = 2)
slave_address = 0x53
num_read = 16

def readHandler():
	print("Getting value over i2c from address: {}".format(slave_address))
	data = i2c_device.read(device = slave_address, count = num_read)
	print("Got value x: {}".format(str(data)))
	print("data: {}".format(data))
	print("data unpack: {}".format(struct.unpack(data)))
	print("data float: {}".format(float(data)))

try:
	readHandler()
except Exception as e:
	print("Exception trying to read from i2c: {}".format(str(e)))