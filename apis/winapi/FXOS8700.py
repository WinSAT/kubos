import smbus
import logging
import graphene
from winserial import i2c
import struct


_FXOS8700_ADDRESS               = 0x1F   # 0011111
_FXOS8700_ID                    = 0xC7   # 1100 0111
_FXOS8700_REGISTER_STATUS       = 0x00
_FXOS8700_REGISTER_OUT_X_MSB    = 0x01
_FXOS8700_REGISTER_OUT_X_LSB    = 0x02
_FXOS8700_REGISTER_OUT_Y_MSB    = 0x03
_FXOS8700_REGISTER_OUT_Y_LSB    = 0x04
_FXOS8700_REGISTER_OUT_Z_MSB    = 0x05
_FXOS8700_REGISTER_OUT_Z_LSB    = 0x06
_FXOS8700_REGISTER_WHO_AM_I     = 0x0D   # 11000111   r
_FXOS8700_REGISTER_XYZ_DATA_CFG = 0x0E
_FXOS8700_REGISTER_CTRL_REG1    = 0x2A   # 00000000   r/w
_FXOS8700_REGISTER_CTRL_REG2    = 0x2B   # 00000000   r/w
_FXOS8700_REGISTER_CTRL_REG3    = 0x2C   # 00000000   r/w
_FXOS8700_REGISTER_CTRL_REG4    = 0x2D   # 00000000   r/w
_FXOS8700_REGISTER_CTRL_REG5    = 0x2E   # 00000000   r/w
_FXOS8700_REGISTER_MSTATUS      = 0x32
_FXOS8700_REGISTER_MOUT_X_MSB   = 0x33
_FXOS8700_REGISTER_MOUT_X_LSB   = 0x34
_FXOS8700_REGISTER_MOUT_Y_MSB   = 0x35
_FXOS8700_REGISTER_MOUT_Y_LSB   = 0x36
_FXOS8700_REGISTER_MOUT_Z_MSB   = 0x37
_FXOS8700_REGISTER_MOUT_Z_LSB   = 0x38
_FXOS8700_REGISTER_MCTRL_REG1   = 0x5B   # 00000000   r/w
_FXOS8700_REGISTER_MCTRL_REG2   = 0x5C   # 00000000   r/w
_FXOS8700_REGISTER_MCTRL_REG3   = 0x5D   # 00000000   r/w

_MAG_UT_LSB                     = 0.1
_ACCEL_MG_LSB_2G                = 0.000244
_SENSORS_GRAVITY_STANDARD       = 9.80665

