#!/usr/bin/env python3

'''
API for interacting with EPS subsystem
'''

import time
import re
import logging

# for controlling power ports
from obcserial import gpio
# for reading battery levels through ADC
from obcapi import ADS1115

class EPS:

    def __init__(self):

        self.logger = logging.getLogger("eps-service")

########################### SUNFLOWER SOLAR POWER MANAGER ##############################
        # initialize GPIO pins
        self.PORT1 = gpio.GPIO(66)
        self.PORT2 = gpio.GPIO(69)
        self.PORT3 = gpio.GPIO(45)

        self.fake_GPIO = True

        self.PORT1.release()
        self.PORT2.release()
        self.PORT3.release()

        # attach GPIO pins
        if self.PORT1.attach():
            if self.PORT2.attach():
                if self.PORT3.attach():
                    self.fake_GPIO = False

        if self.fake_GPIO == False:
            # set GPIO direction
            self.PORT1.direction(1)
            self.PORT2.direction(1)
            self.PORT3.direction(1)    

            # make sure everything is off
            self.PORT1.off()
            self.PORT2.off()
            self.PORT3.off()

        self.power1 = False # power to output 1 off
        self.power2 = False # power to output 2 off
        self.power3 = False # power to output 3 off

############################# ADAFRUIT ADS1115 ADC ######################################
        
        # using Adafruit ADS1115 16-bit, 4 channel ADC
        self.adc = ADS1115.ADS1115()

        # Start continuous ADC conversions on channel 0 using the previously set gain
        # value.  Note you can also pass an optional data_rate parameter, see the simpletest.py
        # example and read_adc function for more infromation.

        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        self.adc.start_adc(channel=0, gain=1)

        # Once continuous ADC conversions are started you can call get_last_result() to
        # retrieve the latest result, or stop_adc() to stop conversions.

        # adc reading on full battery
        # usually 2^16/2 but using a voltage divider
        self.max_adc_reading = 24490

        # max voltage from sunflower solar manager that means full battery
        self.full_battery_voltage = 4.2

    # test service connection
    def ping(self):
        return "pong"

    # control power of ports
    def controlPort(self, controlPortInput):
        if self.fake_GPIO:
            if (controlPortInput.power == 1):
                self.power1 = True
            elif (controlPortInput.power == 2):
                self.power2 = True
            elif (controlPortInput.power == 3):
                self.power3 = True
            return True
          
        if (controlPortInput.port == 1):
            if (controlPortInput.power == 1):
                self.PORT1.on()
                self.power1 = True
            else:
                self.PORT1.off()
                self.power1 = False
            return True
        elif (controlPortInput.port == 2):
            if (controlPortInput.power == 1):
                self.PORT2.on()
                self.power2 = True
            else:
                self.PORT2.off()
                self.power2 = False
            return True
        elif (controlPortInput.port == 3):
            if (controlPortInput.power == 1):
                self.PORT3.on()
                self.power3= True
            else:
                self.PORT3.off()
                self.power3 = False
            return True
        else:
            return False

    # get power state of all ports
    def power(self):
        return self.power1, self.power2, self.power3

    # get current battery level as percentage
    def battery(self):

        # read ADC value
        value = self.adc.get_last_result()
        # get percentage of highest reading
        if value < self.max_adc_reading:
            percentage = float(value)/float(self.max_adc_reading)
        else:
            percentage = 1.0

        # convert to voltage
        voltage = percentage * self.full_battery_voltage

        return int(percentage * 100)

    # release GPIO pins
    def __exit__(self):
        if self.fake_GPIO == False:
            self.PORT1.release()
            self.PORT2.release()
            self.PORT3.release()

        # stop adc
        self.adc.stop_adc()