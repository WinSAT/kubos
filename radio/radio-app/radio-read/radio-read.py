#!/usr/bin/env python3

"""
Mission application that sends reads incoming messages from the ground station over radio.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time

def main():

    logger = app_api.logging_setup("radio-read")

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
        SERVICES = app_api.Services("/etc/kubos-config.toml")

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
    logger.info("Reading messages from ground station...")

    while 1:
        request = '''
        query {
            read {
                result {
                    success
                    errors
                }
                message
            }
        }
        '''
        response = SERVICES.query(service="radio-service", query=request)

        # get results
        read = response["read"]
        result = read["result"]
        success = result["success"]
        errors = result["errors"]
        message = read["message"]

        # check results
        if success:
            if message:
                logger.info("SUCCESS: Got message from ground station: {}".format(message))
            else:
                logger.info("Did not get anything from ground station. Trying again...")
        else:
            logger.warn("ERROR: Trying to read from ground station: {}.".format(errors))

        time.sleep(1)

if __name__ == "__main__":
    main()
