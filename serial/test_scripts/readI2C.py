#!/usr/bin/env python3

import serial
import time
import argparse
from i2c import I2C
import struct
import smbus

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
# get address name from arguments
parser = argparse.ArgumentParser()
#parser.add_argument('address', type=str, help='address number to read from')
#parser.add_argument('num_read', type=int, help='number of bytes to read')
args = parser.parse_args()

# i2c setup
bus = smbus.SMBus(2)
i2c_device = I2C(bus = 2)
slave_address = 0x1F
BUFFER = bytearray(13)

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

def readHandler3():
	data = _read_u8(_FXOS8700_REGISTER_WHO_AM_I)
	if data == _FXOS8700_ID:
		print("Failed to find device. Found ID: {},{}".format(data, _FXOS8700_ID))
	else:
		print("Found device with ID: {},{}".format(data, _FXOS8700_ID))

def readHandler2():

	bus.write_byte_data(slave_address, _FXOS8700_REGISTER_MCTRL_REG1, 0x1F)

	bus.write_byte(slave_address, _FXOS8700_REGISTER_MCTRL_REG1)
	val = bus.read_byte_data(slave_address, _FXOS8700_REGISTER_MCTRL_REG1)
	#val = bus.read_i2c_block_data(slave_address, register_address, 1)
	#for i in val:
	print("Got data: {}".format(val))

def readHandler():
	#print("Getting value over i2c from address: {}".format(str(slave_address)))
	#BUFFER = [0x00] * 13
	#print("BUFFER: {}".format(BUFFER))
	#BUFFER[0] = 0x0D 
	#print("BUFFER: {}".format(BUFFER))

	#data = i2c_device.read(device = slave_address, count = 13)
	#print("data: {}".format(data))

	success,written_command = i2c_device.write(device = slave_address, data = bytes(0x0D))
	if (success):
		data = i2c_device.read(device = slave_address, count = 2)
	else:
		print("Unsuccesful write {}:{}".format(str(slave_address), str(register_address)))

	print("data: {}".format(data))

def read(register_address):
	return bus.read_byte_data(slave_address, register_address)

def read_word(register_address):
	return bus.read_word_data(slave_address, register_address)

def write(register_address, data):
	return bus.write_byte_data(slave_address, register_address, data)

def init():
	if read(_FXOS8700_REGISTER_WHO_AM_I) != _FXOS8700_ID:
		print('Failed to find FXOS8700, check wiring!')
	# Set to standby mode (required to make changes to this register)
	write(_FXOS8700_REGISTER_CTRL_REG1, 0)
	# set accel range to 2G
	write(_FXOS8700_REGISTER_XYZ_DATA_CFG, 0x00)
	# High resolution
	write(_FXOS8700_REGISTER_CTRL_REG2, 0x02)
	# Active, Normal Mode, Low Noise, 100Hz in Hybrid Mode
	write(_FXOS8700_REGISTER_CTRL_REG1, 0x15)
	# Configure the magnetometer
	# Hybrid Mode, Over Sampling Rate = 16
	write(_FXOS8700_REGISTER_MCTRL_REG1, 0x1F)
	# Jump to reg 0x33 after reading 0x06
	write(_FXOS8700_REGISTER_MCTRL_REG2, 0x20)

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
	#readAccelData2()
	readMagData2()
	time.sleep(1)
#except Exception as e:
#	print("Exception trying to read from i2c: {}".format(str(e)))