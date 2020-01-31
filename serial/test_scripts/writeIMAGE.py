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

def writeImageX():
	stream = open('image.jpg', 'rb')
	modem.send(stream)

def writeImage():
    try:
        if ser.isOpen():

            # wait for image request from client
            while True:
                buffer = ser.readline()
                buffer = buffer.decode('utf-8')
                if buffer == "<<SENDIMAGE>>\n":
                    print("Got message to start image transfer. Got: {}".format(buffer))
                    break
                else:
                    print("Waiting for image request. Got data: {}".format(buffer))

            # send SOF tag
            SOF = "<<SOF>>\n"
            ser.write(SOF.encode('utf-8'))

            # send image data
            data = open("image.jpg","rb").read()
            #print("Sending image data: {}".format(data.encode('utf-8')))
            #ser.write(data.encode('utf-8'))
            data = base64.b64encode(data)
            ser.write(data)

            # send EOF tag
            EOF = "\n<<EOF>>\n"
            #ser.write(EOF.encode('utf-8'))
            ser.write(base64.b64encode(EOF))

            print("Image sent.")
        else:
            print("Could not open serial port: {}".format(args.port_name))
    except Exception as e:
        print("Error trying to write image over serial: {}".format(str(e)))

try:
	writeImageX()
except:
	ser.flush()
	ser.close()
