#!/usr/bin/env python3

"""
Mission application that pings the payload subsystem to check for successful connection.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("payload-ping")

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
    logger.info("Starting nominal operation for payload subsystem...")

    # pinging payload subsystem
    request = ''' {
        ping 
    }
    '''
    response = SERVICES.query(service="payload-service", query=request)

    # get results
    result = response["ping"]

    # check results
    if "pong"==result:
        logger.info("Successful ping connection to payload.")
    else:
        logger.warn("Unsuccessful ping connection to payload: {}.".format(errors))

if __name__ == "__main__":
    main()
