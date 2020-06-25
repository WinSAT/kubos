#!/usr/bin/env python3

"""
Main file for adcs application
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def on_boot(logger):
    '''
    code to setup/initialize adcs subsystem
    '''
    pass

def on_command(logger):
    '''
    code for sending/receiving commands/telemetry from adcs subsystem
    '''
    while True:
        # pinging adcs subsystem
        request = '{ ping }'
        response = SERVICES.query(service="adcs-service", query=request)
        response = response["ping"]

        if response == "pong":
            logger.debug("Successful connection to adcs subsystem")
        else:
            logger.warn("Unsuccessful connection to adcs subsystem. Sent: {} | Received: {}. Trying again...".format(request, response))

def main():

    logger = app_api.logging_setup("adcs-app")

    parser = argparse.ArgumentParser()

    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('cmd_args', nargs='*')

    args = parser.parse_args()

    if args.config is not None:
        global SERVICES
        SERVICES = app_api.Services(args.config[0])
    else:
        SERVICES = app_api.Services()

    if args.run is not None:
        if args.run[0] == 'OnBoot':
            on_boot(logger)
        elif args.run[0] == 'OnCommand':
            on_command(logger)
    else:
        on_command(logger)

if __name__ == "__main__":
    main()
