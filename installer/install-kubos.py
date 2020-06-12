#!/usr/bin/env python3

"""
Kubos install
Add 3 mission modes, register all applications and install them in correct mode
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

modes = {
    "safe" : {
        "path": "/home/kubos/installer/modes/safe-mode.json",
        "name": "safe-mode",
        "mode": "safe",
        "apps": {
            "health-mem-query": "/home/kubos/health/health-mem-query",
            "clear-database": "/home/kubos/telemetry/clear-database",
            "health-mem-check": "/home/kubos/health/health-mem-check",
            "set-system-time": "/home/kubos/rtc/rtc-app/set-system-time"
        }
    },
    "science" : {
        "path": "/home/kubos/installer/modes/science-mode.json",
        "name": "science-mode",
        "mode": "science",
        "apps": {
            "set-system-time": "/home/kubos/rtc/rtc-app/set-system-time"
        }
    },
    "ini" : {
        "path": "/home/kubos/installer/modes/ini-mode.json",
        "name": "ini-mode",
        "mode": "ini",
        "apps": {
            "set-system-time": "/home/kubos/rtc/rtc-app/set-system-time"
        }
    }
}

def main():

    logger = app_api.logging_setup("install-kubos")

    # else use default global config file
    SERVICES = app_api.Services("/etc/kubos-config.toml")

    print("\n")
    ############################ REMOVE MISSION MODES ######################################
    for mode, settings in modes.items():
        
        name = mode
        # send mutation to remove mode from scheduler
        request = '''
        mutation {
            removeMode(name: "%s") {
                success
                errors
            }
        }''' % (name)
        response = SERVICES.query(service="scheduler-service", query=request)

        # get results
        response = response["removeMode"]
        success = response["success"]
        errors = response["errors"]

        if success:
            logger.info("Removed mode named: {}.".format(name))
        else:
            logger.warning("Could not remove {} mode: {}.".format(name, errors))

    print("\n")
    ############################ CREATE 3 MISSION MODES ######################################
    for mode, settings in modes.items():
        
        #try:
        name = mode
        # send mutation to create mode in scheduler
        request = '''
        mutation {
            createMode(name: "%s") {
                success
                errors
            }
        }''' % (name)
        response = SERVICES.query(service="scheduler-service", query=request)

        # get results
        response = response["createMode"]
        success = response["success"]
        errors = response["errors"]

        if success:
            logger.info("Created empty mode named: {}.".format(name))
        else:
            # check if error is due to mode already existing
            if ("exists" in errors):
                logger.info("Already a mode named: {}.".format(name))
            else:
                logger.warning("Could not create {} mode: {}.".format(name, errors))

    print("\n")
    ################## DEREGISTER ALL APPLICATIONS WITH APPLICATIONS SERVICE #######################
    for mode, settings in modes.items():
        for app, path in settings['apps'].items():
            # send mutation to deregister app (name is required, version is optional)
            request = '''
            mutation {
                uninstall(name: "%s", version: "1.0") {
                    success,
                    errors
                }
            }
            ''' % (app)
            response = SERVICES.query(service="app-service", query=request)

            # get results
            response = response["uninstall"]
            success = response["success"]
            errors = response["errors"]

            if success:
                logger.info("Deregistered app: {}".format(app))
            else:
                # check if error is due to no app existing in registry
                if ("not found" in errors):
                    logger.info("No app named: {} found in registry.".format(app))
                else:
                    logger.warning("Unable to deregister app {}: {}".format(app, errors))

    print("\n")
    ################## REGISTER APPLICATIONS WITH APPLICATIONS SERVICE #######################
    for mode, settings in modes.items():
        for app, path in settings['apps'].items():

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
                # check if error is due to app already existing in registry
                if ("exists" in errors):
                    logger.info("Already a registered app named: {}.".format(app))
                else:
                    logger.warning("Could not register app {} at path {}: {}".format(app, path, errors))

    print("\n")
    ################# REMOVE REGISTERED APPS FROM SPECIFIC MISSION MODES #####################
    #for mode, settings in modes.items():
    #    
    #    # add safe mode tasks/mission apps to safe mode
    #    path = settings['path']
    #    name = settings['name']
    #    mode = settings['mode']
    #    
    #    # send mutation to remove task list from mode in scheduler
    #    request = '''
    #    mutation {
    #        removeTaskList(name: "%s", mode: "%s") {
    #            success
    #            errors
    #        }
    #    }
    #    ''' % (name, mode)
    #    response = SERVICES.query(service="scheduler-service", query=request)
    #
    #    # get results
    #    response = response["removeTaskList"]
    #    success = response["success"]
    #    errors = response["errors"]
    #
    #    if success:
    #        logger.info("Removed task list {} from mode {}.".format(name, mode))
    #    else:
    #        logger.warning("Could not remove task list {} from mode {}: {}.".format(name, mode, errors))
    #
    #print("\n")
    ################# INSTALL REGISTERED APPS INTO SPECIFIC MISSION MODES #####################
    for mode, settings in modes.items():
        
        # add safe mode tasks/mission apps to safe mode
        path = settings['path']
        name = settings['name']
        mode = settings['mode']

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