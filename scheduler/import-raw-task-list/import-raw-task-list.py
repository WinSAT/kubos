#!/usr/bin/env python3

"""
Add a raw task list as a JSON to a mode in the scheduler. If the targeted mode is active, all tasks in the task list will be immediately scheduled. 
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("import-raw-task-list")

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
    pass

    #name = "camera"
    #mode = "operational"

    # send mutation to add raw task list to mode in scheduler
    #request = '''
    #mutation {
    #    importRawTaskList(name: "a", mode: "b", json: "{\"tasks\":[{\"description\":\"start-camera\",\"delay\":\"10m\",\"app\": {\"name\":\"activate-camera\"}}]}") {
    #        success,
    #        errors
    #    }
    #}
    #'''
    #response = SERVICES.query(service="scheduler-service", query=request)

    # get results
    #response = response["importRawTaskList"]
    #success = response["success"]
    #errors = response["errors"]

    #if success:
    #    logger.info("Added task list {} to mode {}.".format(name, mode))
    #else:
    #    logger.warning("Could not add task list {} to mode {}: {}.".format(name, mode, errors))


if __name__ == "__main__":
    main()
