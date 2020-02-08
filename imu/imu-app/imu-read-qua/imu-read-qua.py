#!/usr/bin/env python3

"""
Mission application that reads all data from IMU and returns quaternion values
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys
import time

import serial
serial = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)

def main():

    logger = app_api.logging_setup("imu-read-qua")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('cmd_args', nargs='*')
    args = parser.parse_args()

    if args.config is not None:
        # use user config file if specified in command line
        SERVICES = app_api.Services(args.config[0])
    else:
        # else use default global config file
        SERVICES = app_api.Services()

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
    logger.info("Querying quaternion values from IMU...")
    while True:
        input("pause")
        try:
            request = '''
            { 
                qua {
                    success
                    errors
                    quaData {
                        q1
                        q2
                        q3
                        q4
                    }
                } 
            }
            '''
            response = SERVICES.query(service="imu-service", query=request)
            result = response["qua"]
            success = result["success"]
            errors = result["errors"]
            quaData = result["quaData"]
            q1 = quaData["q1"]
            q2 = quaData["q2"]
            q3 = quaData["q3"]
            q4 = quaData["q4"]

            if success:
                logger.info('Quaternion: ({}, {}, {}, {})'.format(q1,q2,q3,q4))
            else:
                logger.warning("Unable to retrieve quaternion data: {}".format(errors))

            try:
                # open uart port
                serial.close()
                serial.open()

                if serial.isOpen():
                    message = (q1,q2,q3,q4)
                    # if uart port is open, try to send encoded string message
                    serial.write(str(message).encode('utf-8'))
                    serial.close()
                    logger.debug("UART port is open. Sent message: {}".format(str(message)))
                else:
                    # if could not open uart port, return failure
                    serial.close()
                    logger.warn("Could not open serial port")

            # return failure if exception during write/encoding
            except Exception as e:
                logger.warn("Error sending message {} over uart port: {}".format(str(message), str(e)))


        except Exception as e:
            logger.warning("Unsuccessful getting data from quaternion: {}-{}".format(type(e).__name__,str(e)))

if __name__ == "__main__":
    main()
