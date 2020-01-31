#!/usr/bin/env python3

import serial
import time
import argparse

# get port name from arguments
parser = argparse.ArgumentParser()
parser.add_argument('--port_name', type=str, default='/dev/ttyS1', help='string of port name ex/ /dev/ttyS1')
args = parser.parse_args()

# serial setup
ser = serial.Serial(
	port=args.port_name,
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)

time.sleep(1)
ser.close()
ser.open()

def readImage():
	try:
		if ser.isOpen():
			print('Sending request for image...')
			message = "<<SENDIMAGE>>\n"
			ser.write(message.encode('utf-8'))

			# get initial SOF tag
			while True:
				buffer = ser.readline()
				buffer = buffer.decode('utf-8')
				if buffer == "<<SOF>>":
					break
				else:
					print("Waiting for SOF for image transfer. Got: {}".format(buffer))

			# start reading image bytes
			with open("image.jpg","wb") as outfile:
				while True:
					buffer = ser.readline()
					buffer = buffer.decode('utf-8')

					# check if done reading image
					if buffer == "<<EOF>>":
						print("Got image EOF. Done reading image.")
						break
					else:
						print("Got data over serial: {}".format(buffer))
						outfile.write(buffer)
		else:
			print("Could not open serial port: {}".format(args.port_name))
	except Exception as e:
		print("Error trying to read image over serial: {}".format(str(e)))

try:
	readImage()
except:
	ser.flush()
	ser.close()
