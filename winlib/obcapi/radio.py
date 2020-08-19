#!/usr/bin/env python3

'''
API for interacting with Radio subsystem
'''

import time
import re
import logging
import math

# Kubos
import app_api

# Adafruit
import board
import busio
import digitalio
import adafruit_rfm69

COMMANDS = { 
    'HEALTH': {
        'ping': '\x00',
        'downlink_all': '\x02',
        'downlink_log': '\x03',
        'clear-database': '\x04',
        'set-system-time': '\x05',
        'get-telemetry': '\x06'
    },
    
    
    'EPS': {
        #'eps_reset':    '\x10',
        #'eps_on':       '\x11',
        #'eps_off':      '\x12',

        'turn-port-on-1':   '\x13',
        'turn-port-on-2':   '\x14',
        'turn-port-on-3':   '\x15',
        'turn-port-off-1':  '\x16',
        'turn-port-off-2':  '\x17',
        'turn-port-off-3':  '\x18'
    },

    'ADCS': {
        'set-adcs-idle':    '\x20',
        'set-adcs-on':      '\x21',
        'set-adcs-off':     '\x22',
        'set-adcs-detumble':'\x23',
        'set-adcs-pointing':'\x24',
        'set-adcs-reset':   '\x25'
    },

    'PAYLOAD': {
        'payload_reset':'\x30',
        'payload_on':   '\x31',
        'payload_off':  '\x32',
        'image_capture':'\x33',
        'image_downlink':'\x34',
    }

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

        # connect to Kubos services
        self.SERVICES = app_api.Services("/etc/kubos-config.toml")

    def ping(self):
        """ For testing communications service connection """
        return "pong"
    
    def timeout(self, start_time):
        if (time.time() - start_time > self.timeout_sec):
            return True
        else:
            return False

    def write(self, packet):
        start_time = time.time()

        frames = []
        if (len(packet) > 60):
            # split into separate frames
            size = 58
            num = math.ceil(len(packet)/size)

            for i in range(num):
                
                frame = packet[(i*size):((i+1)*size)]
                
                if i != (num-1):
                    frame.extend(b'\x11\x11') # continuation bits
                
                frames.append(frame)
                
                #print("Frame {}: {}".format(i, frames[i]))

            for n, frame in enumerate(frames):
                while self.radio.send_with_ack(frame) is False:
                    continue
                #print("Frame {}/{}".format(n, len(frames)))
                time.sleep(0.1)

            self.radio.send_with_ack(bytearray(b'\x00\x01'))
            #print("Sent {}".format(bytearray(b'\x00\x01')))

        else:
            # if small enough, just send all in one frame
            frames = [packet]

        # keep sending frame until we get confirmed returned acknowledgement
        for frame in frames:
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

        self.logger.debug("Decoded packet into opcode: {} payload: {}".format(opcode, payload))
        return opcode, payload

    # encode message into radio protocol for sending (AX_25)
    def encode(self, opcode, result, payload='\x00'):
        frame = bytearray()
        frame.extend(bytearray(opcode, 'utf-8'))
        frame.extend(bytearray(result, 'utf-8'))
        frame.extend(bytearray(payload, 'utf-8'))

        self.logger.debug("Encoded opcode: {} result: {} payload: {} into frame: {}".format(opcode, result, payload, frame))
        return frame

    def start_app(self, app):
        request = ''' mutation { startApp(name: "%s") { success, errors, pid } } ''' % (app)
        response = self.SERVICES.query(service="app-service", query=request)
        # get results
        response = response["startApp"]
        success = response["success"]
        errors = response["errors"]

        if success:
            self.logger.debug("Success started app {} with pid: {}. Return ACK.".format(app, response["pid"]))
            return True, []
        else:
            self.logger.warning("Unable to start app {}: {}. Return NACK".format(app, errors))
            return False, errors
    """
    def health_handler(self, opcode):
        health_dict = COMMANDS['HEALTH']
        if (opcode == health_dict['ping']):
            self.logger.debug("Got 'ping' command from ground station. Returning acknowledgement")
            return True, []

    
    def eps_handler(self, received_opcode):
        for app, opcode in COMMANDS['EPS'].items():
            if (opcode == received_opcode):
                self.logger.debug("Got {} command from ground station.".format(app))
                return self.start_app()

    def adcs_handler(self, received_opcode):
        for app, opcode in COMMANDS['ADCS'].items():
            if (opcode == received_opcode):
                self.logger.debug("Got {} command from ground station.".format(app))

                request = ''' mutation { startApp(name: "%s") { success, errors, pid } } ''' % (app)
                response = self.SERVICES.query(service="app-service", query=request)
                # get results
                response = response["startApp"]
                success = response["success"]
                errors = response["errors"]
                
                if success:
                    self.logger.debug("Success started app {} with pid: {}. Return ACK.".format(app, response["pid"]))
                    return True, []
                else:
                    self.logger.warning("Unable to start app {}: {}. Return NACK".format(app, errors))
                    return False, errors
    """

    def handler(self, command_opcode):
        ''' Handle incoming message/comand '''

        for subsystem in COMMANDS.values():
            for app, opcode in subsystem.items(): 
                if (command_opcode == opcode):
                    # ping doesnt have an app, just return ack
                    if opcode == '\x00':
                        print("Got ping")
                        return True, []
                    else:                  
                        return self.start_app(app)
        
        # didn't find opcode in list of valid opcodes
        self.logger.warning("Command opcode: {} not found in list of valid opcodes".format(command_opcode))
        errors = ["Invalid opcode: {}".format(opcode)]
        self.logger.warn(errors)
        return False, errors

    def main(self):
        self.logger = logging.getLogger("radio-service")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("Starting main loop on radio for receiving packets")
        while (True):
            success, frame = self.read()

            if not success:
                continue

            opcode, payload = self.decode(frame)

            success, errors = self.handler(opcode)

            if success:
                frame = self.encode(opcode, '\x00') # success
            else:
                frame = self.encode(opcode, '\x01', errors) # failure

            #print("Frame", frame, len(frame))
            # return ack/nack
            self.write(frame)

    def __exit__(self):
        pass