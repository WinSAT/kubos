#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene

class Result(graphene.ObjectType):
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

#class Time(graphene.ObjectType):
#    time = graphene.types.datetime.Time()
#    result = Result()

class RTCDateTime(graphene.ObjectType):
    datetime = graphene.types.datetime.DateTime()
    result = Result()

#class Date(graphene.ObjectType):
#    datetime = graphene.types.datetime.Date()
#    result = Result()
