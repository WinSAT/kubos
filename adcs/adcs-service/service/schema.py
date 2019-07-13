#!/usr/bin/env python3

"""
Graphene schema setup to enable queries.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import Status, Adcs

# Local subsystem instance for tracking state
# May not be neccesary when tied into actual hardware
_adcs = Adcs(power_on=False)


class Query(graphene.ObjectType):
    """
    Creates query endpoints exposed by graphene.
    """

    adcs = graphene.Field(Adcs)

    def resolve_adcs(self, info):
        """
        Handles request for adcs subsystem query.
        """

        _adcs.refresh()
        return _adcs


class PowerOn(graphene.Mutation):
    """
    Creates mutation for Adcs.PowerOn
    """

    class Arguments:
        power = graphene.Boolean()

    Output = Status

    def mutate(self, info, power):
        """
        Handles request for adcs powerOn mutation
        """

        status = Status(status=True, subsystem=_adcs)
        if power is not None:
            status = _adcs.set_power_on(power)

        return status


class Mutation(graphene.ObjectType):
    """
    Creates mutation endpoints exposed by graphene.
    """

    power_on = PowerOn.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
'''
type Query {
    mode(): String
    orientation(): [Float]
    spin(): [Float]
}

type Mutation {
    setMode(
        input: SetModeInput!
    ): SetModePayload
    update(
        input: UpdateInput
    ): UpdatePayload
}

type SetModePayload implements MutationResult {
    errors: [String]
    success: Boolean
}

input SetModeInput {
    mode: String
    configuration: ModeConfiguration
}

# Whatever is needed for the ADCS to enter a mode
type ModeConfiguration {
    parameter1: Float
    # parameter2: any type
    # parameter3: any type
    # ...
}

type UpdatePayload implements MutationResult {
    errors: [String]
    success: Boolean
}

input UpdateInput {
    time: Float
    gpsLock: [Float]
    # whatever else needs to be updated for the unit to function properly
}
'''
