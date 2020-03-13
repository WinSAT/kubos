#!/usr/bin/env python3

import time
import spidev

_REG_VERSION         = 0x10
'''
def read(regAddr):
    address = 0x80 | regAddr 
    resp = self.spi.xfer2([address,0x00])
    return resp[1]

def _read_into(self, address, buf, length=None):
    # Read a number of bytes from the specified address into the provided
    # buffer.  If length is not specified (the default) the entire buffer
    # will be filled.
    if length is None:
        length = len(buf)
    with self._device as device:
        self._BUFFER[0] = address & 0x7F  # Strip out top bit to set 0
                                        # value (read).
        device.write(self._BUFFER, end=1)
        device.readinto(buf, end=length)

def read_u8(self, address):
    # Read a single byte from the provided address and return it.
    self._read_into(address, self._BUFFER, length=1)
    return self._BUFFER[0]
'''
try:
    spi_device = spidev.SpiDev()
    spi_device.open(1, 0)

    regAddr = _REG_VERSION
    address = 0x80 | regAddr 
    resp = spi_device.xfer2([address,0x00])
    version = resp[1]

    #version = read(_REG_VERSION)
    if version != 0x24:
        raise RuntimeError('Failed to find RFM69 with expected version, check wiring!. Found version: {}'.format(version))
    else:
        print("Found RFM69 device success.")

except Exception as e:
    print("Error trying to read from RMF69 device over SPI: {} | {}".format(type(e).__name__,str(e)))
