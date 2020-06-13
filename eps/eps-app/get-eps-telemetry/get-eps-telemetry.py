#!/usr/bin/env python3

"""
Mission application that queries all telemetry from EPS module.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("get-eps-telemetry")

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
        SERVICES = app_api.Services("/etc/kubos-config.toml")

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
    
    # collect EPS telemetry
    try:
        # send mutation to turn off EPS port
        request = '''
        query {
            telemetry {
                power {
                    power1
                    power2
                    power3
                }
                battery
            }
        }
        '''
        response = SERVICES.query(service="eps-service", query=request)

        # get results
        telemetry = response["telemetry"]

        power = telemetry["power"]
        power1 = power["power1"]
        power2 = power["power2"]
        power3 = power["power3"]
        battery = telemetry["battery"]

        telemetry = [("power1", power1), ("power2", power2), ("power3", power3), ("battery", battery)]
        logger.info("Got EPS telemetry - Current power states: 1 = {} 2 = {} 3 = {} and battery level = {}. Storing in database...".format(power1, power2, power3, battery))

    except Exception as e:
        logger.error("Error collecting EPS telemetry: {}:{}".format(type(e).__name__,str(e)))
        sys.exit(1)

    # add EPS telemetry to database
    try:
        # timestamp is optional and defaults to current system time
        subsystem = "EPS"

        for item in telemetry:
            name = item[0]
            value = item[1]

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
                logger.info("Logged telemetry {}:{}={} in database.".format(subsystem, name, value))
            else:
                logger.error("Unable to log telemetry {}:{}={} in database: {}.".format(subsystem, name, value, errors))

    except Exception as e:
        logger.error("Error logging information in telemetry database: {}:{}".format(type(e).__name__,str(e)))
        sys.exit(1)

if __name__ == "__main__":
    main()
