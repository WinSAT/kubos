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
    ping(): pong
    power(): PowerState
    telemetry(): Telemetry
    battery(): Float
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
        battery
    }
    '''
    battery = graphene.Int()
    def resolve_battery(self, info):
        return _eps.battery()

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

    '''
    query {
        telemetry { 
            power {
                power1
                power2
                power3
            }
            battery
        }
    }
    '''
    telemetry = graphene.Field(Telemetry)
    def resolve_telemetry(self, info):
        power1, power2, power3 = _eps.power()
        battery_level = _eps.battery()
        return Telemetry(power=PowerState(power1=power1, power2=power2, power3=power3), battery=battery_level)

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
