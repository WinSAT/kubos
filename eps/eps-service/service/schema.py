#!/usr/bin/env python3

"""
Graphene schema setup to enable queries.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *

_eps = EPS()

'''
type Query {
    ping(): String
    power(): PowerState
    config(): String
    errors(): [String] # Error descriptions if there are any, or empty if there aren't
    telemetry(): Telemetry
    testResults(): TestResults

####### Additional queries specific to EPS ########
    solar(): SolarStatus
    ports(): PortStatus
    power(): PowerStatus
    battery(): BatteryStatus
}
'''
class Query(graphene.ObjectType):

    '''
    query {
        ping
    }
    '''
    ping = graphene.String()
    def resolve_ping(self, info):
        return _eps.ping()

    '''
    query {
        ping
    }
    '''
    ack = graphene.String()
    def resolve_ack(self, info):
        return _eps.ack()

    '''
    query {
        power { state }
    }
    '''
    power = graphene.Field(PowerState)
    def resolve_power(self, info):
        return _eps.power()

    '''
    query {
        config
    }
    '''
    config = graphene.String()
    def resolve_config(self, info):
        return _eps.config()

    '''
    query {
        errors
    }
    '''
    errors = graphene.List(graphene.String)
    def resolve_errors(self, info):
        return _eps.errors()

    '''
    query {
        telemetry {
            nominal { field1nominal field2nominal }
            debug { field1debug field2debug }
            }
    }
    '''
    telemetry = graphene.Field(Telemetry)
    def resolve_telemetry(self, info):
        return _eps.telemetry()

    '''
    query {
    testResults {
     telemetryNominal { field1nominal field2nominal }
     telemetryDebug { field1debug field2debug }
     success
     results1
     results2
    }
    }
    '''
    testResults = graphene.Field(TestResults)
    def resolve_testResults(self, info):
        return _eps.testResults()

####### Additional queries specific to EPS ########

    '''
    query {
    solar {
        chargingStatus
        panelVoltages
        panelCurrents
        panelTemperatures
        }
    }
    '''
    solar = graphene.Field(SolarStatus)
    def resolve_solar(self, info):
        return _eps.solar()

    '''
    query {
    ports {
        power
        voltage
        current
        }
    }
    '''
    ports = graphene.Field(PortStatus)
    def resolve_ports(self, info):
        return _eps.ports()

    '''
    query {
    power {
        voltageLines
        measuredLineVoltage
        measuredLineCurrent
        }
    }
    '''
    power = graphene.Field(PowerStatus)
    def resolve_power(self, info):
        return _eps.power()

     '''
    query {
    battery {
        stateOfCharge
        chargingStatus
        voltage
        current
        temperature
        heater
        heaterMode
        }
    }
    '''
    battery = graphene.Field(BatteryStatus)
    def resolve_battery(self, info):
        return _eps.battery()

############## MUTATIONS ################
class Noop(graphene.Mutation):
    Output = MutationResult
    def mutate(self, info):
        return _eps.noop()

'''
mutation {
    controlPower(controlPowerInput: {state: OFF}) {
        success
        errors
        power { state }
        }
    }
'''
class ControlPower(graphene.Mutation):
    class Arguments:
        controlPowerInput = ControlPowerInput()

    Output = ControlPowerEPS
    def mutate(self, info, controlPowerInput):
        return _eps.controlPower(controlPowerInput)

'''
mutation {
     configureHardware(configureHardwareInput: {config: "test"}) {
        success
        errors
        config
    }
}
'''
class ConfigureHardware(graphene.Mutation):
    class Arguments:
        configureHardwareInput = ConfigureHardwareInput()

    Output = ConfigureHardwareEPS
    def mutate(self, info, configureHardwareInput):
        return _eps.configureHardware(configureHardwareInput)

# Hardware testing has 2 levels:
# INTEGRATION is to test the FSW's compatibility with the unit
# HARDWARE is to test that the hardware itself is functioning
'''
mutation {
 testHardware(testHardwareInput: {testType: HARDWARE}) {
    success
    errors
    results {
    success
    telemetryNominal { field1nominal field2nominal }
    telemetryDebug { field1debug field2debug }
    results1
    results2
    }
}
}
'''
class TestHardware(graphene.Mutation):
    class Arguments:
        testHardwareInput = TestHardwareInput()

    Output = TestHardwareEPS
    def mutate(self, info, testHardwareInput):
        return _eps.testHardware(testHardwareInput)

'''
mutation {
     issueRawCommand(issueRawCommandInput: {command: "go"}) {
        success
        errors
        ack
    }
}
'''
class IssueRawCommand(graphene.Mutation):
    class Arguments:
        issueRawCommandInput = IssueRawCommandInput()

    Output = IssueRawCommandEPS
    def mutate(self, info, issueRawCommandInput):
        return _eps.issueRawCommand(issueRawCommandInput)

################# Extra mutations specific to the EPS ##############
'''
mutation {
    controlPort(controlPortInput: {
                power: ON
                port: 1 })
    {
    errors
    success
    }
}
'''
class ControlPort(graphene.Mutation):
    class Arguments:
        controlPortInput = ControlPortInput()

    Output = ControlPortEPS
    def mutate(self, info, controlPortInput):
        return _eps.controlPort(controlPortInput)

'''
mutation {
    controlHeater(controlHeaterInput: {
                status: ON })
    {
    errors
    success
    }
}
'''
class controlHeater(graphene.Mutation):
    class Arguments:
        controlHeaterInput = ControlHeaterInput()

    Output = ControlHeaterEPS
    def mutate(self, info, controlHeaterInput):
        return _eps.controlHeater(controlHeaterInput)


####################################################################
'''
type Mutation {
    noop(): Noop
    controlPower(
        input: ControlPowerInput!
    ): ControlPower
    configureHardware(
        input: ConfigureHardwareInput!
    ): ConfigureHardware
    testHardware(
        input: TestHardwareInput!
    ): TestHardware
    issueRawCommand(
        input: IssueRawCommandInput!
    ): IssueRawCommand

################# Extra mutations specific to the EPS ##############
    controlPort(
        input: ControlPortInput!
    ): ControlPortPayload
    controlHeater(
        input: ControlHeaterInput!
    ): ControlHeaterPayload
}
'''
class Mutation(graphene.ObjectType):
    noop = Noop.Field()
    controlPower = ControlPower.Field()
    configureHardware = ConfigureHardware.Field()
    testHardware = TestHardware.Field()
    issueRawCommand = IssueRawCommand.Field()

    ################# Extra mutations specific to the EPS ##############
    controlPort = ControlPort.Field()
    controlHeater = controlHeater.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
