#!/usr/bin/env python3

"""
Main file for radio application that defines communcation between
satellite and ground station
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def on_boot(logger):
    '''
    code to setup/initialize communications subsystem
    '''
    pass

def on_command(logger):
    '''
    code for sending/receiving commands/data from ground station by using built-in
    communcations service
    '''
    while True:
    # pinging adcs subsystem
    request = '{ ping }'
    response = SERVICES.query(service="radio-service", query=request)
    response = response["ping"]

    if response == "pong":
        logger.debug("Successful connection to radio")
    else:
        logger.warn("Unsuccessful connection to radio. Sent: {} | Received: {}. Trying again...".format(request, response))

def main():

    logger = app_api.logging_setup("radio-app")

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

    if args.run[0] == 'OnBoot':
        on_boot(logger)
    elif args.run[0] == 'OnCommand':
        on_command(logger)
    else:
        logger.error("Unknown run level specified")
        sys.exit(1)

if __name__ == "__main__":
    main()
