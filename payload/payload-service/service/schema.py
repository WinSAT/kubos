#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *
import logging
from winapi import payload as payload_api

logger = logging.getLogger("payload-service")

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
        payload = payload_api.PayloadAPI()

        # should send hardware a ping and expect a pong back
        success, errors = payload.write("ping")
        # return results
        return Result(success=success, errors=errors)

'''
mutation {
    captureImage {
        success
        errors
    }
}
'''
class imageTransfer(graphene.Mutation):

    Output = Result
    def mutate(self, info, command):
        payload = payload_api.PayloadAPI()

        # send raw command to payload subsystem
        success, errors = payload.write("capture_image")

        # return results
        return Result(success=success, errors=errors)

'''
mutation {
    issueRawCommand(command: "command") {
        success
        errors
    }
}
'''
class IssueRawCommand(graphene.Mutation):
    class Arguments:
        command = graphene.String()

    Output = Result
    def mutate(self, info, command):
        payload = payload_api.PayloadAPI()

        # send raw command to payload subsystem
        success, errors = payload.write(command)

        # return results
        return Result(success=success, errors=errors)

'''
type Mutation {
    issueRawCommand(
        input: IssueRawCommandInput!
    ): Result
}
'''
class Mutation(graphene.ObjectType):
    issueRawCommand = IssueRawCommand.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)