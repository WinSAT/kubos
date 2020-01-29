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
from i2c import I2C

'''
    i2c_device = I2C(bus = 1)
    slave_address = 0x68
    data = i2c_device.read(device = slave_address, count = 1)
    print("Got data from rtc: {}".format(str(data)))

'''

def main():

    logger = app_api.logging_setup("accelerometer-app")

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
    logger.debug("Setting up payload subsystem...")
'''
code to setup/initialize payload subsystem
'''

# logic run when commanded by OBC
def on_command(logger, SERVICES):
    logger.info("Starting nominal operation for payload subsystem...")

    while True:
        try:
            # pinging payload subsystem
            request = '{ x }'
            response = SERVICES.query(service="accelerometer-service", query=request)
            logger.debug("Got response from accelerometer service: {}".format(str(response)))
            response = response["x"]
            logger.debug("Got x data from accelerometer: {}".format(str(response)))

        except Exception as e:
            logger.warn("Unsuccessful getting data from accelerometer: {}. Trying again...".format(str(e)))

'''
code for continuous nominal operation for payload
'''

if __name__ == "__main__":
    main()
