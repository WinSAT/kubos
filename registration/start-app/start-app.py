#!/usr/bin/env python3

"""
Mission app that manually starts another mission app. Only one instance of an application can be running at one time.


"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("start-app")

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
    # version = Custom config file to be passed to application
    # args = Allows additional arguments to be passed through to the underlying application

    '''
    mutation {
        startApp(name: "mission-app", config: "/home/kubos/config.toml", args: ["-m", "safemode"]) {
            success,
            errors: if app immediately fails, something will be returned here
            pid: empty if not successful
        }
    }
    '''

    request = '''
    mutation {
        startApp(name: "%s") {
            success,
            errors,
            pid
        }
    }
    ''' % (name)
    response = SERVICES.query(service="app-service", query=request)
    # get results
    response = response["startApp"]
    success = response["success"]
    errors = response["errors"]
    
    if success:
        logger.info("Started app {} with pid: {}".format(name, response["pid"]))
    else:
        logger.warning("Unable to start app {}: {}".format(name, errors))

if __name__ == "__main__":
    main()
