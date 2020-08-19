#!/usr/bin/env python3

"""
Mission application that sets the mode of the ADCS module to POINTING.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("set-adcs-pointing")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('a', type=float)
    parser.add_argument('b', type=float)
    parser.add_argument('c', type=float)
    parser.add_argument('d', type=float)

    args = parser.parse_args()

    SERVICES = app_api.Services("/etc/kubos-config.toml")

    # run app onboot or oncommand logic
    if args.run is not None:
        if args.run[0] == 'OnBoot':
            on_boot(logger, SERVICES)
        elif args.run[0] == 'OnCommand':
            on_command(logger, SERVICES, args.a, args.b, args.c, args.d)
    else:
        on_command(logger, SERVICES, args.a, args.b, args.c, args.d)

# logic run for application on OBC boot
def on_boot(logger, SERVICES):
    pass

# logic run when commanded by OBC
def on_command(logger, SERVICES, a, b, c, d):
    
    # send mutation to turn off EPS port
    request = '''
    mutation {
        setModePointing(pointingInput: {a: %f, b: %f, c: %f, d: %f}) {
            errors
            success
        }
    }
    ''' %(a, b, c, d)
    response = SERVICES.query(service="adcs-service", query=request)

    # get results
    result = response["setModePointing"]
    success = result["success"]
    errors = result["errors"]

    # check results
    if success:
        logger.info("Set ADCS to POINTING.")
    else:
        logger.warn("Unable to set ADCS POINTING: {}".format(errors))

if __name__ == "__main__":
    main()
