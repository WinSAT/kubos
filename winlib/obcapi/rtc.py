#!/usr/bin/env python3

from obcserial import i2c
import app_api

import smbus

DS3231_ADDRESS = 0x68

class RTC:
    """Interface to the DS3231 RTC."""

    #lost_power = i2c_bit.RWBit(0x0f, 7)
    """True if the device has lost power since the time was set."""

    #disable_oscillator = i2c_bit.RWBit(0x0e, 7)
    """True if the oscillator is disabled."""

    #datetime_register = i2c_bcd_datetime.BCDDateTimeRegister(0x00)
    """Current date and time."""

    #alarm1 = i2c_bcd_alarm.BCDAlarmTimeRegister(0x07)
    """Alarm time for the first alarm."""

    #alarm1_interrupt = i2c_bit.RWBit(0x0e, 0)
    """True if the interrupt pin will output when alarm1 is alarming."""

    #alarm1_status = i2c_bit.RWBit(0x0f, 0)
    """True if alarm1 is alarming. Set to False to reset."""

    #alarm2 = i2c_bcd_alarm.BCDAlarmTimeRegister(0x0b, has_seconds=False)
    """Alarm time for the second alarm."""

    #alarm2_interrupt = i2c_bit.RWBit(0x0e, 1)
    """True if the interrupt pin will output when alarm2 is alarming."""

    #alarm2_status = i2c_bit.RWBit(0x0f, 1)
    """True if alarm2 is alarming. Set to False to reset."""

    def __init__(self, bus, weekday_first=True, weekday_start=1):

        self.logger = app_api.logging_setup("rtc-service")
        self.buffer = bytearray(8)
        if weekday_first:
            self.weekday_offset = 0
        else:
            self.weekday_offset = 1
        self.weekday_start = weekday_start    

        try:
            self.i2c = i2c.I2C(bus=bus, slave_address=DS3231_ADDRESS)
        except Exception as e:
            self.logger.info("Unable to open I2C bus {} to device: {}. Will use fake i2c for testing.".format(bus, DS3231_ADDRESS))
            self.i2c = i2c.I2C_fake(bus=bus, slave_address=DS3231_ADDRESS)
            return

    def datetime(self):
        """Gets the current date and time or sets the current date and time
        then starts the clock."""

        time0 = self.i2c.read(0x00)
        time1 = self.i2c.read(0x01)
        time2 = self.i2c.read(0x02)
        time3 = self.i2c.read(0x03)
        time4 = self.i2c.read(0x04)
        time5 = self.i2c.read(0x05)
        time6 = self.i2c.read(0x06)
        time7 = self.i2c.read(0x07)

        BUFFER = bytearray()
        BUFFER = [time0,time1,time2,time3,time4,time5,time6,time7]
        BUFFER = bytes(BUFFER)

        time0 = struct.unpack_from('>H', BUFFER[0])[0]
        time1 = struct.unpack_from('>H', BUFFER[1])[0]
        time2 = struct.unpack_from('>H', BUFFER[2])[0]
        time3 = struct.unpack_from('>H', BUFFER[3])[0]
        time4 = struct.unpack_from('>H', BUFFER[4])[0]
        time5 = struct.unpack_from('>H', BUFFER[5])[0]
        time6 = struct.unpack_from('>H', BUFFER[6])[0]
        time7 = struct.unpack_from('>H', BUFFER[7])[0]

        print("Time:",0,1,2,3,4,5,6,7)

        return time.struct_time((_bcd2bin(self.buffer[7]) + 2000,
                                 _bcd2bin(self.buffer[6]),
                                 _bcd2bin(self.buffer[5 - self.weekday_offset]),
                                 _bcd2bin(self.buffer[3]),
                                 _bcd2bin(self.buffer[2]),
                                 _bcd2bin(self.buffer[1] & 0x7F),
                                 _bcd2bin(self.buffer[4 + self.weekday_offset] -
                                          self.weekday_start),
                                 -1,
                                 -1))

    #@datetime.setter
    #def datetime(self, value):
    #    self.datetime_register = value
    #    self.disable_oscillator = False
    #    self.lost_power = False