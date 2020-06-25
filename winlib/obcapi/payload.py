#!/usr/bin/env python3

'''
API for interacting with Payload subsystem
'''

import time
import re
from obcserial import uart
from obcapi import config
import app_api

class Payload:

    def __init__(self):

        self.logger = app_api.logging_setup("payload-api")
        self.use_uart = False
        try: 
            self.UART = uart.UART(1)
            self.use_uart = True
        except Exception as e:
            self.logger.error("FATAL ERROR: Unable to open UART port {}:{}. No communication with payload. Using fake connection...".format(type(e).__name__, str(e)))

    def read(self):
        if self.use_uart:
            success, message = self.UART.read()
            if success:
                return self.unpack(message)
            return None
        else:
            return self.unpack(input("Enter fake serial input:"))

    def send_command(self, command):
        if self.write(command):
            for i in range(config.RETRY):
                response = self.read()
                if response == config.RETURN_CODE[0]:
                    self.logger.info("Got back {} message from payload sending command: {}.".format(response, command))
                    return True
                elif response == config.RETURN_CODE[1]:
                    self.logger.warn("Got back {} message from payload sending command: {}.".format(response, command))
                    return False
            return False
        else:
            self.logger.warn("Error writing {} over UART.".format(command))
            return False

    def read_result(self, expected_response):
        for i in range(config.RETRY):
            response = self.read()
            if response == expected_response:
                self.logger.info("Got back successful {} message from payload.".format(response))
                return True
            elif response == config.RETURN_CODE[1]:
                self.logger.warn("Got back {} message from payload sending command.".format(response))
                return False
            else:
                self.logger.warn("Got back {} message from payload but expecting: {}.".format(response, expected_response))
        return False

    def pack(self, message):
        return "<<" + message + ">>"
    
    def unpack(self, message):
        commands = re.findall(config.REGEX, message)
        if len(commands) != 0:
            return commands[0]
        else:
            return None

    def write(self, command):
        if self.use_uart:
            return self.UART.write(self.pack(command))
        else:
            print(self.pack(command))
            return True

    def read_image(self, filename):
        return self.UART.transfer_image(filename)

    
######## QUERIES AND MUTATIONS ################
    def ping(self):
        return "pong"
        # should send hardware a ping and expect a pong back
        #try:
        #    command = "ping"
        #    response = "pong"
        #    if self.send_command(command):
        #        if self.read_result(response):
        #            return True, []
        #        else:
        #            return False, ["Payload did not send back sucessful result from {}".format(command)]
        #    return False, ["Could not send payload successful {}".format(command)]
        #
        #except Exception as e:
        #    return False, [str(e)]

    def image_capture(self):
        # should send request to capture an image
        try:
            command = "capture_image"
            response = config.RETURN_CODE[2]
            if self.send_command(command):
                if self.read_result(response):
                    return True, []
                else:
                    return False, ["Payload did not send back successful result from {}".format(command)]
            return False, ["Could not send payload successful {}".format(command)]

        except Exception as e:
            return False, [str(e)]

    def image_transfer(self):
        # should send request to start image transfer and then open a stream to read image
        try:
            command = "transfer_image"
            response = config.RETURN_CODE[2]
            if self.send_command(command):
                time.sleep(1)
                self.write("START")
                if self.read_image("/home/kubos/images/image.jpg"):
                    if self.read_result(response):
                        return True, []
                    else:
                        return False, ["Payload did not send back successful result from {}".format(command)]
                else:
                    return False, ["Error trying to read image from Payload."]
            return False, ["Could not send payload successful {}".format(command)]

        except Exception as e:
            return False, [str(e)]