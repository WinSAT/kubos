#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
#import Adafruit_BBIO.UART as UART
import serial

class Payload(graphene.ObjectType):
    """
    Model encapsulating subsystem functionality.
    """
    power_on = graphene.Boolean()

    def refresh(self):
        """
        Will hold code for refreshing the status of the subsystem
        model based on queries to the actual hardware.
        """

        print("Querying for payload status")
        self.power_on = not self.power_on

    def set_power_on(self, power_on):
        """
        Controls the power state of the payload
        """

        print("Sending new power state to payload")
        print("Previous State: {}".format(self.power_on))
        print("New State: {}".format(power_on))
        self.power_on = power_on
        return Status(status=True, subsystem=self)

    def send_message(self, message):
        print("Sending message to the pi: " + str(message))
        try:
            #UART.setup("UART1")
            ser = serial.Serial(
                port = '/dev/ttyS1',
                baudrate = 9600,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 1)
            ser.close()
            ser.open()
            if ser.isOpen():
                print("Serial is open. Sending message to the pi.")
                ser.write(str.encode(message));
                ser.close()
                return Status(status=True, subsystem=self)
            else:
                ser.close()
                return Status(status=False, subsystem=self)
        except Exception as e:
            print("Error sending message to pi: " + str(e))
            return Status(status=False, subsystem=self)

class Status(graphene.ObjectType):
    """
    Model representing execution status. This allows us to return
    the status of the mutation function alongside the state of
    the model affected.
    """

    status = graphene.Boolean()
    subsystem = graphene.Field(Payload)
