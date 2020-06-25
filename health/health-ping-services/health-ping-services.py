#!/usr/bin/env python3

"""
Health mission application that pings every hardware service at intervals to notify of system issues/failures.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time

def main():

    logger = app_api.logging_setup("health-ping-services")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    args = parser.parse_args()

    if args.config is not None:
        # use user config file if specified in command line
        SERVICES = app_api.Services(args.config[0])
    else:
        # else use default global config file
        SERVICES = app_api.Services()

    # run app onboot or oncommand logic
    if args.run is not None:
        if args.run[0] == 'OnBoot':
            on_boot(logger, SERVICES)
        elif args.run[0] == 'OnCommand':
            on_command(logger, SERVICES)
    else:
        on_command(logger, SERVICES)

# logic run for application on OBC boot
def on_boot(logger, SERVICES):
    pass

# logic run when commanded by OBC
def on_command(logger, SERVICES):
    
    # ping ADCS service
    try:
        request = ''' query { ping } '''
        response = SERVICES.query(service="adcs-service", query=request)
        if "pong" == response["ping"]:
            logger.info("Success pinging ADCS service")
        else:
            logger.warn("Unable to ping ADCS service")
    except Exception as e:
        logger.error("Exception trying to ping ADCS service: {}{}".format(type(e).__name__,str(e)))

    # ping EPS service
    try:
        request = ''' query { ping } '''
        response = SERVICES.query(service="eps-service", query=request)
        if "pong" == response["ping"]:
            logger.info("Success pinginG EPS service")
        else:
            logger.warn("Unable to ping EPS service")
    except Exception as e:
        logger.error("Exception trying to ping EPS service: {}{}".format(type(e).__name__,str(e)))

    # ping Payload service
    try:
        request = ''' query { ping } '''
        response = SERVICES.query(service="payload-service", query=request)
        if "pong" == response["ping"]:
            logger.info("Success pinging payload service")
        else:
            logger.warn("Unable to ping payload service")
    except Exception as e:
        logger.error("Exception trying to ping payload service: {}{}".format(type(e).__name__,str(e)))

    # ping Radio service
    try:
        request = ''' query { ping } '''
        response = SERVICES.query(service="radio-service", query=request)
        if "pong" == response["ping"]:
            logger.info("Success pinging radio service")
        else:
            logger.warn("Unable to ping radio service")
    except Exception as e:
        logger.error("Exception trying to ping radio service: {}{}".format(type(e).__name__,str(e)))

if __name__ == "__main__":
    main()
