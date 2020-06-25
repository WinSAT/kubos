#!/usr/bin/env python3

"""
Mission application that sets the power state of the ADCS module (ON, OFF, RESET).
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("set-adcs-power")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('power')
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
            on_boot(logger, SERVICES, args.power)
        elif args.run[0] == 'OnCommand':
            on_command(logger, SERVICES, args.power)
    else:
        on_command(logger, SERVICES, args.power)

# logic run for application on OBC boot
def on_boot(logger, SERVICES, power):
    pass

# logic run when commanded by OBC
def on_command(logger, SERVICES, power):
    
    # send mutation to turn off EPS port
    request = '''
    mutation {
        controlPower(controlPowerInput: {power: %s}) {
            success
            errors
        }
    }
    ''' % (power)
    response = SERVICES.query(service="adcs-service", query=request)

    # get results
    result = response["controlPower"]
    success = result["success"]
    errors = result["errors"]

    # check results
    if success:
        logger.info("Set ADCS power={}.".format(power))
    else:
        logger.warn("Unable to set ADCS power={}: {}.".format(power, errors))

if __name__ == "__main__":
    main()
