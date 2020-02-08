#!/usr/bin/env python3

'''
API for interacting with Payload subsystem
'''

import time
from winserial import uart
import app_api
import logging

#############
# Config Data
DELAY = 1
UART_PORT = '/dev/ttyS1'
TIMEOUT = 1

# RETURN CODES FROM PAYLOAD
SUCCESS = "<<00>>"
FAILURE = "<<01>>"

COMMANDS = {
    "ping": "<<ping>>",
    "ImageTransfer": "<<imgcap>>",
    "ImageCapture": "<<imgtra>>"
}
# End Config Data
#############

logger = logging.getLogger('payload-service')
class Payload:

    def __init__(self):
        try:
            self.UART = uart.UART(UART_PORT, TIMEOUT)

        except Exception as e:
            logger.warn("Unable to open uart port: {}. Will use fake UART api...".format(UART_PORT))
            self.UART = uart.UART_fake()

    def write(self, command):
        '''
        Write command to payload
        '''
        try:
            # check if inputted command is valid
            if command not in COMMANDS:
                return False, ["Inputted command not valid. Make sure command is defined in payload api."]

            # if valid command
            else:    
                # write command over UART with padding
                self.UART.write(COMMANDS[command])
                
                # wait for response 
                time.sleep(DELAY)

                # read response from payload
                response = self.UART.read()
                
                # check return code
                if response == SUCCESS:
                    return True, []
                elif response == FAILURE:
                    return False, ["Payload returned failure return code."]
                else:
                    return False, ["Payload returned invalid return code."]
                    
        except Exception as e:
            return False, [("Exception while writing to payload over UART: {}.".format(str(e)))]

    def ping(self):
        # should send hardware a ping and expect a pong back
        success, errors = self.UART.write(COMMANDS["ping"])
        # return results
        return success, errors

    def image_capture(self):
        # should send hardware a ping and expect a pong back
        success, errors = self.UART.write(COMMANDS["ImageCapture"])
        # return results
        return success, errors

    def image_transfer(self):
        # should send hardware a ping and expect a pong back
        success, errors = self.UART.write(COMMANDS["ImageTransfer"])

        if success:
            # open stream for image transfer
            return self.UART.readImage()
        else:
            return success, errors