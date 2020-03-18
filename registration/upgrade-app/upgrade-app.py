#!/usr/bin/env python3

"""
Mission app to register new version of app in registry, without removing existing registration

Uses the same register mutation to register apps but version number in manifest.toml must be unique.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("upgrade-app")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('path')
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
            on_command(logger, SERVICES, args.path)
    else:
        on_command(logger, SERVICES, args.path)

# logic run for application on OBC boot
def on_boot(logger, SERVICES):
    pass

# logic run when commanded by OBC
def on_command(logger, SERVICES, path):

    # send mutation register app (entry will be empty on a failure)
    request = '''
    mutation {
        register(path: "%s") {
            success,
            errors,
            entry {
                active,
                app {
                    name,
                    version
                }
            }
        }
    }
    ''' % (path)
    response = SERVICES.query(service="app-service", query=request)

    # get results
    response = response["register"]
    success = response["success"]
    errors = response["errors"]

    if success:
        entry = response["entry"]
        active = entry["active"]
        app = entry["app"]
        name = app["name"]
        version = app["version"]

        logger.info("Registered app name: {} path: {} version: {} active: {}.".format(name, path, version, active))
    else:
        logger.warning("Could not registered app at path {}: {}".format(path, errors))


if __name__ == "__main__":
    main()
