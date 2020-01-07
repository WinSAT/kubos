#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
import serial

# send message to payload over serial
def send_message(self, message):
    print("Sending message to the payload: " + str(message))
    try:
        # UART.setup("UART1")
        ser = serial.Serial(
            port='/dev/ttyS1',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)
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
        return Status(status=False, subsystem=self)s


class TelemetryNominal(graphene.ObjectType):
    # telemetry items for general status of hardware
    field1nominal = graphene.Float()
    field2nominal = graphene.Float()

class TelemetryDebug(graphene.ObjectType):
    # telemetry items for general status of hardware
    field1debug = graphene.Float()
    field2debug = graphene.Float()

class Telemetry(graphene.ObjectType):
    nominal = graphene.Field(TelemetryNominal)
    debug = graphene.Field(TelemetryDebug)

class TestResults(graphene.ObjectType):
    # results of last test performed
    success = graphene.Boolean()
    telemetryNominal = graphene.Field(TelemetryNominal)
    telemetryDebug = graphene.Field(TelemetryDebug)
    results1 = graphene.String()
    results2 = graphene.String()

class PowerStateEnum(graphene.Enum):
    OFF = 0
    ON = 1
    RESET = 2

class TestTypeEnum(graphene.Enum):
    INTEGRATION = 1
    HARDWARE = 2
    # add other types as needed

class PowerState(graphene.ObjectType):
    state = graphene.Field(PowerStateEnum)

class MutationResult(graphene.Interface):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

class ControlPowerInput(graphene.InputObjectType):
    state = graphene.Field(PowerStateEnum)

class ControlPowerPayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )
    power = graphene.Field(PowerState)

class ConfigureHardwareInput(graphene.InputObjectType):
    config = graphene.String()

class ConfigureHardwarePayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )
    config = graphene.String()

class TestHardwareInput(graphene.InputObjectType):
    testType = graphene.Field(TestTypeEnum)

class TestHardwarePayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )
    results = graphene.Field(TestResults)

class IssueRawCommandInput(graphene.InputObjectType):
    command = graphene.String()

class IssueRawCommandPayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )
    ack = graphene.String()

class Payload(graphene.ObjectType):

################ mutations #################
    # send a command and if get appropirate response:
    def noop(self):
        return MutationResult(success=True, errors=[])

    # Controls the power state of the payload
    def controlPower(self, controlPowerInput):
        print("Sending new power state to payload")

        # change power state of payload here

        # if successful
        power = PowerState(state=controlPowerInput.state)
        return ControlPowerPayload(success=True, errors=[], power=power)

    def configureHardware(self, configureHardwareInput):
        print("Configuring payload hardware")

        # perform necessary payload configuration

        # if successful
        return ConfigureHardwarePayload(success=True, errors=[], config="test")

    def testHardware(self, testHardwareInput):
        print("Testing payload hardware")

        # perform necessary payload Testing

        # return results
        results = TestResults(success=True)
        return TestHardwarePayload(success=True, errors=[], results=[])

    def issueRawCommand(self, issueRawCommandInput):
        print("Sending command to payload")

        # perform actions to send command to payload

        # return results
        return IssueRawCommandPayload(success=True, errors=[], ack="test")

################ queries ###################
    def ping(self):
        # should send hardware a ping and expect a pong back
        return "pong"

    def ack(self):
        # return some String
        return "test"

    def power(self):
        # return power state (for now just return ON)
        return PowerState(state=PowerStateEnum.get(1))

    def config(self):
        return "test"

    def errors(self):
        # error descriptions if any
        return []

    def telemetry(self):
        # get telemetry from hardware
        nominal = TelemetryNominal(field1nominal=0.1, field2nominal=0.2)
        debug = TelemetryDebug(field1debug=1.2, field2debug=4.5)
        return Telemetry(nominal=nominal, debug=debug)

    def testResults(self):
        # get test_results from hardware
        telemetryNominal = TelemetryNominal(field1nominal=0.1, field2nominal=0.2)
        telemetryDebug = TelemetryDebug(field1debug=1.2, field2debug=4.5)
        return TestResults(success=True, telemetryNominal=telemetryNominal,
        telemetryDebug=telemetryDebug, results1="pass", results2="fail")