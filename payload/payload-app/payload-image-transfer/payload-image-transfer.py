#!/usr/bin/env python3

"""
Mission application that requests an image transfer from payload subsystem to OBC.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("payload-image-transfer")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
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

    # send request for image capture
    request = '''
    mutation {
        issueRawCommand(command: "transfer_image") {
            success
            errors
        }
    }
    '''
    response = SERVICES.query(service="payload-service", query=request)

    # get results
    result = response["issueRawCommand"]
    success = result["success"]
    errors = result["errors"]

    # check results
    if not success:
        logger.warn("Unable to initiate image transfer from payload: {}.".format(errors))
        sys.exit(1)

    logger.info("Starting image transfer with payload...")



if __name__ == "__main__":
    main()
