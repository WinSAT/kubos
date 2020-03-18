#!/usr/bin/env python3

"""
Mission app that manually stops another mission app.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("stop-app")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('name')
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
            on_command(logger, SERVICES, args.name)
    else:
        on_command(logger, SERVICES, args.name)

# logic run for application on OBC boot
def on_boot(logger, SERVICES):
    pass

# logic run when commanded by OBC
def on_command(logger, SERVICES, name):

    # name = Name of app to start
    # runLevel = app could be running onBoot and onCommand at the same time so must specify
    # signal = optional specify signal value that should be sent to app (default is SIGTERM 15) which is run
    #           with kill command and allow for cleanup

    # Note: long-running apps which will be stopped using this mutation should have programmed logic to catch
    #       SIGTERM signal and do necessary cleanup before safely exitting.

    '''
    mutation {
        killApp(name: "main-mission", runLevel: "OnBoot", signal: 2) {
            success,
            errors
        }
    }
    '''

    request = '''
    mutation {
        killApp(name: "%s") {
            success,
            errors
        }
    }
    ''' % (name)
    response = SERVICES.query(service="app-service", query=request)
    # get results
    response = response["killApp"]
    success = response["success"]
    errors = response["errors"]
    
    if success:
        logger.info("Stopped app {}".format(name))
    else:
        logger.warning("Errors stopping app {}: {}".format(name, errors))

if __name__ == "__main__":
    main()
