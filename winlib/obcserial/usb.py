#!/usr/bin/env python3

import usba.core
import time
from obcserial import config
import app_api

#class USB:
#    def __init__(self):  
#        self.logger = app_api.logging_setup("USB")

#dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)
dev = usba.core.find()
if dev is None:
    print('Our device is not connected')
else:
    print('Device is connected')