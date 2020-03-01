#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *
from obcapi import radio

_radio = radio.Radio()

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
        success, errors = _radio.ping()

        # return results
        return Result(success=success, errors=errors)

    '''
    {
        read {
            buffer
            success
            errors
        }
    }
    '''
    read = graphene.Field(MessageResult)
    def resolve_read(self, info):
        # should send hardware a ping and expect a pong back
        buffer = _radio.read()
        success = True
        errors = []
        # return results
        result = Result(success=success, errors=errors)
        return MessageResult(message=buffer, result=result)

'''
mutation {
    image_transfer() {
        success
        errors
    }
}
'''
class ImageTransfer(graphene.Mutation):
    Output = Result
    def mutate(self, info):
        # should send hardware command to payload to start image transfer
        success, errors = _radio.image_transfer()
        # return results
        return Result(success=success, errors=errors)

'''
type Mutation {
    imageTransfer(): Result
}
'''
class Mutation(graphene.ObjectType):
    imageTransfer = ImageTransfer.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)