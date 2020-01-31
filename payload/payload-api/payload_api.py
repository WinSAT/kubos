#!/usr/bin/env python3

'''
API for interacting with Payload subsystem
'''

import time
from winserial import uart

#############
# Config Data
DELAY = 1
UART_PORT = '/dev/ttyS1'
TIMEOUT = 1

TELEMETRY = {
    "supervisor": {
        "power_state": {"command": "0001", "length": 2}
    },
    "camera": {
        "capture_image": {"command": "0002", "length": 2}
    }
}
# End Config Data
#############

class Payload:

    def __init__(self, address):
        '''
        Sets the UART number
        '''
        self.UART = uart.UART(UART_PORT, TIMEOUT)

    def write(self, command):
        '''
        Write command used to append proper stop byte to all writes
        '''
        if (type )
