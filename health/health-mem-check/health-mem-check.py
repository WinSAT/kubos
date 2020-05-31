#!/usr/bin/env python3

"""
Checks current memory usage. If memory usage more than certain amount, enter critical mode
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time

def main():

    logger = app_api.logging_setup("health-mem-check")

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
    # retrieve memory telemetry from database
    try:
        '''
        query {
            telemetry(timestampGe: Float, timestampLe: Float, subsystem: String, parameter: String, parameters: [String], limit: Integer): [{
                timestamp
                subsystem
                parameter
                value
            }]
        }

        timestampGe = return entries with timestamps on or after given value
        timestampLe = return entries with timestamps on or before given value
        subsystem = return entries that match subsystem name
        parameter = return entries which match given parameter name (mutually exclusive with parameters)
        parameters = returns entries which match given parameter names (mutually exclusive with parameter)
        limit = return only first n entries found
        '''

        request = '''
        {
            telemetry(parameter: "free_memory_percentage") {
                timestamp
                subsystem
                parameter
                value
            }
        }
        '''
        response = SERVICES.query(service="telemetry-service", query=request)
        # get results
        result = response["telemetry"]
        for item in result:
            timestamp = item["timestamp"]
            subsystem = item["subsystem"]
            parameter = item["parameter"]
            value = item["value"]

            #logger.debug("Got telemetry:{} | timestamp:{} | subsystem:{} | value:{}".format(parameter, timestamp, subsystem, value))

            threshold = 10.0
            if (float(value) < threshold):
                logger.error("Available memory: {} at {} below threshold: {}. Enter critical mode.".format(value, timestamp, threshold))
            
                # send mutation to activate critical mode
                mode = "critical"
                request = '''
                mutation {
                    activateMode(name: "%s") {
                        success
                        errors
                    }
                }''' % (mode)
                response = SERVICES.query(service="scheduler-service", query=request)

                # get results
                response = response["activateMode"]
                success = response["success"]
                errors = response["errors"]

                if success:
                    logger.info("Activtated mode named: {}.".format(mode))
                else:
                    logger.warning("Could not activate {} mode: {}.".format(mode, errors))
                
                break

    except Exception as e:
        logger.error("Unable to retrieve memory telemetry from database: {}{}".format(type(e).__name__,str(e)))

if __name__ == "__main__":
    main()
