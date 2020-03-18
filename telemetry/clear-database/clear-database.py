#!/usr/bin/env python3

"""
Mission application that cleans out telemetry database
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time

def main():

    logger = app_api.logging_setup("health-clear-database")

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
    # delete all telemetry entries before a certain time
    timestamp = time.time() - 60
    try:
        '''
        mutation {
            delete(timestampGe: Float, timestampLe: Float, subsystem: String, parameter: String): [{
                success: Boolean!,
                errors: String!,
                entriesDeleted: Integer
            }]
        }

        timestampGe = delete entries with timestamps on or after given value
        timestampLe = delete entries with timestamps on or before given value
        subsystem = delete entries that match subsystem name
        parameter = delete entries which match given parameter name (mutually exclusive with parameters)
        '''

        request = '''
        mutation {
            delete(timestampLe: %f) {
                success
                errors
                entriesDeleted
            }
        }
        ''' % (timestamp) # delete entries more than a day old
        response = SERVICES.query(service="telemetry-service", query=request)

        # get results
        result = response["delete"]
        success = result["success"]
        errors = result["errors"]
        entriesDeleted = result["entriesDeleted"]

        if success:
            logger.debug("Deleted {} entries from database before timestamp: {}".format(entriesDeleted, timestamp))
        else:
            logger.warn("Unable to delete entries beforee timestamp: {}".format(timestamp))

    except Exception as e:
        logger.error("Exception trying to clean telemetry database: {}{}".format(type(e).__name__,str(e)))

if __name__ == "__main__":
    main()
