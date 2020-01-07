#!/usr/bin/env python3

"""
Main file for payload application that defines communcation between CDH and
primary payload (camera) mainly through hardware payload-service
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("payload-app")

    parser = argparse.ArgumentParser()

    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('cmd_args', nargs='*')

    args = parser.parse_args()

    if args.config is not None:
        SERVICES = app_api.Services(args.config[0])
    else:
        SERVICES = app_api.Services()

    if args.run is not None:
        if args.run[0] == 'OnBoot':
            on_boot(logger, SERVICES)
        elif args.run[0] == 'OnCommand':
            on_command(logger, SERVICES)
    else:
        on_command(logger, SERVICES)


def on_boot(logger, SERVICES):

    print("OnBoot logic")

'''
code to setup/initialize payload subsystem (camera)
'''

def on_command(logger, SERVICES):

    logger.info("OnCommand logic")
    logger.info("Pinging pi to see if uart setup...")

    request = '{ ping }'

#query {
#    testResults {
#     telemetryNominal { field1nominal field2nominal }
#     telemetryDebug { field1debug field2debug }
#     success
#     results1
#     results2
#    }
#}

    response = SERVICES.query(service="payload-service", query=request)
    data = response["ping"]
    logger.info("Got back response from payload: %s" % data)

'''
code for sending/receiving commands/images from payload subsystem (camera)
using defined hardware payload-service
'''


if __name__ == "__main__":
    main()
