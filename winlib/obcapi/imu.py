import smbus
import logging
import graphene
from winserial import i2c
import struct
from math import sqrt, atan2, asin, degrees, radians
import time
from deltat import DeltaT


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


_FXAS21002C_ADDRESS       = 0x21  # 0100001
_FXAS21002C_ID            = 0xD7       # 1101 0111
_GYRO_REGISTER_STATUS     = 0x00
_GYRO_REGISTER_OUT_X_MSB  = 0x01
_GYRO_REGISTER_OUT_X_LSB  = 0x02
_GYRO_REGISTER_OUT_Y_MSB  = 0x03
_GYRO_REGISTER_OUT_Y_LSB  = 0x04
_GYRO_REGISTER_OUT_Z_MSB  = 0x05
_GYRO_REGISTER_OUT_Z_LSB  = 0x06
_GYRO_REGISTER_WHO_AM_I   = 0x0C   # 11010111   r
_GYRO_REGISTER_CTRL_REG0  = 0x0D  # 00000000   r/w
_GYRO_REGISTER_CTRL_REG1  = 0x13  # 00000000   r/w
_GYRO_REGISTER_CTRL_REG2  = 0x14  # 00000000   r/w
_GYRO_SENSITIVITY_250DPS  = 0.0078125    # Table 35 of datasheet
_GYRO_SENSITIVITY_500DPS  = 0.015625     # ..
_GYRO_SENSITIVITY_1000DPS = 0.03125     # ..
_GYRO_SENSITIVITY_2000DPS = 0.0625      # .

_MAG_UT_LSB                     = 0.1
_ACCEL_MG_LSB_2G                = 0.000244
_SENSORS_GRAVITY_STANDARD       = 9.80665

