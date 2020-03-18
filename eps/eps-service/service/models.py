#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
import serial

class PowerEnum(graphene.Enum):
    OFF = 0
    ON = 1

class PortEnum(graphene.Enum):
    PORT1 = 1
    PORT2 = 2
    PORT3 = 3

class PowerState(graphene.ObjectType):
    power1 = graphene.Field(PowerEnum)
    power2 = graphene.Field(PowerEnum)
    power3 = graphene.Field(PowerEnum)

class ControlPortInput(graphene.InputObjectType):
    power = graphene.Field(PowerEnum)
    port = graphene.Field(PortEnum) 

class Result(graphene.ObjectType):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()