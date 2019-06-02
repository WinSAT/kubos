#!/usr/bin/python3

import argparse
import app_api
import sys

SERVICES = app_api.Services()

def on_boot(logger):
    
    logger.info("OnBoot logic")

def on_command(logger):
    
    request = '{memInfo{available}}'

    try:
        response = SERVICES.query(service="monitor-service", query=request)
    except Exception as e:
        logger.error("Something went wrong: " + str(e))
        sys.exit(1)

    data = response["memInfo"]
    available = data["available"]

    logger.info("Current available memory: %s kB" % (available))

    request = '''
        mutation {
            insert(subsystem: "OBC", parameter: "available_mem", value: "%s") {
                success,
                errors
            }
        }
        ''' % (available)

    try:
        response = SERVICES.query(service="telemetry-service", query=request)
    except Exception as e:
        logger.error("Something went wrong: " + str(e))
        sys.exit(1)

    data = response["insert"]
    success = data["success"]
    errors = data["errors"]

    if success == False:
        logger.error("Telemetry insert encountered errors: " + str(errors))
        sys.exit(1)
    else:
        logger.info("Telemetry insert completed successfully")

def main():
    
    logger = app_api.logging_setup("my-mission-app")
 
    parser = argparse.ArgumentParser()

    parser.add_argument('--run', '-r')

    args = parser.parse_args()

    if args.run == 'OnBoot':
        on_boot(logger)
    elif args.run == 'OnCommand':
        on_command(logger)
    else:
        logger.error("Unknown run level specified")
        sys.exit(1)

if __name__ == "__main__":
    main()

    