logger = logging.getLogger('imu-service')
class FXOS8700(graphene.ObjectType):

    def __init__(self, bus):
        try:
            self.i2c = i2c.I2C(bus=bus, slave_address=_FXOS8700_ADDRESS)
        except Exception as e:
            logger.info("Unable to open I2C bus {} to device: {}. Will use fake i2c for testing.".format(bus, _FXOS8700_ADDRESS))
            self.i2c = i2c.I2C_fake(bus=bus, slave_address=_FXOS8700_ADDRESS)
            return

        if self.i2c.read(_FXOS8700_REGISTER_WHO_AM_I) != _FXOS8700_ID:
            logger.info('Failed to find FXOS8700, check wiring!. Using fake i2c for now')
            self.i2c = i2c.I2C_fake(bus=bus, slave_address=_FXOS8700_ADDRESS)

        # Set to standby mode (required to make changes to this register)
        self.i2c.write(_FXOS8700_REGISTER_CTRL_REG1, 0)
        # set accel range to 2G
        self.i2c.write(_FXOS8700_REGISTER_XYZ_DATA_CFG, 0x00)
        # High resolution
        self.i2c.write(_FXOS8700_REGISTER_CTRL_REG2, 0x02)
        # Active, Normal Mode, Low Noise, 100Hz in Hybrid Mode
        self.i2c.write(_FXOS8700_REGISTER_CTRL_REG1, 0x15)
        # Configure the magnetometer
        # Hybrid Mode, Over Sampling Rate = 16
        self.i2c.write(_FXOS8700_REGISTER_MCTRL_REG1, 0x1F)
        # Jump to reg 0x33 after reading 0x06
        self.i2c.write(_FXOS8700_REGISTER_MCTRL_REG2, 0x20)

    # return magnetometer data
    def mag(self):
        try:
            x_MSB = self.i2c.read(_FXOS8700_REGISTER_MOUT_X_MSB)
            x_LSB = self.i2c.read(_FXOS8700_REGISTER_MOUT_X_LSB)

            y_MSB = self.i2c.read(_FXOS8700_REGISTER_MOUT_Y_MSB)
            y_LSB = self.i2c.read(_FXOS8700_REGISTER_MOUT_Y_LSB)

            z_MSB = self.i2c.read(_FXOS8700_REGISTER_MOUT_Z_MSB)
            z_LSB = self.i2c.read(_FXOS8700_REGISTER_MOUT_Z_LSB)

            BUFFER = bytearray()
            BUFFER = [x_MSB, x_LSB, y_MSB, y_LSB, z_MSB, z_LSB]
            BUFFER = bytes(BUFFER)
            x = struct.unpack_from('>H', BUFFER[0:2])[0]
            y = struct.unpack_from('>H', BUFFER[2:4])[0]
            z = struct.unpack_from('>H', BUFFER[4:6])[0]
            
            x = self._twos_comp(x >> 2, 14)
            y = self._twos_comp(y >> 2, 14)
            z = self._twos_comp(z >> 2, 14)

            x = x * _MAG_UT_LSB
            y = y * _MAG_UT_LSB
            z = z * _MAG_UT_LSB
        
            success = True
            errors = []
            return success, errors, x, y, z

        except Exception as e:
            success = False
            errors = ["{}:{}".format(type(e).__name__,str(e))]
            return success, errors, None, None, None

    # return accelerometer x,y,z values
    def acc(self):
        try:
            x_MSB = self.i2c.read(_FXOS8700_REGISTER_OUT_X_MSB)
            x_LSB = self.i2c.read(_FXOS8700_REGISTER_OUT_X_LSB)

            y_MSB = self.i2c.read(_FXOS8700_REGISTER_OUT_Y_MSB)
            y_LSB = self.i2c.read(_FXOS8700_REGISTER_OUT_Y_LSB)

            z_MSB = self.i2c.read(_FXOS8700_REGISTER_OUT_Z_MSB)
            z_LSB = self.i2c.read(_FXOS8700_REGISTER_OUT_Z_LSB)

            BUFFER = bytearray()
            BUFFER = [x_MSB, x_LSB, y_MSB, y_LSB, z_MSB, z_LSB]
            BUFFER = bytes(BUFFER)
            x = struct.unpack_from('>H', BUFFER[0:2])[0]
            y = struct.unpack_from('>H', BUFFER[2:4])[0]
            z = struct.unpack_from('>H', BUFFER[4:6])[0]
            
            x = self._twos_comp(x >> 2, 14)
            y = self._twos_comp(y >> 2, 14)
            z = self._twos_comp(z >> 2, 14)

            x = x * _ACCEL_MG_LSB_2G * _SENSORS_GRAVITY_STANDARD
            y = y * _ACCEL_MG_LSB_2G * _SENSORS_GRAVITY_STANDARD
            z = z * _ACCEL_MG_LSB_2G * _SENSORS_GRAVITY_STANDARD

            success = True
            errors = []
            return success, errors, x, y, z

        except Exception as e:
            success = False
            errors = ["{}:{}".format(type(e).__name__,str(e))]
            return success, errors, None, None, None
        

    def _twos_comp(self, val, bits):
        # Convert an unsigned integer in 2's compliment form of the specified bit
        # length to its signed integer value and return it.
        if val & (1 << (bits - 1)) != 0:
            return val - (1 << bits)
        return val