#!/usr/bin/env python3

"""
Graphene schema setup to enable queries.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *

from obcapi import eps

_eps = eps.EPS()

'''
type Query {
    power(): PowerState
}
'''
class Query(graphene.ObjectType):

    '''
    query {
        power { 
            power1
            power2
            power3
        }
    }
    '''
    power = graphene.Field(PowerState)
    def resolve_power(self, info):
        power1, power2, power3 = _eps.power()

        return PowerState(power1=power1, power2=power2, power3=power3)


############## MUTATIONS ################
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

    Output = Result
    def mutate(self, info, controlPortInput):
        if (_eps.controlPort(controlPortInput)):
            return Result(success=True, errors=[])
        else:
            return Result(success=False, errors=["Invalid port number: {}".format(controlPortInput.port)])

####################################################################
'''
type Mutation {
    controlPort(
        input: ControlPowerInput!
    ): Result
}
'''
class Mutation(graphene.ObjectType):
    controlPort = ControlPort.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