logger = logging.getLogger('imu-service')
class IMU(graphene.ObjectType):
    declination = 0
    def __init__(self, bus, timediff=None):

        timediff = lambda start, end : (start-end)/1000000
        self.magbias = (0, 0, 0)
        self.q = [1.0, 0.0, 0.0, 0.0]
        GyroMeasError = radians(40)
        self.beta = sqrt(3.0 / 4.0) * GyroMeasError
        self.deltat = DeltaT(timediff)

        try:
            self.fxos_i2c = i2c.I2C(bus=bus, slave_address=_FXOS8700_ADDRESS)
            self.fxas_i2c = i2c.I2C(bus=bus, slave_address=_FXAS21002C_ADDRESS)
        except Exception as e:
            logger.info("Unable to open I2C bus {} to device: {}. Will use fake i2c for testing.".format(bus, _FXOS8700_ADDRESS))
            self.fxos_i2c = i2c.I2C_fake(bus=bus, slave_address=_FXOS8700_ADDRESS)
            self.fxas_i2c = i2c.I2C_fake(bus=bus, slave_address=_FXAS21002C_ADDRESS)
            return

        if self.fxos_i2c.read(_FXOS8700_REGISTER_WHO_AM_I) != _FXOS8700_ID:
            logger.info('Failed to find FXOS8700, check wiring!. Using fake i2c for now')
            self.fxos_i2c = i2c.I2C_fake(bus=bus, slave_address=_FXOS8700_ADDRESS)

        if self.fxas_i2c.read(_GYRO_REGISTER_WHO_AM_I) != _FXAS21002C_ID:
            logger.info('Failed to find FXAS21002C, check wiring!. Using fake i2c for now')
            self.fxas_i2c = i2c.I2C_fake(bus=bus, slave_address=_FXAS21002C_ADDRESS)

        # Set to standby mode (required to make changes to this register)
        self.fxos_i2c.write(_FXOS8700_REGISTER_CTRL_REG1, 0)
        # set accel range to 2G
        self.fxos_i2c.write(_FXOS8700_REGISTER_XYZ_DATA_CFG, 0x00)
        # High resolution
        self.fxos_i2c.write(_FXOS8700_REGISTER_CTRL_REG2, 0x02)
        # Active, Normal Mode, Low Noise, 100Hz in Hybrid Mode
        self.fxos_i2c.write(_FXOS8700_REGISTER_CTRL_REG1, 0x15)
        # Configure the magnetometer
        # Hybrid Mode, Over Sampling Rate = 16
        self.fxos_i2c.write(_FXOS8700_REGISTER_MCTRL_REG1, 0x1F)
        # Jump to reg 0x33 after reading 0x06
        self.fxos_i2c.write(_FXOS8700_REGISTER_MCTRL_REG2, 0x20)

        self.fxas_i2c.write(_GYRO_REGISTER_CTRL_REG0, 0x03) # Set sensitivity
        self.fxas_i2c.write(_GYRO_REGISTER_CTRL_REG1, 0x0E)     # Active
        time.sleep(0.1) # 60 ms + 1/ODR

    # return magnetometer data
    def mag(self):
        try:
            x_MSB = self.fxos_i2c.read(_FXOS8700_REGISTER_MOUT_X_MSB)
            x_LSB = self.fxos_i2c.read(_FXOS8700_REGISTER_MOUT_X_LSB)

            y_MSB = self.fxos_i2c.read(_FXOS8700_REGISTER_MOUT_Y_MSB)
            y_LSB = self.fxos_i2c.read(_FXOS8700_REGISTER_MOUT_Y_LSB)

            z_MSB = self.fxos_i2c.read(_FXOS8700_REGISTER_MOUT_Z_MSB)
            z_LSB = self.fxos_i2c.read(_FXOS8700_REGISTER_MOUT_Z_LSB)

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
            x_MSB = self.fxos_i2c.read(_FXOS8700_REGISTER_OUT_X_MSB)
            x_LSB = self.fxos_i2c.read(_FXOS8700_REGISTER_OUT_X_LSB)

            y_MSB = self.fxos_i2c.read(_FXOS8700_REGISTER_OUT_Y_MSB)
            y_LSB = self.fxos_i2c.read(_FXOS8700_REGISTER_OUT_Y_LSB)

            z_MSB = self.fxos_i2c.read(_FXOS8700_REGISTER_OUT_Z_MSB)
            z_LSB = self.fxos_i2c.read(_FXOS8700_REGISTER_OUT_Z_LSB)

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
        
    # return gyroscope x,y,z values
    def gyr(self):
        try:
            x_MSB = self.fxas_i2c.read(_GYRO_REGISTER_OUT_X_MSB)
            x_LSB = self.fxas_i2c.read(_GYRO_REGISTER_OUT_X_LSB)

            y_MSB = self.fxas_i2c.read(_GYRO_REGISTER_OUT_Y_MSB)
            y_LSB = self.fxas_i2c.read(_GYRO_REGISTER_OUT_Y_LSB)

            z_MSB = self.fxas_i2c.read(_GYRO_REGISTER_OUT_Z_MSB)
            z_LSB = self.fxas_i2c.read(_GYRO_REGISTER_OUT_Z_LSB)

            BUFFER = bytearray()
            BUFFER = [x_MSB, x_LSB, y_MSB, y_LSB, z_MSB, z_LSB]
            BUFFER = bytes(BUFFER)
            # Parse out the gyroscope data as 16-bit signed data.
            x = struct.unpack_from('>h', BUFFER[0:2])[0]
            y = struct.unpack_from('>h', BUFFER[2:4])[0]
            z = struct.unpack_from('>h', BUFFER[4:6])[0]

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

    def qua(self, ts=None):
        ts = time.time()
        success, errors, x, y, z = self.mag()
        mag = (x,y,z)
        success, errors, x, y, z = self.acc()
        accel = (x,y,z)
        success, errors, x, y, z = self.gyr()
        gyro = (x,y,z)

        mx, my, mz = (mag[x] - self.magbias[x] for x in range(3)) # Units irrelevant (normalised)
        ax, ay, az = accel                  # Units irrelevant (normalised)
        gx, gy, gz = (radians(x) for x in gyro)  # Units deg/s
        q1, q2, q3, q4 = (self.q[x] for x in range(4))   # short name local variable for readability
        # Auxiliary variables to avoid repeated arithmetic
        _2q1 = 2 * q1
        _2q2 = 2 * q2
        _2q3 = 2 * q3
        _2q4 = 2 * q4
        _2q1q3 = 2 * q1 * q3
        _2q3q4 = 2 * q3 * q4
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q1q4 = q1 * q4
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q2q4 = q2 * q4
        q3q3 = q3 * q3
        q3q4 = q3 * q4
        q4q4 = q4 * q4

        # Normalise accelerometer measurement
        norm = sqrt(ax * ax + ay * ay + az * az)
        if (norm == 0):
            return True, [], self.q[0], self.q[1], self.q[2], self.q[3]
        norm = 1 / norm                     # use reciprocal for division
        ax *= norm
        ay *= norm
        az *= norm

        # Normalise magnetometer measurement
        norm = sqrt(mx * mx + my * my + mz * mz)
        if (norm == 0):
            return True, [], self.q[0], self.q[1], self.q[2], self.q[3]
        norm = 1 / norm                     # use reciprocal for division
        mx *= norm
        my *= norm
        mz *= norm

        # Reference direction of Earth's magnetic field
        _2q1mx = 2 * q1 * mx
        _2q1my = 2 * q1 * my
        _2q1mz = 2 * q1 * mz
        _2q2mx = 2 * q2 * mx
        hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 + _2q2 * my * q3 + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4
        hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * q3 - my * q2q2 + my * q3q3 + _2q3 * mz * q4 - my * q4q4
        _2bx = sqrt(hx * hx + hy * hy)
        _2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * q4 - mz * q2q2 + _2q3 * my * q4 - mz * q3q3 + mz * q4q4
        _4bx = 2 * _2bx
        _4bz = 2 * _2bz

        # Gradient descent algorithm corrective step
        s1 = (-_2q3 * (2 * q2q4 - _2q1q3 - ax) + _2q2 * (2 * q1q2 + _2q3q4 - ay) - _2bz * q3 * (_2bx * (0.5 - q3q3 - q4q4)
             + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
             + _2bx * q3 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

        s2 = (_2q4 * (2 * q2q4 - _2q1q3 - ax) + _2q1 * (2 * q1q2 + _2q3q4 - ay) - 4 * q2 * (1 - 2 * q2q2 - 2 * q3q3 - az)
             + _2bz * q4 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4)
             + _2bz * (q1q2 + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

        s3 = (-_2q1 * (2 * q2q4 - _2q1q3 - ax) + _2q4 * (2 * q1q2 + _2q3q4 - ay) - 4 * q3 * (1 - 2 * q2q2 - 2 * q3q3 - az)
             + (-_4bx * q3 - _2bz * q1) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx)
             + (_2bx * q2 + _2bz * q4) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
             + (_2bx * q1 - _4bz * q3) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

        s4 = (_2q2 * (2 * q2q4 - _2q1q3 - ax) + _2q3 * (2 * q1q2 + _2q3q4 - ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (0.5 - q3q3 - q4q4)
              + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
              + _2bx * q2 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

        norm = 1 / sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4)    # normalise step magnitude
        s1 *= norm
        s2 *= norm
        s3 *= norm
        s4 *= norm

        # Compute rate of change of quaternion
        qDot1 = 0.5 * (-q2 * gx - q3 * gy - q4 * gz) - self.beta * s1
        qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy) - self.beta * s2
        qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx) - self.beta * s3
        qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx) - self.beta * s4

        # Integrate to yield quaternion
        deltat = self.deltat(ts)
        q1 += qDot1 * deltat
        q2 += qDot2 * deltat
        q3 += qDot3 * deltat
        q4 += qDot4 * deltat
        norm = 1 / sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4)    # normalise quaternion
        self.q = q1 * norm, q2 * norm, q3 * norm, q4 * norm
        self.heading = self.declination + degrees(atan2(2.0 * (self.q[1] * self.q[2] + self.q[0] * self.q[3]),
            self.q[0] * self.q[0] + self.q[1] * self.q[1] - self.q[2] * self.q[2] - self.q[3] * self.q[3]))
        self.pitch = degrees(-asin(2.0 * (self.q[1] * self.q[3] - self.q[0] * self.q[2])))
        self.roll = degrees(atan2(2.0 * (self.q[0] * self.q[1] + self.q[2] * self.q[3]),
            self.q[0] * self.q[0] - self.q[1] * self.q[1] - self.q[2] * self.q[2] + self.q[3] * self.q[3]))

        return True, [], self.q[0], self.q[1], self.q[2], self.q[3]


    def _twos_comp(self, val, bits):
        # Convert an unsigned integer in 2's compliment form of the specified bit
        # length to its signed integer value and return it.
        if val & (1 << (bits - 1)) != 0:
            return val - (1 << bits)
        return val