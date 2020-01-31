#!/usr/bin/env python3

import serial
import time
import argparse
from xmodem import XMODEM

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

def getc(size, timeout=1):
	return ser.read(size) or None

def putc(data, timeout=1):
	return ser.write(data) # note that this ignores the timeout

modem = XMODEM(getc, putc)

def readImageX():
	stream = open('image.jpg', 'wb')
	modem.recv(stream)

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
				if buffer == "<<SOF>>\n":
					break
				else:
					print("Waiting for SOF for image transfer. Got: {}".format(buffer))

			# start reading image bytes
			count = 0
			with open("image.jpg","wb") as outfile:
				print("Beginning reading of image data...")
				while True:
					try:
						buffer = ser.readline()
						buffer = base64.b64decode(buffer)
						if buffer == "<<EOF>>":
							break
						buffer = "".join(buffer)
						#print(buffer)

						#if buffer == b'\n<<EOF>>\n':
						#	break
						#line = "".join(ser.readline())
						
						outfile.write(buffer)
						#outfile.write(line)
						
						print(count)
						count = count + 1
						'''
						buffer = buffer.decode('utf-8')
						print("Decoded buffer: {}".format(buffer))
						# check if done reading image
						if buffer == "\n<<EOF>>\n":
							print("Got image EOF. Done reading image.")
							break
						'''
					except Exception as e:	
						print("Error: {}".format(str(e)))
						#print("Got data over serial: {}".format(buffer))
						#outfile.write(buffer)
						break
		else:
			print("Could not open serial port: {}".format(args.port_name))
	except Exception as e:
		print("Error trying to read image over serial: {}".format(str(e)))

try:
	#readImage()
	readImageX()
except:
	ser.flush()
	ser.close()
