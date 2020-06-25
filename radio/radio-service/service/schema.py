#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import threading
import graphene
from .models import *
from obcapi import radio

# initialize radio - sync word from astrodev datasheet
_radio = radio.RADIO(sync_word=b"\x48\x65")

# start radio read thread for constantly receiving and handling any incoming packets
read_thread = threading.Thread(target=_radio.main())
read_thread.start()

'''
type Query {
    ping(): String
}
'''
class Query(graphene.ObjectType):

    '''
    {
        ping
    }
    '''
    ping = graphene.String()
    def resolve_ping(self, info):
        return _radio.ping()

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
        buffer = _radio.receive()
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