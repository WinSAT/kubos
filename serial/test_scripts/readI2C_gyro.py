#!/usr/bin/env python3

import serial
import time
import argparse
from i2c import I2C
import struct
import smbus

# accelerometer and magnetometer
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


# https://github.com/adafruit/Adafruit_CircuitPython_FXAS21002C/blob/master/adafruit_fxas21002c.py#L62
# gyroscope
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
_GYRO_SENSITIVITY_2000DPS = 0.0625      # ..

# get address name from arguments
parser = argparse.ArgumentParser()
#parser.add_argument('address', type=str, help='address number to read from')
#parser.add_argument('num_read', type=int, help='number of bytes to read')
args = parser.parse_args()

# i2c setup
bus = smbus.SMBus(2)
i2c_device = I2C(bus = 2)
slave_address = 0x21
BUFFER = bytearray(7)


# Gyroscope constants/module globals:
GYRO_RANGE_250DPS   = 250
GYRO_RANGE_500DPS   = 500
GYRO_RANGE_1000DPS  = 1000
GYRO_RANGE_2000DPS  = 2000
_gyro_range = GYRO_RANGE_250DPS
_device= I2C(bus = 2)

_MAG_UT_LSB                     = 0.1
_ACCEL_MG_LSB_2G                = 0.000244
_SENSORS_GRAVITY_STANDARD       = 9.80665

def writeto(address, buffer, *, start=0, end=None, stop=True):
	if end is None:
		end = len(buffer)
	self._i2c_bus.write_bytes(address, buffer[start:end])

def readfrom_into(address, buffer, *, start=0, end=None, stop=True):
	if end is None:
		end = len(buffer)
	
	readin = self._i2c_bus.read_bytes(address, end-start)
	for i in range(end-start):
		buffer[i+start] = readin[i]

def writeto_then_readfrom(address, buffer_out, buffer_in, *,
                          out_start=0, out_end=None,
                          in_start=0, in_end=None, stop=False):
	if out_end is None:
		out_end = len(buffer_out)        
	if in_end is None:
		in_end = len(buffer_in)
	if stop:
		# To generate a stop in linux, do in two transactions
		writeto(address, buffer_out, start=out_start, end=out_end, stop=True)
		readfrom_into(address, buffer_in, start=in_start, end=in_end)
	else:
		# To generate without a stop, do in one block transaction
		print("type: {}".format(type(address)))
		print("type: {}".format(type(buffer_out[out_start:out_end])))
		print("type: {}".format(buffer_out[out_start:out_end]))
		print("type: {}".format(type(in_end-in_start)))

		print("buffer: {}".format(buffer_out))
		print("buffer_index: {}".format(buffer_out[out_start:out_end]))
		print("start: {}:{}".format(out_start, out_end))

		#readin = bus.read_i2c_block_data(address, buffer_out[out_start:out_end], in_end-in_start)
		readin = bus.read_i2c_block_data(address, 0x0D, in_end-in_start)
		for i in range(in_end-in_start):
			buffer_in[i+in_start] = readin[i]

