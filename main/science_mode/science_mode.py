#!/usr/bin/env python3

"""
Main file for science mode operation which is started when the CDH is notified
that an image capture needs to be completed.

The mode starts when an image capture is requested and ends when the image
capture is completed.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():
    logger = app_api.logging_setup("critical-mode")

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
'''
1. Send command to payload to capture image at certain time (still need to figure out how timing will work)
2. Wait for image capture to be completed.
3. Once notified image capture completed, return to nominal mode of operation
'''

if __name__ == "__main__":
    main()
