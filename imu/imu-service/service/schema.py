#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *
from winapi import imu

_imu = imu.IMU(bus=2)

'''
type Query {
    mag(): MagResult
    acc(): AccResult
    gyr(): GyrResult
    qua(): QuaResult
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
        success, errors, x, y, z = _imu.mag()
        return MagnetometerResult(success=success, errors=errors, magData=Magnetometer(x=x, y=y, z=z))


    '''
    query {
        acc
    }
    '''
    acc = graphene.Field(AccelerometerResult)
    def resolve_acc(self, info):
        success, errors, x, y, z = _imu.acc()
        return AccelerometerResult(success=success, errors=errors, accData=Accelerometer(x=x, y=y, z=z))

    '''
    query {
        gyr
    }
    '''
    gyr = graphene.Field(GyroscopeResult)
    def resolve_gyr(self, info):
        success, errors, x, y, z = _imu.gyr()
        return GyroscopeResult(success=success, errors=errors, gyrData=Gyroscope(x=x, y=y, z=z))

    '''
    query {
        qua
    }
    '''
    qua = graphene.Field(QuaternionResult)
    def resolve_qua(self, info):
        success, errors, q1, q2, q3, q4 = _imu.qua()
        return QuaternionResult(success=success, errors=errors, quaData=Quaternion(q1=q1,q2=q2,q3=q3,q4=q4))

schema = graphene.Schema(query=Query)
