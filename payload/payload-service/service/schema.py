#!/usr/bin/env python3

"""
Graphene schema setup to enable queries.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene

from .models import Status, Payload

# Local subsystem instance for tracking state
# May not be neccesary when tied into actual hardware
_payload = Payload(power_on=False)

class Query(graphene.ObjectType):
    """
    Creates query endpoints exposed by graphene.
    """

    payload = graphene.Field(Payload)

    def resolve_payload(self, info):
        """
        Handles request for subsystem query.
        """

        _payload.refresh()
        return _payload


class PowerOn(graphene.Mutation):
    """
    Creates mutation for Payload.PowerOn
    """

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

class Message(graphene.Mutation):
    class Arguments:
        message = graphene.String()

    Output = Status

    def mutate(self, info, message):
        # Handles say hello request and sends hello message to pi
        status = _payload.send_message(message)
        return status

class Mutation(graphene.ObjectType):
    """
    Creates mutation endpoints exposed by graphene.
    """
    message = Message.Field()
    power_on = PowerOn.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

'''
type Query {
    ack(): String
    power(): PowerState
    config(): String
    errors(): [String] # Error descriptions if there are any, or empty if there aren't
    telemetry(): Telemetry
    testResults(): TestResults
}

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

# Result of an attemped mutation
interface MutationResult {
    errors: [String]
    success: Boolean
}

# Simply confirms that the unit is present and talking
type NoopPayload implements MutationResult {
    errors: [String]
    success: Boolean
}

type ControlPowerPayload implements MutationResult {
    errors: [String]
    success: Boolean
    power: PowerState
}

input ControlPowerInput {
    state: PowerStateEnum!
}

enum PowerStateEnum {
    ON
    OFF
    RESET
}

type ConfigureHardwarePayload implements MutationResult {
    errors: [String]
    success: Boolean
    config: String
}

input ConfigureHardwareInput {
    config: String
}

# Hardware testing has 2 levels:
# INTEGRATION is to test the FSW's compatibility with the unit
# HARDWARE is to test that the hardware itself is functioning
type TestHardwarePayload implements MutationResult {
    errors: [String]
    success: Boolean
    results: TestResults
}

input TestHardwareInput {
    testType: TestType
}

enum TestTypeEnum {
    INTEGRATION
    HARDWARE
    # Add other types as needed
}

type IssueRawCommandPayload implements MutationResult {
    errors: [String]
    success: Boolean
    ack: String
}

input IssueRawCommandInput {
    # Input for this is really whatever it needs to be for the specific unit, and can be changed accordingly
    command: String
}
'''
