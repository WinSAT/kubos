#!/usr/bin/env python3

"""
List all avaialble versions of all registered applications in the applications service.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("list-registered-apps")

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

    # name = returns app entries which have the specified application name
    # version = returns app entries which have the specified version number
    # active = when True, returns only active entry of an application, i.e. the version which will be used when run

    '''
    {
        registeredApps(name: String, version: String, active: Boolean) {
            [
                active = specifies whether this version of the app will be run on startApp mutation,
                app {
                    name = name of application
                    executable = path of file which is executed when app is started
                    version = version number of this application entry
                    author = creator/owner of this application entry
                    config = configuration file passed to application when run
                }
            ]
        }
    }
    '''

    request = '''
    query {
        registeredApps {
            active
            app {
                name
                executable
                version
                author
                config
            }
        }
    }
    '''
    response = SERVICES.query(service="app-service", query=request)

    # get results
    response = response["registeredApps"]
    for item in response:
        active = item["active"]
        app = item["app"]
        name = app["name"]
        executable = app["executable"]
        version = app["version"]
        author = app["author"]
        config = app["config"]

        logger.info("\nRegistered app: {}\n executable: {}\n version: {}\n author: {}\n config: {}\n active: {}\n".format(name, executable, version, author, config, active))


if __name__ == "__main__":
    main()
