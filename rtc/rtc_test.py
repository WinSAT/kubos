#!/usr/bin/env python3

from obcserial import i2c
import struct

def _bcd2bin(value):
    """Convert binary coded decimal to Binary
    :param value: the BCD value to convert to binary (required, no default)
    """
    return value - 6 * (value >> 4)

def _bin2bcd(value):
    """Convert a binary value to binary coded decimal.
    :param value: the binary value to convert to BCD. (required, no default)
    """
    return value + 6 * (value // 10)

DS3231_ADDRESS = 0x68

i2c = i2c.I2C(bus=2, slave_address=DS3231_ADDRESS)

# set date
'''
sec = 0
min = 28
hour = 19
wday = 3
mday = 11
month = 3
year = 2020

i2c.write(0x00, _bin2bcd(sec) & 0x7F)
i2c.write(0x01, _bin2bcd(min))
i2c.write(0x02, _bin2bcd(hour))
i2c.write(0x03, _bin2bcd(wday + 1))
i2c.write(0x04, _bin2bcd(mday))
i2c.write(0x05, _bin2bcd(month))
i2c.write(0x06, _bin2bcd(year - 2000))
'''

# get date
sec = _bcd2bin(i2c.read(0x00) & 0x7F) 
min = _bcd2bin(i2c.read(0x01))
hour = _bcd2bin(i2c.read(0x02))
wday = _bcd2bin(i2c.read(0x03) - 1)
mday = _bcd2bin(i2c.read(0x04))
month = _bcd2bin(i2c.read(0x05))
year = _bcd2bin(i2c.read(0x06)) + 2000

print("{}-{}-{}-{} {}-{}-{}".format(year, month, mday, wday, hour, min, sec))