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

class PowerState(graphene.ObjectType):
    state = graphene.Field(PowerEnum)

class Result(graphene.ObjectType):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()