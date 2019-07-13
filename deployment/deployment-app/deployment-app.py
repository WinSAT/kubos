#!/usr/bin/env python3

"""
Deployment application that handles the deployment sequence. The Deployment
sequence is made of 4 steps:
    1) Keeping track of hold time required by launch provider
    2) Deployment of deployables (solar panels, antenna, etc.)
    3) Powering on radio and configuring appropriately for initial contact
    4) Detumbling and stabilization of spacecraft
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import app_api
import sys

SERVICES = app_api.Services()

def on_boot(logger):

    logger.info("OnBoot logic")

''''''''''''''''''''''' STEP 1 - HOLD TIME TRACKING ''''''''''''''''''''
Hold time tracking done by U-boot environment variables. Two variables are used:
    1) deployed: boolean True if satellite deployment already complete
    2) deploy_start: string in seconds since unix epoch

(The U-Boot environment is a block of memory that is kept on persistent storage
and copied to RAM when U-Boot starts. It is used to store environment variables
which can be used to configure the system.)
'''
    # set system time from real-time clock from OBC

    # if (deployed)
    #   complete recurring boot tasks
    # else
    #   check "deploy_start" has a value
    #   yes:
    #       resume from "deploy_start" time
    #   no:
    #       set "deploy_start"
    #       begin timer
    #   once timer ends...
    #   check deployment tasks
    #   set "deployed" to True if successful

def on_command(logger):

def main():

    logger = app_api.logging_setup("deployment-app")

    parser = argparse.ArgumentParser()

    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('cmd_args', nargs='*')

    args = parser.parse_args()

    if args.config is not None:
        global SERVICES
        SERVICES = app_api.Services(args.config[0])
    else:
        SERVICES = app_api.Services()

    if args.run[0] == 'OnBoot':
        on_boot(logger)
    elif args.run[0] == 'OnCommand':
        on_command(logger)
    else:
        logger.error("Unknown run level specified")
        sys.exit(1)

if __name__ == "__main__":
    main()
