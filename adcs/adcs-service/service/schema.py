#!/usr/bin/env python3

"""
Graphene schema setup to enable queries.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *
from obcapi import adcs 

# Local subsystem instance for tracking state
# May not be neccesary when tied into actual hardware
_adcs = adcs.ADCS()

############## QUERIES ################

'''
type Query {
    ping(): String
    power(): PowerState
    mode(): ModeState
    orientation(): Orientation
    spin(): Spin
    telemetry(): Telemetry
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
        power { state }
    }
    '''
    power = graphene.Field(PowerState)
    def resolve_power(self, info):
        state = _adcs.power()
        return PowerState(state=state)

    '''
    query {
        mode { state }
    }
    '''
    mode = graphene.Field(ModeState)
    def resolve_mode(self, info):
        state = _adcs.mode()
        return ModeState(state=state)

    '''
    query {
        orientation { a b c d }
    }
    '''
    orientation = graphene.Field(Orientation)
    def resolve_orientation(self, info):
        orient = _adcs.orientation()
        return Orientation(a=orient[0],b=orient[1],c=orient[2],d=orient[3])

    '''
    query {
        spin { x y z }
    }
    '''
    spin = graphene.Field(Spin)
    def resolve_spin(self, info):
        spin = _adcs.spin()
        return Spin(x=spin[0],y=spin[1],z=spin[2])
        
    '''
    query {
        telemetry {
            orientation { a b c d }
            spin { x y z }
            mode { state }
            power { state }
        }
    }
    '''
    telemetry = graphene.Field(Telemetry)
    def resolve_telemetry(self, info):
        mode = _adcs.mode()
        power = _adcs.power()

        o = _adcs.orientation()
        orientation = Orientation(a=o[0],b=o[1],c=o[2],d=o[3])
        
        spin = _adcs.spin()
        spin = Spin(x=spin[0],y=spin[1],z=spin[2])

        return Telemetry(   ModeState(state=mode),
                            PowerState(state=power),
                            orientation,
                            spin
        )

############## MUTATIONS ################

'''
mutation {
    controlPower(controlPowerInput: {power: OFF}) {
        success
        errors
        }
    }
'''
class ControlPower(graphene.Mutation):
    class Arguments:
        controlPowerInput = ControlPowerInput()

    Output = Result
    def mutate(self, info, controlPowerInput):
        success, errors = _adcs.controlPower(controlPowerInput)
        return Result(success=success, errors=errors)

'''
mutation {
    setModePointing(pointingInput: {a: 1.0, b: 1.0, c: 1.0, d: 1.0}) {
        errors
        success
    }
}
'''
class SetModePointing(graphene.Mutation):
    class Arguments:
        pointingInput = PointingInput()

    Output = Result
    def mutate(self, info, pointingInput):
        success, errors = _adcs.setModePointing(pointingInput)
        return Result(success=success, errors=errors)

'''
mutation {
    setModeDetumble() {
        errors
        success
    }
}
'''
class SetModeDetumble(graphene.Mutation):
    Output = Result
    def mutate(self, info):
        success, errors = _adcs.setModeDetumble()
        return Result(success=success, errors=errors)

'''
mutation {
    setModeIdle() {
        errors
        success
    }
}
'''
class SetModeIdle(graphene.Mutation):
    Output = Result
    def mutate(self, info):
        success, errors = _adcs.setModeIdle()
        return Result(success=success, errors=errors)

'''
type Mutation {
    controlPower(input: ControlPowerInput!): ControlPower
    setModePointing (input: pointingInput!): Result
    setModeDetumble (): Result
    setModeIdle (): Result
}
'''
class Mutation(graphene.ObjectType):
    controlPower = ControlPower.Field()
    setModeDetumble = SetModeDetumble.Field()
    setModePointing = SetModePointing.Field()
    setModeIdle = SetModeIdle.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
