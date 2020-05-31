#!/usr/bin/env python3

"""
Add entry to telemetry database
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time

def main():

    logger = app_api.logging_setup("add-entry-database")

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
    name = str(input("Enter telemetry item name: "))
    subsystem = str(input("Enter telemetry item subsystem: "))
    value = str(input("Enter telemetry item value: "))

    # add telemetry to database
    try:
        # timestamp is optional and defaults to current system time
        request = '''
        mutation {
            insert(subsystem: "%s", parameter: "%s", value: "%s") {
                success
                errors
            }
        }
        ''' % (subsystem, name, value)
        response = SERVICES.query(service="telemetry-service", query=request)

        # get results
        result = response["insert"]
        success = result["success"]
        errors = result["errors"]

        if success:
            logger.info("Logged telemetry in database.")
        else:
            logger.warn("Unable to log telemetry to database: {}".format(errors))

    except Exception as e:
        logger.error("Error logging information in telemetry database: {}{}".format(type(e).__name__,str(e)))

if __name__ == "__main__":
    main()
