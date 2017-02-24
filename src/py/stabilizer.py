"""
Keeps the robot upright at a certain angle
"""
import math
import re
import threading
import time

from smbus import SMBus
from mpu6050 import mpu6050

import robot_interface as robot
import util


class InputThread(threading.Thread):

    def __init__(self, ctrl, gyro):
        super().__init__()
        self.ctrl = ctrl
        self.gyro = gyro

    def run(self):
        while True:
            try:	
            	match = re.search(r'([a-z])(-?\d*\.?\d*)', input())
            	a = match.group(1)
            	n = match.group(2)
            	if a and n:
                    n = float(n)
                    if a == 'p':
                        self.ctrl.p = n
                    elif a == 'i':
                        self.ctrl.i = n
                    elif a == 'd':
                        self.ctrl.d = n
                    elif a == 't':
                        self.ctrl.set_target(n)
                    elif a == 'c':
                        self.gyro.calibrate()
                        self.gyro.angle = rotation(self.gyro.mpu.get_accel_data())
                    print('set %s to %s' % (a, n))
            except AttributeError:
                pass

def output_to_motors(power, left, right):
    left.set_power(power)
    right.set_power(-power)

def rotation(data):
    return math.degrees(math.atan2(data['z'], data['x']))

def main():
    i2c_bus = SMBus(1)
    mpu = mpu6050(0x68)
    mpu.set_gyro_range(mpu6050.GYRO_RANGE_1000DEG)

    left_motor = robot.CRServoI2C(i2c_bus, 0x73, ord('l'), neutral=85, suppress_errors=True)
    right_motor = robot.CRServoI2C(i2c_bus, 0x73, ord('r'), neutral=90, suppress_errors=True)
    left_motor.set_power(1)
    output = 0
    
    gyro = util.GyroIntegrator(mpu, 'y')
    feedback = lambda: math.cos(rotation(mpu.get_accel_data()))
     
    ctrl = util.PIDController(0, 0, 0, feedback, lambda x: output_to_motors(x, left_motor, right_motor), deadzone=3)

    InputThread(ctrl, gyro).start()

    timer = util.ElapsedTime()

    while True:
        #stdscr.clear()

        dt = timer.get_time()

        ctrl.update(dt)
        gyro.update(dt)
        print(dt, feedback())
        
        #stdscr.refresh()
        timer.reset()
        time.sleep(0.05)


if __name__ == '__main__':
    #wrapper(main)
    main()