def write_then_readinto(out_buffer, in_buffer, *,
                        out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
	if out_end is None:
		out_end = len(out_buffer)
	if in_end is None:
		in_end = len(in_buffer)
	if stop:
		print("Stop must be False. Use writeto instead.")
	#if hasattr(self.i2c, 'writeto_then_readfrom'):
		# In linux, at least, this is a special kernel function call
	writeto_then_readfrom(slave_address, out_buffer, in_buffer,
                              out_start=out_start, out_end=out_end,
                              in_start=in_start, in_end=in_end)

	#else:
		# If we don't have a special implementation, we can fake it with two calls
	#	self.write(out_buffer, start=out_start, end=out_end, stop=False)
	#	self.readinto(in_buffer, start=in_start, end=in_end)

def _read_u8(address):
	# Read an 8-bit unsigned value from the specified 8-bit address.
	BUFFER[0] = address & 0xFF
	print("BUFFER: {}".format(BUFFER))
	write_then_readinto(BUFFER, BUFFER, out_end=1, in_end=1)
	return BUFFER[0]

def read(register_address):
	return bus.read_byte_data(slave_address, register_address)

def read_word(register_address):
	return bus.read_word_data(slave_address, register_address)

def write(register_address, data):
	return bus.write_byte_data(slave_address, register_address, data)

# Gyro
def read_raw():
    # Read the raw gyroscope readings.  Returns a 3-tuple of X, Y, Z axis
    # 16-bit signed values.  If you want the gyroscope values in friendly
    # units consider using the gyroscope property!

    # Read gyro data from the sensor.
    x_MSB = read(_GYRO_REGISTER_OUT_X_MSB)
    x_LSB = read(_GYRO_REGISTER_OUT_X_LSB)

    y_MSB = read(_GYRO_REGISTER_OUT_Y_MSB)
    y_LSB = read(_GYRO_REGISTER_OUT_Y_LSB)

    z_MSB = read(_GYRO_REGISTER_OUT_Z_MSB)
    z_LSB = read(_GYRO_REGISTER_OUT_Z_LSB)

    BUFFER = bytearray()
    BUFFER = [x_MSB, x_LSB, y_MSB, y_LSB, z_MSB, z_LSB]
    BUFFER = bytes(BUFFER)
 
    # Parse out the gyroscope data as 16-bit signed data.
    raw_x = struct.unpack_from('>h', BUFFER[0:2])[0]
    raw_y = struct.unpack_from('>h', BUFFER[2:4])[0]
    raw_z = struct.unpack_from('>h', BUFFER[4:6])[0]

    factor = 0
    if _gyro_range == GYRO_RANGE_250DPS:
        factor = _GYRO_SENSITIVITY_250DPS
    elif _gyro_range == GYRO_RANGE_500DPS:
        factor = _GYRO_SENSITIVITY_500DPS
    elif _gyro_range == GYRO_RANGE_1000DPS:
        factor = _GYRO_SENSITIVITY_1000DPS
    elif _gyro_range == GYRO_RANGE_2000DPS:
        factor = _GYRO_SENSITIVITY_2000DPS
    raw_x = factor * raw_x
    raw_y = factor * raw_y
    raw_z = factor * raw_z

    print ("GYRO: X {} | Y {} | Z {}".format(raw_x, raw_y, raw_z))

def init():
        gyro_range=GYRO_RANGE_250DPS
        assert gyro_range in (GYRO_RANGE_250DPS, GYRO_RANGE_500DPS,
                              GYRO_RANGE_1000DPS, GYRO_RANGE_2000DPS)
        # Check for chip ID value.
        if read(_GYRO_REGISTER_WHO_AM_I) != _FXAS21002C_ID:
            print('Failed to find FXAS21002C, check wiring!')
            exit()

        _gyro_range = gyro_range
        ctrl_reg0 = 0x00
        if gyro_range == GYRO_RANGE_250DPS:
            ctrl_reg0 = 0x03
        elif gyro_range == GYRO_RANGE_500DPS:
            ctrl_reg0 = 0x02
        elif gyro_range == GYRO_RANGE_1000DPS:
            ctrl_reg0 = 0x01
        elif gyro_range == GYRO_RANGE_2000DPS:
            ctrl_reg0 = 0x00

        write(_GYRO_REGISTER_CTRL_REG0, ctrl_reg0) # Set sensitivity
        write(_GYRO_REGISTER_CTRL_REG1, 0x0E)     # Active


def _twos_comp(val, bits):
    # Convert an unsigned integer in 2's compliment form of the specified bit
    # length to its signed integer value and return it.
    if val & (1 << (bits - 1)) != 0:
        return val - (1 << bits)
    return val

def readAccelData2():
	# X,Y,Z axis 16-bit signed raw value
	x_MSB = read(_FXOS8700_REGISTER_OUT_X_MSB)
	x_LSB = read(_FXOS8700_REGISTER_OUT_X_LSB)

	y_MSB = read(_FXOS8700_REGISTER_OUT_Y_MSB)
	y_LSB = read(_FXOS8700_REGISTER_OUT_Y_LSB)

	z_MSB = read(_FXOS8700_REGISTER_OUT_Z_MSB)
	z_LSB = read(_FXOS8700_REGISTER_OUT_Z_LSB)

	BUFFER = bytearray()
	BUFFER = [x_MSB, x_LSB, y_MSB, y_LSB, z_MSB, z_LSB]
	BUFFER = bytes(BUFFER)
	x = struct.unpack_from('>H', BUFFER[0:2])[0]
	y = struct.unpack_from('>H', BUFFER[2:4])[0]
	z = struct.unpack_from('>H', BUFFER[4:6])[0]
	
	x = _twos_comp(x >> 2, 14)
	y = _twos_comp(y >> 2, 14)
	z = _twos_comp(z >> 2, 14)

	x = x * _ACCEL_MG_LSB_2G * _SENSORS_GRAVITY_STANDARD
	y = y * _ACCEL_MG_LSB_2G * _SENSORS_GRAVITY_STANDARD
	z = z * _ACCEL_MG_LSB_2G * _SENSORS_GRAVITY_STANDARD

	print("ACCEL X: {} | Y: {} | Z: {}".format(x,y,z))

def readMagData2():
	# X,Y,Z axis 16-bit signed raw value
	x_MSB = read(_FXOS8700_REGISTER_MOUT_X_MSB)
	x_LSB = read(_FXOS8700_REGISTER_MOUT_X_LSB)

	y_MSB = read(_FXOS8700_REGISTER_MOUT_Y_MSB)
	y_LSB = read(_FXOS8700_REGISTER_MOUT_Y_LSB)

	z_MSB = read(_FXOS8700_REGISTER_MOUT_Z_MSB)
	z_LSB = read(_FXOS8700_REGISTER_MOUT_Z_LSB)

	BUFFER = bytearray()
	BUFFER = [x_MSB, x_LSB, y_MSB, y_LSB, z_MSB, z_LSB]
	BUFFER = bytes(BUFFER)
	x = struct.unpack_from('>H', BUFFER[0:2])[0]
	y = struct.unpack_from('>H', BUFFER[2:4])[0]
	z = struct.unpack_from('>H', BUFFER[4:6])[0]
	
	x = _twos_comp(x >> 2, 14)
	y = _twos_comp(y >> 2, 14)
	z = _twos_comp(z >> 2, 14)

	x = x * _MAG_UT_LSB
	y = y * _MAG_UT_LSB
	z = z * _MAG_UT_LSB

	print("MAG X: {} | Y: {} | Z: {}".format(x,y,z))

def readMagData():
	# X,Y,Z axis 16-bit signed raw value
	x = read(_FXOS8700_REGISTER_OUT_X_MSB)
	x = _twos_comp(x >> 2, 14)

	y = read(_FXOS8700_REGISTER_OUT_Y_MSB)
	y = _twos_comp(y >> 2, 14)

	z = read(_FXOS8700_REGISTER_OUT_Z_MSB)
	z = _twos_comp(z >> 2, 14)

	print("X: {} | Y: {} | Z: {}".format(x,y,z))

#try:
init()
while True:
	# readAccelData2()
	# readMagData2()
        read_raw()
        time.sleep(1)
#except Exception as e:
#	print("Exception trying to read from i2c: {}".format(str(e)))
