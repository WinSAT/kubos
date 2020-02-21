#!/usr/bin/env python3

import serial
import time
import argparse

# get port name from arguments
parser = argparse.ArgumentParser()
parser.add_argument('--port_name', type=str, default='/dev/ttyS1', help='string name of UART port ex/ /dev/ttyS1')
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

def sendHandler():
	while 1:
		if ser.isOpen():
			message = input('Msg to send: ')
			ser.write(message.encode('utf-8'))
			print("sent message:{}".format(str(message)))

try:
	sendHandler()
except Exception as e:
	print("Exception: {}".format(str(e)))
	ser.flush()
	ser.close()
