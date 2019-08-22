#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
import serial

'''
enum PowerStateEnum {
    ON
    OFF
    RESET
}
'''
class PowerStateEnum(graphene.Enum):
    OFF = 0
    ON = 1
    RESET = 2

class PowerState(graphene.ObjectType):
    state = graphene.Field(PowerStateEnum)

class Result(graphene.ObjectType):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

class ControlPowerPayload(graphene.ObjectType):
    result = graphene.Field(Result)
    power = graphene.Field(PowerState)

class Payload(graphene.ObjectType):
    power = graphene.Field(PowerState, default_value=PowerState(state=PowerStateEnum(0)))
    config = graphene.String()
    errors = graphene.List(graphene.String)
    #telemetry = graphene.Field(Telemetry)
    #testResults = graphene.Field(TestResults)

################ mutations #################
    # send a command and if get appropirate response:
    def noop(self):
        return Result(success=True, errors=[])

    # Controls the power state of the payload
    def controlPower(self, controlPowerInput):
        print("Sending new power state to payload")
        print("Previous State: {}".format(self.power.state.name))

        # change power state of payload here

        # if successful
        self.power = PowerState(state=controlPowerInput.state)
        self.result = Result(errors=[],success=True)
        #print("New State: {}".format())
        return ControlPowerPayload(result=self.result,power=self.power)
        #return True

################ queries ###################
    def ping():
        return "pong"

    def refresh(self):
        """
        Will hold code for refreshing the status of the subsystem
        model based on queries to the actual hardware.
        """

        print("Querying for payload status")
        self.power_on = not self.power_on



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
