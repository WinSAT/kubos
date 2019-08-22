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

def on_boot(logger):

    print("OnBoot logic")

'''
code to setup/initialize payload subsystem (camera)
'''

def on_command(logger):

    print("OnCommand logic")
    print("Sending message 'hello' to pi...", end="")

    request = '''
mutation {
     controlPower(controlPowerInput: {state: OFF}) {
        result { success errors }
        power { state }
    }
}
        '''

    response = SERVICES.query(service="payload-service", query=request)
    print(response)

'''
code for sending/receiving commands/images from payload subsystem (camera)
using defined hardware payload-service
'''

def main():

    logger = app_api.logging_setup("payload-app")

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

    if args.run is not None:
        if args.run[0] == 'OnBoot':
            on_boot(logger)
        elif args.run[0] == 'OnCommand':
            on_command(logger)
    else:
        on_command(logger)

if __name__ == "__main__":
    main()
