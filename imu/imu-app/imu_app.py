#!/usr/bin/env python3

"""
Test python application for testing IMU hardware service.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time
#import board
#import busio
import adafruit_fxos8700

from i2c_device import ADA_I2C
from i2c_device import Kubos_I2C

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
            time.sleep(1)
            # pinging payload subsystem
            #request = '{ x }'
            #response = SERVICES.query(service="accelerometer-service", query=request)
            #logger.debug("Got response from accelerometer service: {}".format(str(response)))
            #response = response["x"]
            #logger.debug("Got x data from accelerometer: {}".format(str(response)))

            #i2c = ADA_I2C(board.SCL, board.SDA)
            i2c = Kubos_I2C(bus=2)
            print('Using I2C Bus 2')
            sensor = adafruit_fxos8700.FXOS8700(i2c)
            print('Setup i2c done.')

            while True:
                accel_x, accel_y, accel_z = sensor.accelerometer
                mag_x, mag_y, mag_z = sensor.magnetometer
                print('Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(accel_x, accel_y, accel_z))
                print('Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(mag_x, mag_y, mag_z))
                time.sleep(1.0)

        except Exception as e:
            logger.warn("Unsuccessful getting data from accelerometer: {}. Trying again...".format(str(e)))

'''
code for continuous nominal operation for payload
'''

if __name__ == "__main__":
    main()
