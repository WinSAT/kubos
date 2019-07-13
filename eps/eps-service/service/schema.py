#!/usr/bin/env python3

"""
Graphene schema setup to enable queries.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import Status, Eps

# Local subsystem instance for tracking state
# May not be neccesary when tied into actual hardware
_eps = Eps(power_on=False)


class Query(graphene.ObjectType):
    """
    Creates query endpoints exposed by graphene.
    """

    eps = graphene.Field(Eps)

    def resolve_eps(self, info):
        """
        Handles request for subsystem query.
        """

        _eps.refresh()
        return _eps


class PowerOn(graphene.Mutation):
    """
    Creates mutation for Eps.PowerOn
    """

    class Arguments:
        power = graphene.Boolean()

    Output = Status

    def mutate(self, info, power):
        """
        Handles request for eps powerOn mutation
        """

        status = Status(status=True, subsystem=_eps)
        if power is not None:
            status = _eps.set_power_on(power)

        return status


class Mutation(graphene.ObjectType):
    """
    Creates mutation endpoints exposed by graphene.
    """

    power_on = PowerOn.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
