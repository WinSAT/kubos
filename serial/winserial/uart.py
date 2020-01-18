import serial
import app_api
import time

class UART:
    def __init__(self, port_name, timeout_value):
        self.port = port_name
        self.serial = serial.Serial(
            port=str(port_name),
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout_value)

        self.logger = app_api.logging_setup("uart")

    # send message to hardware over uart
    def send(self, message):
        try:
            # open uart port
            self.serial.close()
            self.serial.open()

            if self.serial.isOpen():
                # if uart port is open, try to send encoded string message
                self.serial.write(str(message).encode('utf-8'))
                self.serial.close()
                self.logger.debug("UART port {} is open. Sent message: {}".format(self.port, str(message)))
                return True
            else:
                # if could not open uart port, return failure
                self.serial.close()
                self.logger.warn("Could not open serial port: {}".format(self.port))
                return False

        # return failure if exception during write/encoding
        except Exception as e:
            self.logger.warn("Error sending message {} over uart port {}: {}".format(str(message), self.port, str(e)))
            return False

    # get message from hardware over uart
    def get(self):
        try:
            self.serial.close()
            self.serial.open()

            if self.serial.isOpen():
                # if uart port is open, try to read something
                message = self.serial.readline()
                message = message.decode('utf-8')
                self.logger.debug("Uart port {} is open. Read line: {}".format(message))
                self.serial.close()
                return True
            else:
                # if could not open uart port, return failure
                self.serial.close()
                self.logger.warn("Could not open serial port: {}".format(self.port))
                return False

        # return failure if exception during read/decoding
        except Exception as e:
            self.logger.warn("Error sending message over uart port {}: {}".format(self.port, str(e)))
            return False

    # send message to hardware over uart and expect a message back
    def send_wait(self, message):
        try:
            # open uart port
            self.serial.close()
            self.serial.open()

            if self.serial.isOpen():
                # if uart port is open, try to send encoded string message
                self.serial.write(str(message).encode('utf-8'))
                self.logger.debug("UART port {} is open. Sent message: {}".format(self.port, str(message)))

                # add some time to wait (may need to be adjusted)
                time.sleep(1)

                response = self.serial.readline()
                self.logger.debug("Got message back: {}".format(str(response)))
                response = (response.decode('utf-8'))
                self.logger.debug("Decoded message: {}".format(response))
                self.logger.debug("Uart port {} is closed. Read line: {}".format(self.port, response))
                self.serial.close()
                return response
            else:
                # if could not open uart port, return failure
                self.serial.close()
                self.logger.warn("Could not open serial port: {}".format(self.port))
                return "error"

        # return failure if exception during write/encoding
        except Exception as e:
            self.logger.warn("Error sending message over uart port {}: {}".format(self.port, str(e)))
            return "error"