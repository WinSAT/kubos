#!/usr/bin/env python3

"""
Mission app that retrieves information about currently running applications, and info about last time application was run.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("app-status")

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

    # name = Returns app entries which have the specified application name
    # version = Returns app entries which have the specified version number
    # running = Returns app entries which are/aren’t actively running

    '''
    {
        appStatus(name: String, version: String, running: Boolean) {
            name:       Application name
            version:    Version of the application which was/is running
            startTime:  The time at which the application was started, in ISO 8601 format
            endTime:    If the application has finished executing, the time at which execution ended
            running:    Indicates if the application is currently executing
            pid:        If the application is still running, the process ID assigned to the running application
            lastRc:     If the application has finished executing, the return code emitted by the application. Mutually exclusive with lastSignal
            lastSignal: If the application has finished executing and was stopped by a signal, the signal which was sent to the application. Mutually exlusive with lastRc
            args:       Any command-line arguments which were passed to the application executable. If no arguments were given, this field will not be returned
            config:     The non-default service configuration file which will be referenced by the application. If the default configuration is being used, this field will not be returned
        }
    }
    '''

    request = '''
    query     {
        appStatus(name: "%s") {
            name
            version
            startTime
            endTime
            running
            pid
            lastRc
            lastSignal
            args
            config
        }
    }
    ''' % (name)
    response = SERVICES.query(service="app-service", query=request)

    # get results
    for item in response["appStatus"]:
        name = item["name"]
        version = item["version"]
        startTime = item["startTime"]
        endTime = item["endTime"]
        running = item["running"]
        pid = item["pid"]
        lastRc = item["lastRc"]
        lastSignal = item["lastSignal"]
        args = item["args"]
        config = item["config"]

        if running:
            logger.info("App {} version {} is running with pid: {}".format(name, version, pid))
        else:
            if lastRc:
                logger.info("App {} version {} ran from {} - {} and finished exit code: {}".format(name, version, startTime, endTime, lastRc))
            else:
                logger.info("App {} version {} ran from {} - {} and finished successfully.".format(name, version, startTime, endTime))


if __name__ == "__main__":
    main()
