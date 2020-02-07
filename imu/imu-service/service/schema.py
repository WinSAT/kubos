#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *
from winapi import FXOS8700

_fxos8700 = FXOS8700.FXOS8700(bus=2)

'''
type Query {
    mag(): MagResult
    acc(): AccResult
}
'''
class Query(graphene.ObjectType):

    '''
    query {
        mag
    }
    '''
    mag = graphene.Field(MagnetometerResult)
    def resolve_mag(self, info):
        success, errors, x, y, z = _fxos8700.mag()
        return MagnetometerResult(success=success, errors=errors, magData=Magnetometer(x=x, y=y, z=z))


    '''
    query {
        acc
    }
    '''
    acc = graphene.Field(AccelerometerResult)
    def resolve_acc(self, info):
        success, errors, x, y, z = _fxos8700.acc()
        return AccelerometerResult(success=success, errors=errors, accData=Accelerometer(x=x, y=y, z=z))

schema = graphene.Schema(query=Query)
