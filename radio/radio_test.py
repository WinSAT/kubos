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

    #spi_device.xfer([regAddr])
    #version = spi_device.xfer([0x00])

    #address = regAddr & 0x7F
    spi_device.xfer2([0x01,0x18])

    address = 0x80 | regAddr 
    resp = spi_device.xfer2([address,0x01])
    
    #resp = spi_device.xfer2([address,0x00,0x01,0x00,0x02,0x00,0x03,0x00,0x04,0x00,0x05,0x00,0x06,0x00,0x07,0x00,0x08,0x00,0x09,0x00,0x10,0x00,0x11,0x00,0x12,0x00,0x13,0x00,0x14,0x00,0x15,0x00,0x16,0x00,0x17,0x00])
    version = resp[1]
    print(version)
    print(resp)

    #version = read(_REG_VERSION)
    if version != 0x24:
        raise RuntimeError('Failed to find RFM69 with expected version, check wiring!. Found version: {}'.format(version))
    else:
        print("Found RFM69 device success.")

except Exception as e:
    print("Error trying to read from RMF69 device over SPI: {} | {}".format(type(e).__name__,str(e)))
