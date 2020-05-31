#!/usr/bin/env python3

"""
Register mission applications
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

# SAFE MODE APPS
SAFE_MODE = {
    "HEALTH-MEM-QUERY": "/home/kubos/health/health-mem-query",
    "CLEAR-DATABASE": "/home/kubos/telemetry/clear-database",
    "HEALTH-MEM-CHECK": "/home/kubos/health/health-mem-check"
}

# SCIENCE MODE APPS
SCIENCE_MODE = {

}

# CRTICAL MODE
CRTICAL_MODE = {

}

def main():

    logger = app_api.logging_setup("register")

    # else use default global config file
    SERVICES = app_api.Services("/etc/kubos-config.toml")

    # SAFE MODE APPS
    for item, path in SAFE_MODE.items():

        request = ''' mutation { register(path: "%s") { success, errors, entry { active, app { name, version } } } } ''' % (path)
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
            logger.warning("Could not register app at path {}: {}".format(path, errors))

if __name__ == "__main__":
    main()
