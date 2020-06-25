#!/usr/bin/env python3

'''
API for interacting with Radio subsystem
'''

import time
import re
import logging
import math

# Adafruit
import board
import busio
import digitalio
import adafruit_rfm69

COMMANDS = { 
    "ping": '\x00'

}


class RADIO:

    def __init__(self, sync_word=b"\x2D\xD4", frequency=915.0):
        """ Initialize radio and serial connection """

        self.logger = logging.getLogger("radio-service")
        self.logger.setLevel(logging.DEBUG)
        
        self.frequency = frequency
        self.sync_word = sync_word

        self.timeout_sec = 60

        #self.baud_rate = 9600

        # set pins
        self.cs = digitalio.DigitalInOut(board.P9_25)
        self.reset = digitalio.DigitalInOut(board.P9_27)
        self.led = digitalio.DigitalInOut(board.P8_8)

        # set pin direction
        self.cs.direction = digitalio.Direction.OUTPUT
        self.reset.direction = digitalio.Direction.OUTPUT
        self.led.direction = digitalio.Direction.OUTPUT

        # setup spi
        self.spi = busio.SPI(board.SCLK_1, board.MOSI_1, board.MISO_1)

        # using Adafruit rfm 69 radio module
        self.radio = adafruit_rfm69.RFM69(self.spi, self.cs, self.reset, self.frequency, sync_word=self.sync_word)

        # set encryption key - must be same on other end at other transceiver
        self.radio.encryption_key = (b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08")

        self.logger.debug("Finished radio initialization.")

    def ping(self):
        """ For testing communications service connection """
        return "pong"
    
    def timeout(self, start_time):
        if (time.time() - start_time > self.timeout_sec):
            return True
        else:
            return False

    def write(self, frame):
        start_time = time.time()
        # keep sending frame until we get confirmed returned acknowledgement
        while (self.radio.send_with_ack(frame) == False):
            # check for timeout
            if self.timeout(start_time):
                self.logger.warn("Timeout trying to write packet to radio.")
                return False
            else:
                continue

        self.logger.debug("Wrote packet to radio: {}".format(frame))
        return True

    def read(self):
        start_time = time.time()
        while (True):
            frame = self.radio.receive()

            # check for timeout
            if self.timeout(start_time):
                self.logger.warn("Timeout trying to read a packet.")
                return False, []

            if frame is None:
                continue
            else:
                break
        
        self.logger.debug("Read packet: {}".format(frame))
        return True, frame
            

    def downlink_image(self, filename):

        with open(filename, "rb") as image:
            f = image.read()
            b = bytearray(f)

            print(b)

            size = 60
            num = math.ceil(len(b)/60)

            # split image into separate frames
            frames = []
            for i in range(num):
                frames.append(b[(i*size):((i+1)*size)])
                print("Frame {}: {}".format(i, frames[i]))

            for n, frame in enumerate(frames):
                while self.radio.send_with_ack(frame) is False:
                    continue
                print("Frame {}/{}".format(n, len(frames)))
                time.sleep(0.1)

            self.radio.send_with_ack(bytearray(b'\x00\x01'))
            print("Sent {}".format(bytearray(b'\x00\x01')))

    # decode radio protocol (AX_25)        
    def decode(self, frame):
        opcode = bytes(frame[:1]).decode('utf-8')
        payload = bytes(frame[1:]).decode('utf-8')

        #opcode = opcode.decode('utf-8')
        #payload = opcode.decode('utf-8')

        self.logger.debug("Decoded packet into opcode: {} payload: {}".format(opcode, payload))
        return opcode, payload

    # encode message into radio protocol for sending (AX_25)
    def encode(self, opcode, payload):
        frame = bytearray()
        frame.extend(bytearray(opcode, 'utf-8'))
        frame.extend(bytearray(payload, 'utf-8'))

        self.logger.debug("Encoded opcode: {} and payload: {} into frame: {}".format(opcode, payload, frame))
        return frame

    def main(self):

        self.logger.info("Starting main loop on radio for receiving packets")
        while (True):
            success, frame = self.read()

            if not success:
                continue

            opcode, payload = self.decode(frame)

            # received ping, send back acknowledgement
            if (opcode == COMMANDS['ping']):
                self.logger.debug("Got 'ping' command from ground station. Returning acknowledgement")
                frame = self.encode(opcode, '\x00')
            else:
                self.logger.warn("Received command/opcode that is not in valid opcodes: {}.".format(opcode))
                continue

            # return acknowledgement
            self.write(frame)

    def __exit__(self):
        pass