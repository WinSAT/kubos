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
    payload = graphene.Field(Payload)

    #def resolve_payload(self, info):
    #    _payload.refresh()
    #    return _payload

    #ping = graphene.String()
    #power = graphene.Field(PowerState)
    #config = graphene.String()
    #errors = graphene.List(lambda: String)
    #telemetry = graphene.Field(Telemetry)
    #testResults = graphene.Field(TestResults)

    def resolve_ping(self, info):
        return _payload.ping()

    def resolve_power(self, info):
        power = Payload.objects.get()

    #def resolve_config(self, info):
    #def resolve_errors(self, info):
    #def resolve_telemetry(self, info):
    #def resolve_testResults(self, info):


################## MUTATIONS #################
'''
mutation {
    noop {
        success
        errors
    }
}
        '''
class Noop(graphene.Mutation):
    Output = Result
    def mutate(self, info):
        return _payload.noop()

'''
mutation {
 controlPower(controlPowerInput: {state: ON}) {
    result { success errors }
    power
    }
}
    '''
class ControlPowerInput(graphene.InputObjectType):
    state = graphene.Field(PowerStateEnum)

class ControlPower(graphene.Mutation):
    class Arguments:
        controlPowerInput = ControlPowerInput()

    Output = ControlPowerPayload

    def mutate(self, info, controlPowerInput):
        return _payload.controlPower(controlPowerInput)


'''
type ConfigureHardwarePayload implements MutationResult {
    errors: [String]
    success: Boolean
    config: String
}
'''
#class ConfigureHardwarePayload(graphene.ObjectType):
#    class Meta:
#        interfaces = (MutationResult, )
#
#    config = graphene.String()

'''
input ConfigureHardwareInput {
    config: String
}
'''
#class ConfigureHardwareInput(graphene.InputObjectType):
#    config = graphene.String()

#class configureHardware():
#    class Arguments:

#    Output = Status

    #def mutate(self, info):

'''
# Hardware testing has 2 levels:
# INTEGRATION is to test the FSW's compatibility with the unit
# HARDWARE is to test that the hardware itself is functioning
type TestHardwarePayload implements MutationResult {
    errors: [String]
    success: Boolean
    results: TestResults
}
'''
#class TestHardwarePayload(graphene.ObjectType):
#    class Meta:
#        interfaces = (MutationResult, )

#    results = graphene.Field(TestResults)

'''
input TestHardwareInput {
    testType: TestType
}
'''
#class TestHardwareInput(graphene.InputObjectType):
#    testType = graphene.Field(TestType)

'''
enum TestTypeEnum {
    INTEGRATION
    HARDWARE
    # Add other types as needed
}
'''
#class TestTypeEnum(graphene.Enum):
#    INTEGRATION = 1
#    HARDWARE = 2

#class testHardware():
#    class Arguments:

#    Output = Status

    #def mutate(self, info):

'''
type IssueRawCommandPayload implements MutationResult {
    errors: [String]
    success: Boolean
    ack: String
}
'''
#class IssueRawCommandPayload(graphene.ObjectType):
#    class Meta:
#        interfaces = (MutationResult, )

#    ack = graphene.String()

'''
input IssueRawCommandInput {
    # Input for this is really whatever it needs to be for the specific unit, and can be changed accordingly
    command: String
}
'''
#class IssueRawCommandInput(graphene.InputObjectType):
#    command = graphene.String()


#class issueRawCommand():
#    class Arguments:

#    Output = Status

    #def mutate(self, info):

'''
type Mutation {
    noop(): NoopPayload
    controlPower(
        input: ControlPowerInput!
    ): ControlPowerPayload
    configureHardware(
        input: ConfigureHardwareInput!
    ): ConfigureHardwarePayload
    testHardware(
        input: TestHardwareInput!
    ): TestHardwarePayload
    issueRawCommand(
        input: IssueRawCommandInput!
    ): IssueRawCommandPayload
}
'''
class Mutation(graphene.ObjectType):
    #message = Message.Field()
    #power_on = PowerOn.Field()
    noop = Noop.Field()
    controlPower = ControlPower.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

















'''
type Telemetry {
    nominal: TelemetryNominal
    debug: TelemetryDebug
}

type TelemetryNominal {
    # Telemetry items that are required to know the general status of the hardware
    field1: Float
    # field2: whatever type
    # field3: whatever type
    # ...
}

type TelemetryDebug {
    # Telemetry items that are only useful if actively debugging/diagnosing the system
    field1: Float
    # field2: whatever type
    # field3: whatever type
    # ...
}

type TestResults {
    # Results of last test performed. success, telemetryNominal, and telemetryDebug are always present
    # Additional results can be added as indicated
    success: Boolean
    telemetryNominal: TelemetryNominal
    telemetryDebug: TelemetryDebug
    # results1: any type
    # results2: any type
    # ...
}

'''
