#!/usr/bin/env python3

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene
from .models import *
from obcapi import rtc

_rtc = rtc.RTC(2)

'''
type Query {
    getTime(): Time
    getDate(): Date
    getDateTime(): DateTime
}
'''
class Query(graphene.ObjectType):

    getDateTime = graphene.Field(RTCDateTime)
    def resolve_datetime(self, info):
        # should send hardware a ping and expect a pong back
        _datetime, _success, _errors = _rtc.getDateTime()

        # return results
        return Time(result=Result(success=_success, errors=_errors), datetime=_datetime)

    '''
    {
        getTime {
            time
            result {
                success
                errors
            }
        }
    }
    '''
    #getTime = graphene.Field(Time)
    #def resolve_time(self, info):
    #    # should send hardware a ping and expect a pong back
    #    _time, _success, _errors = _rtc.getTime()
    #
    #    # return results
    #    return Time(result=Result(success=_success, errors=_errors), time=_time)

    '''
    {
        getDate { 
            date
            result {
                success
                errors
            }
        }
    }
    '''
    #getDate = graphene.Field(Date)
    #def resolve_date(self, info):
    #    # should send hardware a ping and expect a pong back
    #    date, success, errors = _rtc.getDate()
    #
    #    # return results
    #    return Date(result=Result(success=_success, errors=_errors), date=_date)

    '''
    {
        getDateTime {
            datetime
            result {
                success
                errors
            }
        }
    }
    '''


schema = graphene.Schema(query=Query)