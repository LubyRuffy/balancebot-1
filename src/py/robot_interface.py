import smbus
from mpu6050 import mpu6050

import util


class Motor:

    def set_power(self, power: float):
        pass


class CRServoI2C(Motor):

    def __init__(self, i2c, addr, first_byte, min_power=0, neutral=90, max_power=180, suppress_errors=False):
        self.i2c = i2c
        self.addr = addr
        self.first_byte = first_byte
        self.min_power = min_power
        self.max_power = max_power
        self.neutral = neutral
        self.suppress_errors = suppress_errors

    def set_power(self, power: float):
        try:
            if power < 0:
                output = int(util.rangemap(power, -1, 0, self.min_power, self.neutral))
            else:
                output = int(util.rangemap(power, 0, 1, self.neutral, self.max_power))
            self.i2c.write_byte_data(0x73, self.first_byte, util.cap(output, self.min_power, self.max_power))
        except OSError:
            if not self.suppress_errors:
                raise
