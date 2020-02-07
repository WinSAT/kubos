#!/usr/bin/env python3

"""
Mission application that reads magnetometer data from IMU
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time

def main():

    logger = app_api.logging_setup("imu-read-mag")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('cmd_args', nargs='*')
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
    logger.info("Querying magnetometer data from FXOS8700...")

    try:
        request = '''
        { 
            mag {
                success
                errors
                magData {
                    x
                    y
                    z
                }
            } 
        }
        '''
        response = SERVICES.query(service="imu-service", query=request)
        result = response["mag"]
        success = result["success"]
        errors = result["errors"]
        magData = result["magData"]
        x = magData["x"]
        y = magData["y"]
        z = magData["z"]

        if success:
            logger.info('Magnetometer (uTesla): ({}, {}, {})'.format(x, y, z))
        else:
            logger.warn("Unable to retrieve magnetometer data: {}".format(errors))

    except Exception as e:
        logger.warn("Unsuccessful getting data from magnetometer: {}-{}".format(type(e).__name__,str(e)))

if __name__ == "__main__":
    main()
