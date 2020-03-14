#!/usr/bin/env python3

import time
import spidev

# Internal constants:
_REG_FIFO            = 0x00
_REG_OP_MODE         = 0x01
_REG_DATA_MOD        = 0x02
_REG_BITRATE_MSB     = 0x03
_REG_BITRATE_LSB     = 0x04
_REG_FDEV_MSB        = 0x05
_REG_FDEV_LSB        = 0x06
_REG_FRF_MSB         = 0x07
_REG_FRF_MID         = 0x08
_REG_FRF_LSB         = 0x09
_REG_VERSION         = 0x10
_REG_PA_LEVEL        = 0x11
_REG_RX_BW           = 0x19
_REG_AFC_BW          = 0x1A
_REG_RSSI_VALUE      = 0x24
_REG_DIO_MAPPING1    = 0x25
_REG_IRQ_FLAGS1      = 0x27
_REG_IRQ_FLAGS2      = 0x28
_REG_PREAMBLE_MSB    = 0x2C
_REG_PREAMBLE_LSB    = 0x2D
_REG_SYNC_CONFIG     = 0x2E
_REG_SYNC_VALUE1     = 0x2F
_REG_PACKET_CONFIG1  = 0x37
_REG_FIFO_THRESH     = 0x3C
_REG_PACKET_CONFIG2  = 0x3D
_REG_AES_KEY1        = 0x3E
_REG_TEMP1           = 0x4E
_REG_TEMP2           = 0x4F
_REG_TEST_PA1        = 0x5A
_REG_TEST_PA2        = 0x5C
_REG_TEST_DAGC       = 0x6F

_TEST_PA1_NORMAL     = 0x55
_TEST_PA1_BOOST      = 0x5D
_TEST_PA2_NORMAL     = 0x70
_TEST_PA2_BOOST      = 0x7C

# The crystal oscillator frequency and frequency synthesizer step size.
# See the datasheet for details of this calculation.
_FXOSC  = 32000000.0
_FSTEP  = _FXOSC / 524288

# RadioHead specific compatibility constants.
_RH_BROADCAST_ADDRESS = 0xFF

# User facing constants:
SLEEP_MODE   = 0b000
STANDBY_MODE = 0b001
FS_MODE      = 0b010
TX_MODE      = 0b011
RX_MODE      = 0b100
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

def read(address):
    address = address & 0x7F
    resp = spi_device.xfer([address,0])
    if resp[1] == 0x24:
        print("Correct Version*************************************")
    return resp[1]

def write(address, data):
    print("Add",hex(address),hex(data))
    address = (address | 0x80) & 0xFF
    print("Add",hex(address),hex(data))
    spi_device.xfer([address,data])
    return True

def listen(self):
    """Listen for packets to be received by the chip.  Use :py:func:`receive` to listen, wait
        and retrieve packets as they're available.
    """
    # Like RadioHead library, turn off high power boost if enabled.
    if self._tx_power >= 18:
        self._write_u8(_REG_TEST_PA1, _TEST_PA1_NORMAL)
        self._write_u8(_REG_TEST_PA2, _TEST_PA2_NORMAL)
    # Enable payload ready interrupt for D0 line.
    self.dio_0_mapping = 0b01
    # Enter RX mode (will clear FIFO!).
    self.operation_mode = RX_MODE

try:
    spi_device = spidev.SpiDev()
    spi_device.open(1, 0)
    spi_device.max_speed_hz = 8000000

    regAddr = _REG_FIFO

# set frequency
    # Calculate FRF register 24-bit value using section 6.2 of the datasheet.
    frf = int((915 * 1000000.0) / _FSTEP) & 0xFFFFFF
    # Extract byte values and update registers.
    msb = frf >> 16
    mid = (frf >> 8) & 0xFF
    lsb = frf & 0xFF
    write(_REG_FRF_MSB, msb)
    write(_REG_FRF_MID, mid)
    write(_REG_FRF_LSB, lsb)

    #spi_device.xfer([regAddr])
    #version = spi_device.xfer([0x00])

    #address = regAddr & 0x7F
    #spi_device.xfer2([0x01,0x18])

    #address = 0x80 | regAddr 
    #resp = spi_device.xfer2([address,0x01])
    
    #resp = spi_device.xfer2([address,0x00,0x01,0x00,0x02,0x00,0x03,0x00,0x04,0x00,0x05,0x00,0x06,0x00,0x07,0x00,0x08,0x00,0x09,0x00,0x10,0x00,0x11,0x00,0x12,0x00,0x13,0x00,0x14,0x00,0x15,0x00,0x16,0x00,0x17,0x00])
    #version = resp[1]
    #write(_REG_TEST_PA1,_TEST_PA1_NORMAL)
    #print(read(_REG_TEST_PA1))
    #print(resp)
    #print(read(_REG_TEST_DAGC))
    #write(_REG_TEST_DAGC, 0x30)
    #print(read(_REG_TEST_DAGC))
    #print("\n")

    for i in range(20):
        print(i+1, hex(i+1), read(i+1), hex(read(i+1)))

    # set RX Mode
    #assert 0 <= val <= 4
    # Set the mode bits inside the operation mode register.
    op_mode = read(_REG_OP_MODE)
    op_mode &= 0b11100011
    op_mode |= (4 << 2)
    write(_REG_OP_MODE, op_mode)
    # Wait for mode to change by polling interrupt bit.
    time.sleep(5)

    # get current mode
    op_mode = read(_REG_OP_MODE)
    print((op_mode >> 2) & 0b111)

    print("Version: ", read(_REG_VERSION))
    while(1):
        print("Got data: ", read(regAddr))
        time.sleep(1)


    #version = read(_REG_VERSION)
    #if version != 0x24:
    #    raise RuntimeError('Failed to find RFM69 with expected version, check wiring!. Found version: {}'.format(version))
    #else:
    #    print("Found RFM69 device success.")

except Exception as e:
    print("Error trying to read from RMF69 device over SPI: {} | {}".format(type(e).__name__,str(e)))
