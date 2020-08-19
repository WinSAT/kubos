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
        self._orientation = [1.0, 1.0, 1.0, 1.0]
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

    def setModePointing(self, pointingInput):
        success = False
        errors = []
        try:
            self.logger.info("Pointing ADCS...")

            # set mode to Pointing-  wouldn't need this if connected to real ADCS subsystem
            self._mode = 2  # pointing
            
            a=pointingInput.a
            b=pointingInput.b
            c=pointingInput.c
            d=pointingInput.d
            ####################################################################
            # TODO: Perform pointing of ADCS here
            self._orientation[0] = a
            self._orientation[1] = b
            self._orientation[2] = c
            self._orientation[3] = d
            ####################################################################
            success = True
            errors = []

            # set mode to IDLE once done - wouldn't need this if connected to real ADCS subsystem
            self._mode = 1 # idle

            if success:
                self.logger.info("Set ADCS pointing to orienation=({},{},{},{})".format(a,b,c,d))
            else:
                self.logger.error("Unable to point ADCS: {}".format(errors))
        
        except Exception as e:
            self.logger.error("Exception trying to pointing ADCS: {}".format(str(e)))
            success = False
            errors = [str(e)]
        
        finally: 
            return success, errors

    def setModeDetumble(self):
        success = False
        errors = []
        try:
            self.logger.info("Commanding ADCS to detumble...")

            # set mode to detumble -  wouldn't need this if connected to real ADCS subsystem
            self._mode = 0 # detumble
            
            ####################################################################
            # TODO: Perform detumble of ADCS here
            ####################################################################
            success = True
            errors = []

            # set mode to IDLE once done
            self._mode = 1 # idle

            if success:
                self.logger.info("Set ADCS to detumble")
            else:
                self.logger.error("Unable to set ADCS to detumble")
        
        except Exception as e:
            self.logger.error("Exception trying to set ADCS to detumble: {}".format(str(e)))
            success = False
            errors = [str(e)]
        
        finally: 
            return success, errors

    def setModeIdle(self):
        success = False
        errors = []
        try:
            self.logger.info("Commanding ADCS to idle...")

            # set mode to idle -  wouldn't need this if connected to real ADCS subsystem
            self._mode = 1 # idle
            
            ####################################################################
            # TODO: Set ADCS idle here
            ####################################################################
            success = True
            errors = []

            if success:
                self.logger.info("Set ADCS to idle")
            else:
                self.logger.error("Unable to set ADCS to idle")
        
        except Exception as e:
            self.logger.error("Exception trying to set ADCS to idle: {}".format(str(e)))
            success = False
            errors = [str(e)]
        
        finally: 
            return success, errors