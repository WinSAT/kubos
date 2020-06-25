#!/usr/bin/env python3

"""
Mission application that collects the current telemetry from ADCS module.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("get-adcs-spin")

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
    
    # send mutation to turn off EPS port
    request = '''     
    query {
        telemetry {
            orientation { x y z yaw pitch roll }
            spin { x y z }
            mode { state }
            power { state }
        }
    } '''
    response = SERVICES.query(service="adcs-service", query=request)

    # get results
    result = response["telemetry"]

    spin = result['spin']
    x_spin = spin['x']
    y_spin = spin['y']
    z_spin = spin['z']

    orientation = result['orientation']
    x = orientation['x']
    y = orientation['y']
    z = orientation['z']
    yaw = orientation['yaw']
    pitch = orientation['pitch']
    roll = orientation['roll']

    mode = result['mode']
    mode = mode['state']

    power = result['power']
    power = power['state']

    logger.info("Got ADCS telemetry:\n power={} mode={}\n orientation=({},{},{},{},{}.{})\n spin=({},{},{})".format(
                power,
                mode,
                x,y,z,yaw,pitch,roll,
                x_spin,y_spin,z_spin
    ))

    logger.info("Storing telemetry in ADCS database...")

    # timestamp is optional and defaults to current system time
    request = '''
    mutation {
        insertBulk(entries: [
            { subsystem: "ADCS", parameter: "mode", value: "%s" },
            { subsystem: "ADCS", parameter: "power", value: "%s" },
            { subsystem: "ADCS", parameter: "x", value: "%s" },
            { subsystem: "ADCS", parameter: "y", value: "%s" },
            { subsystem: "ADCS", parameter: "z", value: "%s" },
            { subsystem: "ADCS", parameter: "yaw", value: "%s" },
            { subsystem: "ADCS", parameter: "pitch", value: "%s" },
            { subsystem: "ADCS", parameter: "roll", value: "%s" },
            { subsystem: "ADCS", parameter: "spin_x", value: "%s" },
            { subsystem: "ADCS", parameter: "spin_y", value: "%s" },
            { subsystem: "ADCS", parameter: "spin_z", value: "%s" }
        ]) 
        {
            success
            errors
        }
    }
    ''' % (mode,power,x,y,z,yaw,pitch,roll,x_spin,y_spin,z_spin)
    response = SERVICES.query(service="telemetry-service", query=request)

    # get results
    result = response["insertBulk"]
    success = result["success"]
    errors = result["errors"]

    if success:
        logger.info("Logged telemetry in database.")
    else:
        logger.warn("Unable to log telemetry to database: {}".format(errors))

if __name__ == "__main__":
    main()
