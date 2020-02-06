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
    "ping": {"<<ping>>"},
    "capture_image": {"<<imgcap>>"},
    "transfer_image": {"<<imgtra>>"}
}
# End Config Data
#############

class PayloadAPI:

    def __init__(self):
        '''
        Sets the UART number
        '''
        logger = logging.getLogger("payload-service")

        try:
            self.UART = uart.UART(UART_PORT, TIMEOUT)
        except Exception as e:
            logger.warn("Unable to open uart port: {}. Will use local payload api...".format(UART_PORT))
            self.UART = uart.UART_fake(SUCCESS)

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
