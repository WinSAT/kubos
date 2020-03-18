#!/usr/bin/env python3

"""
Deregister a mission application or uninstall a single verison or all version of an application.

If you would like to uninstall a current active version, use the setVersion mutation first to rollback
to a previous version of the app before uninstalling. Or else the system will not know which version to use.

If the app to be uninstalled is currently running, it will be stopped by SIGTERM then SIGKILL. Using the 
killApp mutation instead prior to uninstalling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("deregister-app")

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

    # send mutation to deregister app (name is required, version is optional)
    request = '''
    mutation {
        uninstall(name: "%s", version: "1.0") {
            success,
            errors
        }
    }
    ''' % (name)
    response = SERVICES.query(service="app-service", query=request)

    # get results
    response = response["uninstall"]
    success = response["success"]
    errors = response["errors"]

    if success:
        logger.info("Deregistered app: {}".format(name))
    else:
        logger.warning("Unable to deregister app {}: {}".format(name, errors))


if __name__ == "__main__":
    main()
