#!/usr/bin/env python3

import time
import argparse
import spidev

# get port name from arguments
#parser = argparse.ArgumentParser()
#parser.add_argument('--port_name', type=str, default='/dev/ttyS1', help='string of port name ex/ /dev/ttyS1')
#args = parser.parse_args()

# spi setup
spi = spidev.SpiDev()
bus = 1
spi.open(bus,0)
spi.mode = 0b00
spi.max_speed_hz = 500000

def readHandler():
	while 1:
		time.sleep(1)
		try:
			received = spi.readbytes(3) # transfer one byte
			#if (received[0] != 255):
			print("Read from spi bus: {}".format(str(received)))
		except Exception as e:
			print("Error reading from spi bus: {}".format(str(e)))
			
try:
	print("Starting read from SPI bus {}".format(bus))
	readHandler()
except Exception as e:
	print("Error reading from spi bus: {}".format(str(e)))
