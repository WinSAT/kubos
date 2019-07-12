#!/usr/bin/env python

# Copyright 2017 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

"""
Graphene schema setup to enable queries.
"""

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


class Mutation(graphene.ObjectType):
    """
    Creates mutation endpoints exposed by graphene.
    """

    power_on = PowerOn.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
