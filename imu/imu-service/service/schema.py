#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *

# Local subsystem instance for tracking state
# May not be neccesary when tied into actual hardware
_accelerometer = Accelerometer()

'''
type Query {
    x(): Float
}
'''
class Query(graphene.ObjectType):

    '''
    query {
        x
    }
    '''
    x = graphene.Float()
    def resolve_x(self, info):
        return _accelerometer.x()

schema = graphene.Schema(query=Query)
