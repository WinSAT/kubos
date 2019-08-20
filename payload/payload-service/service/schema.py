#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import Status, Payload

# Local subsystem instance for tracking state
# May not be neccesary when tied into actual hardware
_payload = Payload(power_on=False)

'''
type Query {
    ack(): String
    power(): PowerState
    config(): String
    errors(): [String] # Error descriptions if there are any, or empty if there aren't
    telemetry(): Telemetry
    testResults(): TestResults
}
'''
class Query(graphene.ObjectType):
    payload = graphene.Field(Payload)
    

    def resolve_payload(self, info):

        _payload.refresh()
        return _payload


class PowerOn(graphene.Mutation):
    class Arguments:
        power = graphene.Boolean()

    Output = Status

    def mutate(self, info, power):
        """
        Handles request for payload powerOn mutation
        """

        status = Status(status=True, subsystem=_payload)
        if power is not None:
            status = _payload.set_power_on(power)

        return status

'''
mutation {
    message(message:"hello") {
        status
    }
}
'''
class Message(graphene.Mutation):
    class Arguments:
        message = graphene.String()

    Output = Status

    def mutate(self, info, message):
        # Handles say hello request and sends hello message to pi
        status = _payload.send_message(message)
        return status

'''
# Result of an attemped mutation
interface MutationResult {
    errors: [String]
    success: Boolean
}
'''
class MutationResult(graphene.Interface):
    errors = graphene.List(lambda: String)
    success = graphene.Boolean()

'''
# Simply confirms that the unit is present and talking
type NoopPayload implements MutationResult {
    errors: [String]
    success: Boolean
}
'''
class NoopPayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )


class Noop():
    class Arguments:

    Output = Status

    #def mutate(self, info):

'''
type ControlPowerPayload implements MutationResult {
    errors: [String]
    success: Boolean
    power: PowerState
}
'''
class ControlPowerPayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )

    power = graphene.Field(PowerState)

'''
enum PowerStateEnum {
    ON
    OFF
    RESET
}
'''
class PowerStateEnum(graphene.Enum):
    ON = 1
    OFF = 2
    RESET = 3

'''
input ControlPowerInput {
    state: PowerStateEnum!
}
'''
class ControlPowerInput(graphene.InputObjectType):
    state = graphene.Field(PowerStateEnum)

class controlPower():
    class Arguments:

    Output = Status

    #def mutate(self, info):

'''
type ConfigureHardwarePayload implements MutationResult {
    errors: [String]
    success: Boolean
    config: String
}
'''
class ConfigureHardwarePayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )

    config = graphene.String()

'''
input ConfigureHardwareInput {
    config: String
}
'''
class ConfigureHardwareInput(graphene.InputObjectType):
    config = graphene.String()

class configureHardware():
    class Arguments:

    Output = Status

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
class TestHardwarePayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )

    results = graphene.Field(TestResults)

'''
input TestHardwareInput {
    testType: TestType
}
'''
class TestHardwareInput(graphene.InputObjectType):
    testType = graphene.Field(TestType)

'''
enum TestTypeEnum {
    INTEGRATION
    HARDWARE
    # Add other types as needed
}
'''
class TestTypeEnum(graphene.Enum):
    INTEGRATION = 1
    HARDWARE = 2

class testHardware():
    class Arguments:

    Output = Status

    #def mutate(self, info):

'''
type IssueRawCommandPayload implements MutationResult {
    errors: [String]
    success: Boolean
    ack: String
}
'''
class IssueRawCommandPayload(graphene.ObjectType):
    class Meta:
        interfaces = (MutationResult, )

    ack = graphene.String()

'''
input IssueRawCommandInput {
    # Input for this is really whatever it needs to be for the specific unit, and can be changed accordingly
    command: String
}
'''
class IssueRawCommandInput(graphene.InputObjectType):
    command = graphene.String()


class issueRawCommand():
    class Arguments:

    Output = Status

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
    message = Message.Field()
    power_on = PowerOn.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

'''
















type PowerState {
    state: PowerStateEnum
    uptime: Int
}

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
