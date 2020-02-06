#!/usr/bin/env python3

"""
Graphene schema setup to enable queries.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *

# Local subsystem instance for tracking state
# May not be neccesary when tied into actual hardware
_radio = RADIO()

'''
type Query {
    ping(): String
    power(): PowerState
    config(): String
    errors(): [String] # Error descriptions if there are any, or empty if there aren't
    telemetry(): Telemetry
    testResults(): TestResults

####### Additional queries specific to adcs ########
    mode(): String
    orientation(): [Float]
    spin(): [Float]
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
        return _adcs.ping()

    '''
    query {
        ping
    }
    '''
    ack = graphene.String()
    def resolve_ack(self, info):
        return _adcs.ack()

    '''
    query {
        power { state }
    }
    '''
    power = graphene.Field(PowerState)
    def resolve_power(self, info):
        return _adcs.power()

    '''
    query {
        config
    }
    '''
    config = graphene.String()
    def resolve_config(self, info):
        return _adcs.config()

    '''
    query {
        errors
    }
    '''
    errors = graphene.List(graphene.String)
    def resolve_errors(self, info):
        return _adcs.errors()

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
        return _adcs.telemetry()

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
        return _adcs.testResults()

####### Additional queries specific to adcs ########
    '''
    query {
        mode
    }
    '''
    mode = graphene.String()
    def resolve_mode(self, info):
        return _adcs.mode()

    '''
    query {
        orientation
    }
    '''
    orientation = graphene.List(graphene.Float)
    def resolve_orientation(self, info):
        return _adcs.orientation()

    '''
    query {
        spin
    }
    '''
    spin = graphene.List(graphene.Float)
    def resolve_spin(self, info):
        return _adcs.spin()


############## MUTATIONS ################
class Noop(graphene.Mutation):
    Output = MutationResult
    def mutate(self, info):
        return _adcs.noop()

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

    Output = ControlPowerADCS
    def mutate(self, info, controlPowerInput):
        return _adcs.controlPower(controlPowerInput)

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

    Output = ConfigureHardwareADCS
    def mutate(self, info, configureHardwareInput):
        return _adcs.configureHardware(configureHardwareInput)

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

    Output = TestHardwareADCS
    def mutate(self, info, testHardwareInput):
        return _adcs.testHardware(testHardwareInput)

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

    Output = IssueRawCommandADCS
    def mutate(self, info, issueRawCommandInput):
        return _adcs.issueRawCommand(issueRawCommandInput)

################# Extra mutations specific to the ADCS ##############
'''
mutation {
    setMode(setModeInput: {mode: "detumble"
                           configuration: {parameter1: 1.0}})
    {
    errors
    success
    }
}
'''
class SetMode(graphene.Mutation):
    class Arguments:
        setModeInput = SetModeInput()

    Output = SetModeADCS
    def mutate(self, info, setModeInput):
        return _adcs.setMode(setModeInput)

'''
mutation {
    update(updateInput: {time: 1.0
                    gpsLock: [1.0,2.0]})
    {
    errors
    success
    }
}
'''
class Update(graphene.Mutation):
    class Arguments:
        updateInput = UpdateInput()

    Output = UpdateADCS
    def mutate(self, info, updateInput):
        return _adcs.update(updateInput)

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

################# Extra mutations specific to the ADCS ##############
    setMode(
        input: SetModeInput!
    ): SetMode
    update(
        input: UpdateInput
    ): Update
}
'''
class Mutation(graphene.ObjectType):
    noop = Noop.Field()
    controlPower = ControlPower.Field()
    configureHardware = ConfigureHardware.Field()
    testHardware = TestHardware.Field()
    issueRawCommand = IssueRawCommand.Field()

    ################# Extra mutations specific to the ADCS ##############
    setMode = SetMode.Field()
    update = Update.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
