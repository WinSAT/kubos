#!/usr/bin/env python3

import serial
import time
from obcserial import config
from xmodem import XMODEM
import app_api

class UART:
    def __init__(self, port_number):
        self.port = config.PORT_NAME[port_number]
        self.serial = serial.Serial(
            port=self.port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

        # setup xmodem for image transfers
        self.modem = XMODEM(self.getc, self.putc)
    
        self.logger = app_api.logging_setup("UART")

    def getc(self, size, timeout=1):
        return self.serial.read(size) or None

    def putc(self, data, timeout=1):
        return self.serial.write(data) # note that this ignores the timeout

    def transfer_image(self, filename):
        try:
            # open uart port
            self.serial.close()
            self.serial.open()

            if self.serial.isOpen():
                self.logger.debug("UART port {} is open. Waiting for file...".format(self.port))
                stream = open(filename, 'wb+')
                result = self.modem.recv(stream)
                self.serial.close()
                return result
            else:
                self.serial.close()
                self.logger.warn("Could not open serial port for file transfer: {}".format(self.port))
                return False

        except Exception as e:
            self.logger.warn("Exception trying to read file: {} from xmodem stream: {}|{}".format(filename, type(e).__name__,str(e)))
            return False

    # send message to hardware over uart
    def write(self, message):
        try:
            # open uart port
            self.serial.close()
            self.serial.open()

            if self.serial.isOpen():
                # if uart port is open, try to send encoded string message
                self.serial.write(str(message + '\r\n').encode('utf-8'))
                self.serial.close()
                self.logger.debug("UART port {} is open. Sent message: {}".format(self.port, str(message)))
                return True
            else:
                # if could not open uart port, return failure
                self.serial.close()
                self.logger.warn("Could not open serial port: {}".format(self.port))
                return False

        # return failure if exception during write/encoding
        except Exception as e:
            self.logger.warn("Error sending message {} over uart port {}: {}".format(str(message), self.port, str(e)))
            self.serial.close()
            return False

    # get message from hardware over uart
    def read(self):
        try:
            message = None
            self.serial.close()
            self.serial.open()
            if self.serial.isOpen():
                # if uart port is open, try to read something
                message = self.serial.readline()
                message = message.decode('utf-8')
                self.logger.debug("Uart port {} is open. Read line: {}".format(self.port,message))
                self.serial.close()
                return True, message
            else:
                # if could not open uart port, return failure
                self.serial.close()
                self.logger.warn("Could not open serial port: {}".format(self.port))
                return False, None

        # return failure if exception during read/decoding
        except Exception as e:
            self.logger.warn("Error reading message: {} over uart port {}: {}".format(message, self.port, str(e)))
            self.serial.close
            return False, None