#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *

# Local subsystem instance for tracking state
# May not be neccesary when tied into actual hardware
_payload = Payload()

'''
type Query {
    ping(): String
    power(): PowerState
    config(): String
    errors(): [String] # Error descriptions if there are any, or empty if there aren't
    telemetry(): Telemetry
    testResults(): TestResults
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
        return _payload.ping()

    '''
    query {
        ping
    }
    '''
    ack = graphene.String()
    def resolve_ack(self, info):
        return _payload.ack()

    '''
    query {
        power { state }
    }
    '''
    power = graphene.Field(PowerState)
    def resolve_power(self, info):
        return _payload.power()

    '''
    query {
        config
    }
    '''
    config = graphene.String()
    def resolve_config(self, info):
        return _payload.config()

    '''
    query {
        errors
    }
    '''
    errors = graphene.List(graphene.String)
    def resolve_errors(self, info):
        return _payload.errors()

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
        return _payload.telemetry()

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
        return _payload.testResults()

################## MUTATIONS #################
class Noop(graphene.Mutation):
    Output = MutationResult
    def mutate(self, info):
        return _payload.noop()

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

    Output = ControlPowerPayload
    def mutate(self, info, controlPowerInput):
        return _payload.controlPower(controlPowerInput)

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

    Output = ConfigureHardwarePayload
    def mutate(self, info, configureHardwareInput):
        return _payload.configureHardware(configureHardwareInput)

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

    Output = TestHardwarePayload
    def mutate(self, info, testHardwareInput):
        return _payload.testHardware(testHardwareInput)

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

    Output = IssueRawCommandPayload
    def mutate(self, info, issueRawCommandInput):
        return _payload.issueRawCommand(issueRawCommandInput)

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
}
'''
class Mutation(graphene.ObjectType):
    noop = Noop.Field()
    controlPower = ControlPower.Field()
    configureHardware = ConfigureHardware.Field()
    testHardware = TestHardware.Field()
    issueRawCommand = IssueRawCommand.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
