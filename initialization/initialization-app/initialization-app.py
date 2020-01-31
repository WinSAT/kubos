#!/usr/bin/env python3

"""
Initialization application that handles the initialization sequence. This sequence
is started on CDH startup and ends when finished initialization steps shown below:

    1) Initialize EPS subsystem
    2) Initialize RF and start initial communication with ground station
    3) Wait for message confirmation from ground station
    4) ADCS detumble
    5) Finish any other desired actions

"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import app_api
import sys

def main():
    logger = app_api.logging_setup("initialization-mode")

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
    '''
    Implement above functionality and steps
    '''
    pass

# logic run when commanded by OBC
def on_command(logger, SERVICES):
    '''
    Implement above functionality and steps
    '''
    pass

if __name__ == "__main__":
    main()
