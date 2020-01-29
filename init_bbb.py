#!/usr/bin/env python3

import subprocess
from IPython import embed

def run(cmd):
	return subprocess.check_output(cmd, shell=True)

def call(cmd):
	subprocess.call(cmd.split())

usbDevicesList = run('ls /dev | grep ttyUSB').decode().split('\n')

print(usbDevicesList)
deviceIdx = int(input('Select index number of device to use: '))
print(usbDevicesList[0])
call('sudo slattach -s 115200 -p cslip /dev/{} &'.format(usbDevicesList[deviceIdx]))
call('sudo ifconfig sl0 192.168.0.1 pointopoint 192.168.0.2 up')
call('sudo slattach -s 115200 -p cslip /dev/{} &'.format(usbDevicesList[deviceIdx]))
call('sudo ifconfig sl0 192.168.0.1 pointopoint 192.168.0.2 up')
call('sudo slattach -s 115200 -p cslip /dev/{} &'.format(usbDevicesList[deviceIdx]))
call('sudo ifconfig sl0 192.168.0.1 pointopoint 192.168.0.2 up')

call('sudo route add 192.168.0.1 dev lo')

print('Complete! Now run `ssh kubos@192.168.0.2`, pass: Kubos123')
