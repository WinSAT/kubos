#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *
from obcapi import payload

_payload = payload.Payload()

'''
type Query {
    ping(): String
}
'''
class Query(graphene.ObjectType):

    '''
    {
        ping {
            success
            errors
        }
    }
    '''
    ping = graphene.Field(Result)
    def resolve_ping(self, info):
        # should send hardware a ping and expect a pong back
        success, errors = _payload.ping()
        # return results
        return Result(success=success, errors=errors)

'''
mutation {
    image_capture() {
        success
        errors
    }
}
'''
class ImageTransfer(graphene.Mutation):
    Output = Result
    def mutate(self, info):
        # should send hardware command to payload to start image transfer
        success, errors = _payload.image_transfer()
        # return results
        return Result(success=success, errors=errors)

'''
mutation {
    image_transfer() {
        success
        errors
    }
}
'''
class ImageCapture(graphene.Mutation):
    Output = Result
    def mutate(self, info):
        # should send hardware command to payload to start image capture
        success, errors = _payload.image_capture()
        # return results
        return Result(success=success, errors=errors)

'''
type Mutation {
    imageCapture(): Result
    imageTransfer(): Result
}
'''
class Mutation(graphene.ObjectType):
    imageCapture = ImageCapture.Field()
    imageTransfer = ImageTransfer.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)