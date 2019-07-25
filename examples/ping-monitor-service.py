#!/usr/bin/env python3

import argparse
import app_api
import sys

def on_boot():

    print("OnBoot logic")

def on_command():

    request = '{ ping }'

    try:
        response = SERVICES.query(service="monitor-service", query=request)
    except Exception as e:
        print("Something went wrong: " + str(e))
        sys.exit(1)

    data = response["ping"]

    if data == "pong":
        print("Successfully pinged monitor service")
    else:
        print("Unexpected monitor service response: %s" % data)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--run', '-r')
    parser.add_argument('--config', '-c')

    args = parser.parse_args()

    if args.config is not None:
        global SERVICES
        SERVICES = app_api.Services(args.config)
    else:
        SERVICES = app_api.services()

    if args.run == 'OnBoot':
        on_boot()
    elif args.run == 'OnCommand':
        on_command()
    else:
        print("Unknown run level specified")
        sys.exit(1)

if __name__ == "__main__":
    main()
