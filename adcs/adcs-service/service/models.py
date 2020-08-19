#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
import serial

# POWER
class PowerStateEnum(graphene.Enum):
    OFF = 0
    ON = 1
    RESET = 2

class PowerState(graphene.ObjectType):
    state = graphene.Field(PowerStateEnum)

# MODE
class ModeStateEnum(graphene.Enum):
    IDLE = 0
    DETUMBLE = 1
    POINTING = 2

class ModeState(graphene.ObjectType):
    state = graphene.Field(ModeStateEnum)

# ORIENTATION
class Orientation(graphene.ObjectType):
    a = graphene.Float()
    b = graphene.Float()
    c = graphene.Float()
    d = graphene.Float()

# SPIN
class Spin(graphene.ObjectType):
    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()

# Mutation Result
class Result(graphene.ObjectType):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

# Control power mutation input
class ControlPowerInput(graphene.InputObjectType):
    power = graphene.Field(PowerStateEnum)

# input orienatio
class PointingInput(graphene.InputObjectType):
    a = graphene.Float()
    b = graphene.Float()
    c = graphene.Float()
    d = graphene.Float()

class Telemetry(graphene.ObjectType):
    # telemetry items for general status of hardware
    mode = graphene.Field(ModeState)
    power = graphene.Field(PowerState)
    orientation = graphene.Field(Orientation)
    spin = graphene.Field(Spin)