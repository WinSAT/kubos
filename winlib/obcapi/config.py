#!/usr/bin/env python3

# RETURN CODES
RETURN_CODE = {
    0 : "OK",
    1 : "ERR",
    2 : "DONE",
    3 : "FAIL"
}

COMMANDS = {
    "ping",
    "capture_image",
    "transfer_image"
}

REGEX = "\<\<(.*?)\>\>"

CAMERA = {
    "resolution" : {"height": 1200, "width": 1600} 
}

DELAY = 1
RETRY = 5