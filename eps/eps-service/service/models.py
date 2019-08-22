#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
import serial

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

class ControlPowerEPS(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )
    power = graphene.Field(PowerState)

class ConfigureHardwareInput(graphene.InputObjectType):
    config = graphene.String()

class ConfigureHardwareEPS(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )
    config = graphene.String()

class TestHardwareInput(graphene.InputObjectType):
    testType = graphene.Field(TestTypeEnum)

class TestHardwareEPS(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )
    results = graphene.Field(TestResults)

class IssueRawCommandInput(graphene.InputObjectType):
    command = graphene.String()

class IssueRawCommandEPS(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )
    ack = graphene.String()

###### ADDITIONAL MODELS FOR EPS ########
class ChargingEnum(graphene.Enum):
    DISCHARGING = 0
    CHARGING = 1

class HeaterEnum(graphene.Enum):
    OFF = 0
    ON = 1
    AUTO = 2

class PowerEnum(graphene.Enum):
    OFF = 0
    ON = 1

class SolarStatus(graphene.ObjectType):
    chargingStatus = graphene.Field(ChargingEnum)
    panelVoltages = graphene.List(graphene.Float)
    panelCurrents = graphene.List(graphene.Float)
    panelTemperatures = graphene.List(graphene.Float)

class PortStatus(graphene.ObjectType):
    power = graphene.List(PowerEnum)
    voltage = graphene.List(graphene.Float)
    current = graphene.List(graphene.Float)

class PowerStatus(graphene.ObjectType):
    voltageLines = graphene.List(graphene.Float) # available voltages on the bus
    measuredLineVoltage = graphene.List(graphene.Float) # actual voltages of available lines
    measuredLineCurrent = graphene.List(graphene.Float) # current for each voltage line

class BatteryStatus(graphene.ObjectType):
    stateOfCharge = graphene.List(graphene.Float)
    chargingStatus = graphene.Field(ChargingEnum)
    voltage = graphene.Float()
    current = graphene.Float()
    temperature = graphene.List(graphene.Float)
    heater = graphene.Field(HeaterEnum)
    heaterMode = graphene.Field(HeaterEnum)

class ControlPortEPS(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )

class ControlPortInput(graphene.InputObjectType):
    power = graphene.Field(PowerEnum)
    port = graphene.Int()

class ControlHeaterEPS(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )

class ControlHeaterInput(graphene.InputObjectType):
    status = graphene.Field(HeaterEnum)

########################################################

class EPS(graphene.ObjectType):

################ mutations #################
    # send a command and if get appropirate response:
    def noop(self):
        return MutationResult(success=True, errors=[])

    # Controls the power state of the EPS
    def controlPower(self, controlPowerInput):
        print("Sending new power state to EPS")

        # change power state of EPS here

        # if successful
        power = PowerState(state=controlPowerInput.state)
        return ControlPowerEPS(success=True, errors=[], power=power)

    def configureHardware(self, configureHardwareInput):
        print("Configuring EPS hardware")

        # perform necessary EPS configuration

        # if successful
        return ConfigureHardwareEPS(success=True, errors=[], config="test")

    def testHardware(self, testHardwareInput):
        print("Testing EPS hardware")

        # perform necessary EPS Testing

        # return results
        results = TestResults(success=True)
        return TestHardwareEPS(success=True, errors=[], results=[])

    def issueRawCommand(self, issueRawCommandInput):
        print("Sending command to EPS")

        # perform actions to send command to EPS

        # return results
        return IssueRawCommandEPS(success=True, errors=[], ack="test")

################### Additional mutations specific to EPS ######################

    def controlPort(self, controlPortInput):
        print("Controlling port on EPS")

        # perform actions to control port on EPS

        # return results
        return ControlPortEPS(success=True, errors=[])

    def controlHeater(self, controlHeaterInput):
        print("Controlling heater on EPS")

        # perform actions to control heater on EPS

        # return results
        return ControlHeaterEPS(success=True, errors=[])

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

################### Additional queries specific to EPS ######################

    def solar(self):
        # get solar status from EPS
        chargingStatus = ChargingEnum.get(1)
        panelVoltages = [1.0, 1.0]
        panelCurrents = [2.0, 2.0]
        panelTemperatures = [3.0, 3.0]
        return SolarStatus(chargingStatus=chargingStatus,
                            panelVoltages=panelVoltages,
                            panelCurrents=panelCurrents,
                            panelTemperatures=panelTemperatures)

    def ports(self):
        power = [PowerEnum.get(1), PowerEnum.get(0)]
        voltage = [1.0, 1.0]
        current = [2.0, 2.0]
        return PortStatus(power=power, voltage=voltage, current=current)

    def power(self):
        voltageLines = [1.0, 1.0]
        measuredLineVoltage = [2.0, 2.0]
        measuredLineCurrent = [3.0, 3.0]
        return PowerStatus(voltageLines=voltageLines,
                            measuredLineVoltage=measuredLineVoltage,
                            measuredLineCurrent=measuredLineCurrent)

    def battery(self):
        stateOfCharge = [1.0, 1.0]
        chargingStatus = ChargingEnum.get(1)
        voltage = 2.0
        current = 3.0
        temperature = [4.0, 4.0]
        heater = HeaterEnum.get(1)
        heaterMode = HeaterEnum.get(0)
        return BatteryStatus(stateOfCharge=stateOfCharge,
                                chargingStatus=chargingStatus,
                                voltage=voltage,
                                current=current,
                                temperature=temperature,
                                heater=heater,
                                heaterMode=heaterMode)

'''
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
'''
