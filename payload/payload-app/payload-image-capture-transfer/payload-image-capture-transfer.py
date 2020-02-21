#!/usr/bin/env python3

"""
Mission application that requests an image capture and then transfers it from payload subsystem.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time

def main():

    logger = app_api.logging_setup("payload-image-capture-transfer")

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
        SERVICES = app_api.Services("/home/kubos/kubos/local_config.toml")

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
    logger.info("Starting image capture..")

    time_1 = time.time()

    # send request for image capture
    request = '''
    mutation {
        imageCapture {
            success
            errors
        }
    }
    '''
    response = SERVICES.query(service="payload-service", query=request)

    time_2 = time.time()

    # get results
    result = response["imageCapture"]
    success = result["success"]
    errors = result["errors"]

    # check results
    if success:
        logger.info("Payload completed successful image capture.")
    else:
        logger.warn("Unsuccessful image capture request to payload: {}.".format(errors))
        sys.exit(1)

    time.sleep(1)

    logger.info("Starting image transfer..")

    time_3 = time.time()

    # send request for image transfer
    request = '''
    mutation {
        imageTransfer {
            success
            errors
        }
    }
    '''
    response = SERVICES.query(service="payload-service", query=request, timeout=100)

    time_4 = time.time()

    # get results
    result = response["imageTransfer"]
    success = result["success"]
    errors = result["errors"]

    # check results
    if success:
        logger.warn("Successful image transfer with payload.")
    else:
        logger.warn("Unable to complete image transfer with payload: {}.".format(errors))
        sys.exit(1)

    # debug
    logger.debug("Time for image capture: {}".format(time_2 - time_1))
    logger.debug("Time for image transfer: {}".format(time_4 - time_3))

if __name__ == "__main__":
    main()
