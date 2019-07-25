#!/usr/bin/env python3

from i2c import I2C
import argparse
import app_api
import sys

# choose i2c bus
i2c_device = I2C(bus = 1)

# get services from api
SERVICES = app_api.Services()

def on_boot(logger):

    print("OnBoot logic")

def on_command(logger):

    print("OnBoot logic")

    slave_address = 0x51
    num_read = 20
    data = 

def main():

    logger = app_api.logging_setup("i2c-app")

    parser = argparse.ArgumentParser()

    parser.add_argument('--run', '-r')

    args = parser.parse_args()

    if args.run == 'OnBoot':
        on_boot(logger)
    elif args.run == 'OnCommand':
        on_command(logger)
    else:
        logger.error("Unknown run level specified")
        sys.exit(1)

if __name__ == "__main__":
    main()
