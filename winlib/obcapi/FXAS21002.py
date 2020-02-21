import smbus
import logging
import graphene
from winserial import i2c
import struct





logger = logging.getLogger('imu-service')
class FXAS21002:

    def __init__(self, bus):
        try:
            self.i2c = i2c.I2C(bus=bus, slave_address=_FXAS21002C_ADDRESS)
        except Exception as e:
            logger.info("Unable to open I2C bus {} to device: {}. Will use fake i2c for testing.".format(bus, _FXAS21002C_ADDRESS))
            self.i2c = i2c.I2C_fake(bus=bus, slave_address=_FXAS21002C_ADDRESS)
            return

        if self.i2c.read(_GYRO_REGISTER_WHO_AM_I) != _FXAS21002C_ID:
            logger.info('Failed to find FXAS21002C, check wiring!. Using fake i2c for now')
            self.i2c = i2c.I2C_fake(bus=bus, slave_address=_FXAS21002C_ADDRESS)

        self.i2c.write(_GYRO_REGISTER_CTRL_REG0, ctrl_reg0) # Set sensitivity
        self.i2c.write(_GYRO_REGISTER_CTRL_REG1, 0x0E)     # Active
        time.sleep(0.1) # 60 ms + 1/ODR

    # return gyroscope x,y,z values
    def gyr(self):
        try:
            x_MSB = self.i2c.read(_GYRO_REGISTER_OUT_X_MSB)
            x_LSB = self.i2c.read(_GYRO_REGISTER_OUT_X_LSB)

            y_MSB = self.i2c.read(_GYRO_REGISTER_OUT_Y_MSB)
            y_LSB = self.i2c.read(_GYRO_REGISTER_OUT_Y_LSB)

            z_MSB = self.i2c.read(_GYRO_REGISTER_OUT_Z_MSB)
            z_LSB = self.i2c.read(_GYRO_REGISTER_OUT_Z_LSB)

            BUFFER = bytearray()
            BUFFER = [x_MSB, x_LSB, y_MSB, y_LSB, z_MSB, z_LSB]
            BUFFER = bytes(BUFFER)
            # Parse out the gyroscope data as 16-bit signed data.
            x = struct.unpack_from('>h', self._BUFFER[0:2])[0]
            y = struct.unpack_from('>h', self._BUFFER[2:4])[0]
            z = struct.unpack_from('>h', self._BUFFER[4:6])[0]

            x = x * _GYRO_SENSITIVITY_250DPS
            y = y * _GYRO_SENSITIVITY_250DPS
            z = z * _GYRO_SENSITIVITY_250DPS

            success = True
            errors = []
            return success, errors, x, y, z

        except Exception as e:
            success = False
            errors = ["{}:{}".format(type(e).__name__,str(e))]
            return success, errors, None, None, None