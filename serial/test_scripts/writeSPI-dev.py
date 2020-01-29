#!/usr/bin/env python3

import argparse
import spidev
import time

# get port name from arguments
#parser = argparse.ArgumentParser()
#parser.add_argument('--port_name', type=str, default='/dev/ttyS1', help='string of port name ex/ /dev/ttyS1')
#args = parser.parse_args()

# spi setup
spi = spidev.SpiDev() # create spi object
spi.open(1,0) # open spi port 0, device (CS) 1
spi.max_speed_hz = 500000
spi.mode = 0b00

def sendHandler():
	try:
		while True:
			user_input = input("Push any key to send data over spi: ")
			vals = [0x01,0x02,0x03]
			print("Writing to SPI bus: {}".format(vals))
			resp = spi.writebytes(vals) # transfer one byte
			print("Got back response: {}".format(str(resp)))
			time.sleep(1.0) # sleep for 1 seconds
	except KeyboardInterrupt: # Ctrl+C pressed, so…
		spi.close() # … close the port before exit

try:
	sendHandler()
except Exception as e:
	print("Error writing to spi bus: {}".format(str(e)))
	spi.close() # … close the port before exit
