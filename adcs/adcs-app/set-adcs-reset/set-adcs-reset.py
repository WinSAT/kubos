#!/usr/bin/env python3

"""
Mission application that sets the power state of the ADCS module RESET.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("set-adcs-reset")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    args = parser.parse_args()

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
    
    request = '''
    mutation {
        controlPower(controlPowerInput: {power: RESET}) {
            success
            errors
        }
    }
    '''
    response = SERVICES.query(service="adcs-service", query=request)

    # get results
    result = response["controlPower"]
    success = result["success"]
    errors = result["errors"]

    # check results
    if success:
        logger.info("Set ADCS power RESET.")
    else:
        logger.warn("Unable to set ADCS power RESET: {}.".format(errors))

if __name__ == "__main__":
    main()
