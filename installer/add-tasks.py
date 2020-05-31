#!/usr/bin/env python3

"""
Add tasks (mission apps) to each of the modes
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("add-tasks")

    SERVICES = app_api.Services("/etc/kubos-config.toml")

    # add safe mode tasks/mission apps to safe mode
    path = "/home/kubos/modes/safe-mode.json"
    name = "safe-mode"
    mode = "safe"

    request = ''' mutation { importTaskList(path: "%s", name: "%s", mode: "%s") { success errors } } ''' % (path, name, mode)
    response = SERVICES.query(service="scheduler-service", query=request)

    # get results
    response = response["importTaskList"]
    success = response["success"]
    errors = response["errors"]

    if success:
        logger.info("Added task list {} at {} to mode {}.".format(name, path, mode))
    else:
        logger.warning("Could not add task list {} at {} to mode {}: {}.".format(name, path, mode, errors))


if __name__ == "__main__":
    main()
