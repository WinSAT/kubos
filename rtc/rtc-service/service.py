#!/usr/bin/env python3

"""
Boilerplate service code which reads the config file and starts up the
GraphQL/HTTP endpoint. (should not need to much modification)
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import logging

from service import schema
from logging.handlers import SysLogHandler
import sys
#import toml

#print("hello")
from kubos_service.config import Config
config = Config("rtc-service")
#print(toml.dumps(config))

# Setup logging
logger = logging.getLogger("rtc-service")
logger.setLevel(logging.DEBUG)
handler = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_DAEMON)
formatter = logging.Formatter('rtc-service: %(message)s')
handler.formatter = formatter
logger.addHandler(handler)

# Set up a handler for logging to stdout
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setFormatter(formatter)
logger.addHandler(stdout)

from kubos_service import http_service
# Start an http service
http_service.start(config, schema.schema)

#from kubos_service import udp_service

# Start a udp service with optional context
# udp_service.start(config, schema, {'bus': '/dev/ttyS3'})

# Start a udp service
#udp_service.start(logger, config, schema)
