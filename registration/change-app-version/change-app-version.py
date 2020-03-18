#!/usr/bin/env python3

"""
Mission app to swap between different versions of an application. 

This is useful for manually rolling back to an older version of an application prior
to uninstalling the current version.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("change-app-version")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('name')
    parser.add_argument('version')
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
            on_command(logger, SERVICES, args.name, args.version)
    else:
        on_command(logger, SERVICES, args.name, args.version)

# logic run for application on OBC boot
def on_boot(logger, SERVICES):
    pass

# logic run when commanded by OBC
def on_command(logger, SERVICES, name, version):

    # send mutation to change version of app in registry
    request = '''
    mutation {
        setVersion(name: "%s", version: "%s") {
            success,
            errors
        }
    }
    ''' % (name, version)
    response = SERVICES.query(service="app-service", query=request)

    # get results
    response = response["setVersion"]
    success = response["success"]
    errors = response["errors"]

    if success:
        logger.info("Changed app {} to version {}.".format(name, version))
    else:
        logger.warning("Unable to change app {} to version {}: {}".format(name, version, errors))



if __name__ == "__main__":
    main()
