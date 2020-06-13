#!/usr/bin/env python3

'''
API for interacting with ADCS subsystem
'''

from obcserial import i2c
import logging

class ADCS:

    def __init__(self):

        self.logger = logging.getLogger("adcs-service")

        # telemetry defaults
        self._power = 0  # (OFF=0,ON=1,RESET=2)
        self._mode = 0   # (IDLE=0,DETUMBLE=1,POINTING=2)
        self._orientation = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0]
        self._spin = [1.0, 1.0, 1.0]

        # ADCS initialize stuff here

################ queries ###################
    def ping(self):
        # should send hardware a ping and expect a pong back
        return "pong"

    def power(self):
        #############################################################
        # TODO: Get power state (ON=1, OFF=0, RESET=2) from ADCS here
        #############################################################
        return self._power

    def mode(self):
        ####################################################################
        # TODO: Get mode state (IDLE=1,DETUMBLE=0,POINTING=2) from ADCS here
        ####################################################################
        return self._mode

    def orientation(self):
        #############################################################
        # TODO: Get orientation (x,y,z,yaw,pitch,roll) from ADCS here
        #############################################################
        return self._orientation

    def spin(self):
        #######################################
        # TODO: Get spin (x,y,z) from ADCS here
        #######################################
        return self._spin

################ mutations #################
    # Controls the power state of the ADCS
    def controlPower(self, controlPowerInput):
        success = False
        errors = []
        try:
            self.logger.info("Sending new power state to ADCS...")
            power=controlPowerInput.power
            ####################################################################
            # TODO: Set mode state (IDLE=1,DETUMBLE=0,POINTING=2) from ADCS here
            ####################################################################
            success = True
            errors = []
            self._power = power

            if success:
                self.logger.info("Set ADCS power state={}".format(power))
            else:
                self.logger.error("Unable to set ADCS power state={}".format(power))
        
        except Exception as e:
            self.logger.error("Exception trying to set ADCS power state={} : {}".format(power, str(e)))
            success = False
            errors = [str(e)]
        
        finally: 
            return success, errors

    def setMode(self, setModeInput):
        success = False
        errors = []
        try:
            self.logger.info("Sending new mode to ADCS...")
            mode=setModeInput.mode
            ####################################################################
            # TODO: Set mode state (IDLE=1,DETUMBLE=0,POINTING=2) from ADCS here
            ####################################################################
            success = True
            errors = []
            self._mode = mode

            if success:
                self.logger.info("Set ADCS mode={}".format(mode))
            else:
                self.logger.error("Unable to set ADCS mode={}".format(mode))
        
        except Exception as e:
            self.logger.error("Exception trying to set ADCS mode={} : {}".format(mode, str(e)))
            success = False
            errors = [str(e)]
        
        finally: 
            return success, errors

