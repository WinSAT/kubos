#!/usr/bin/env python3

"""
Mission application that checks current active mode (safe, idle, critical).
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("check-active-mode")

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
    logger.debug("Requesting current active mode..")

    # send query to check current active mode
    request = '''
    query {
        activeMode {
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
    response = response["activeMode"]
    name = response["name"]
    path = response["path"]
    lastRevised = response["lastRevised"]
    active = response["active"]
    schedule = response["schedule"]

    logger.info("Currently in {} mode.".format(name))

if __name__ == "__main__":
    main()
