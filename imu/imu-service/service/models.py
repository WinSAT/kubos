#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
import serial
import time
import app_api
import struct
from winserial import i2c
import logging
import smbus

class Result(graphene.ObjectType):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

class Accelerometer(graphene.ObjectType):
    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()

class Magnetometer(graphene.ObjectType):
    x = graphene.Float()
    y = graphene.Float()
    z = graphene.Float()

class AccelerometerResult(graphene.ObjectType):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()
    accData = graphene.Field(Accelerometer)

class MagnetometerResult(graphene.ObjectType):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()
    magData = graphene.Field(Magnetometer)