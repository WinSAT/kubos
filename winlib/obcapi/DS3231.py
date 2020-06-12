#!/usr/bin/env python3

from obcserial import i2c
import app_api
import smbus
import datetime

DS3231_ADDRESS = 0x68

class DS3231:
    """Interface to the DS3231 RTC."""

    def __init__(self, bus):
        """
        Sets I2C bus number and address
        """
        self.fake = False
        try:
            self.i2cfile = i2c.I2C(bus=bus, slave_address=DS3231_ADDRESS)
        except Exception as e:
            # exception trying to open i2c bus, run fake version
            self.fake = True

    def bcd2bin(self, value):
        """
        Convert binary coded decimal (bcd) to binary
        """
        return value - 6 * (value >> 4)

    def bin2bcd(self, value):
        """
        Convert binary value to binary coded decimal (bcd)
        """
        return value + 6 * (value // 10)

    def datetime(self):
        """
        Get current date and time from RTC.
        """
        if (self.fake):
            return datetime.datetime(1970, 1, 1, 0, 0, 0)

        sec = self.bcd2bin(self.i2cfile.read(0x00) & 0x7F) 
        minute = self.bcd2bin(self.i2cfile.read(0x01))
        hour = self.bcd2bin(self.i2cfile.read(0x02))
        wday = self.bcd2bin(self.i2cfile.read(0x03) - 1)
        mday = self.bcd2bin(self.i2cfile.read(0x04))
        month = self.bcd2bin(self.i2cfile.read(0x05))
        year = self.bcd2bin(self.i2cfile.read(0x06)) + 2000

        return datetime.datetime(year, month, mday, hour, minute, sec)