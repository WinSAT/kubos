#!/usr/bin/env python3

"""
Mission application that checks current available modes (safe, idle, critical).
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("check-available-modes")

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
    logger.debug("Requesting current available modes..")

    # send query for available modes
    request = '''
    query {
        availableModes {
            name
            path
            lastRevised
            active
            schedule {
                filename
                path
                timeImported
                tasks {
                    description
                    delay
                    time
                    period
                    app {
                        name
                        args
                        config
                    }
                }
            }
        }
    }
    '''
    response = SERVICES.query(service="scheduler-service", query=request)
    # get results
    response = response["availableModes"]
    modes = []
    for mode in response:
        name = mode["name"]
        path = mode["path"]
        lastRevised = mode["lastRevised"]
        active = mode["active"]
        schedule = mode["schedule"]

        modes.append(name)
        

    logger.info("Currently available modes: {}.".format(modes))

if __name__ == "__main__":
    main()
