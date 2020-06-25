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
        orientation { x y z yaw pitch roll }
    }
    '''
    orientation = graphene.Field(Orientation)
    def resolve_orientation(self, info):
        orient = _adcs.orientation()
        return Orientation(x=orient[0],y=orient[1],z=orient[2],yaw=orient[3],pitch=orient[4],roll=orient[5])

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
            orientation { x y z yaw pitch roll }
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
        orientation = Orientation(x=o[0],y=o[1],z=o[2],yaw=o[3],pitch=o[4],roll=o[5])
        
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
    setMode(setModeInput: {mode: DETUMBLE}) {
        errors
        success
    }
}
'''
class SetMode(graphene.Mutation):
    class Arguments:
        setModeInput = SetModeInput()

    Output = Result
    def mutate(self, info, setModeInput):
        success, errors = _adcs.setMode(setModeInput)
        return Result(success=success, errors=errors)

'''
type Mutation {
    controlPower(
        input: ControlPowerInput!
    ): ControlPower
    setMode(
        input: SetModeInput!
    ): SetMode
}
'''
class Mutation(graphene.ObjectType):
    controlPower = ControlPower.Field()
    setMode = SetMode.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
