#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *
from obcapi import DS3231

_rtc = DS3231.DS3231(2)

class Query(graphene.ObjectType):

    '''
    query {
        ping
    }
    '''
    ping = graphene.String()
    def resolve_ping(self, info):
        return _rtc.ping()

    '''
    type Query {
        dateTime {
            datetime
                result {
                    success
                    errors
            }
        }
    }
    '''
    dateTime = graphene.Field(RTCDateTime)
    def resolve_dateTime(self, info):
        # should send hardware a ping and expect a pong back
        _datetime = _rtc.datetime()
        # set success to true and error to nothing as default for now
        _success = True 
        _errors = []

        # return results
        return RTCDateTime(result=Result(success=_success, errors=_errors), datetime=_datetime)

schema = graphene.Schema(query=Query)