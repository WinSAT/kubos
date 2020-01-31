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

def writeImage():
    try:
        if ser.isOpen():

            # wait for image request from client
            while True:
                buffer = ser.readline()
                buffer = buffer.decode('utf-8')
                if buffer == "<<SENDIMAGE>>":
                    print("Got message to start image transfer. Got: {}".format(buffer))
                    break
                else:
                    print("Waiting for image request. Got data: {}".format(buffer))

                # send image data
                print("Sending image data: {}".format(open("image.jpg","rb").read()))
                ser.write(open("image.jpg","rb").read())

                # send EOF tag
                ser.write("\n<<EOF>>\n")

                print("Image sent.")
        else:
            print("Could not open serial port: {}".format(args.port_name))
    except Exception as e:
        print("Error trying to write image over serial: {}".format(str(e)))

try:
	writeImage()
except:
	ser.flush()
	ser.close()
