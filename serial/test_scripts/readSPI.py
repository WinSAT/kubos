#!/usr/bin/env python3

import serial
import time
import argparse
from spi import SPI

# get port name from arguments
#parser = argparse.ArgumentParser()
#parser.add_argument('--port_name', type=str, default='/dev/ttyS1', help='string of port name ex/ /dev/ttyS1')
#args = parser.parse_args()

# spi setup
spi = SPI("/dev/spidev1.0")
spi.mode = SPI.MODE_0
spi.bits_per_word = 8
spi.speed = 500000
#received = spi.transfer([0x11, 0x22, 0xFF])
#spi.write([0x12, 0x34, 0xAB, 0xCD])

def readHandler():
	while 1:
		time.sleep(1)
		try:
			received = spi.read(10)
			print("Read from spi bus: {}".format(str(received)))
		except Exception as e:
			print("Error reading from spi bus: {}".format(str(e)))
			
try:
	readHandler()
except Exception as e:
	print("Error reading from spi bus: {}".format(str(e)))
