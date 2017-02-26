import functools
import time


class PIDController:
    """
    A controller for PID
    """

    def __init__(self, p: float, i: float, d: float, feedback: callable, output: callable, deadzone=0):
        """
        :param p: constant
        :param i: constant
        :param d: constant
        :param feedback: float producer
        :param output: float consumer (1 argument)
        """
        self.p = p
        self.i = i
        self.d = d

        self.feedback = feedback
        self.output = output
        self.deadzone = 0

        self.target = 0
        self._sum = 0
        self._last_error = 0

        self.last_output = 0
        self.last_target = 0
        self.last_input = 0

    def update(self, dt):
        self.last_target = self.target
        self.last_input = self.feedback()

        error = self.target - self.feedback()
        delta = (error - self._last_error) / dt
        self._sum += error * dt

        self.last_output = self.p * error + self.i * self._sum + self.d * delta
        if (abs(error) > self.deadzone):
            self.output(self.last_output)
        else:
            self.output(0)

        self._last_error = error

    def set_target(self, target):
        self.target = target


class GyroIntegrator:

    def __init__(self, mpu, axis):
        self.mpu = mpu
        self.axis = axis
        self._angle = 0
        self.offset = 0
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, val):
        self._angle = val
    
    def calibrate(self, iterations=100, between=0.01):
        sum = 0
        for i in range(0, iterations):
            sum += self.raw_data()
            time.sleep(between)
        self.offset = sum / iterations
        print('OFFSET: %s' % (self.offset))
    
    def update(self, dt, mult=1):
        self._angle += dt * mult * (self.raw_data() - self.offset)
        
    def raw_data(self):
        return self.mpu.get_gyro_data()[self.axis]


class Buffer:
    
    def __init__(self, size):
        self.size = size
        self.data = [0 for _ in range(0, size)]
        self._index = 0
    
    def push(self, obj):
        self.data[self._index] = obj
        self._index = (self._index + 1) % self.size
    
    def sum(self):
        return functools.reduce((lambda x, y: x + y), self.data)
    
    def avg(self):
        return self.sum() / len(self.data)


class ElapsedTime:

    def __init__(self):
        self._base = 0
        self.reset()

    def reset(self):
        self._base = time.time()

    def get_time(self):
        return time.time() - self._base


def rangemap(x, a1, b1, a2, b2):
    return (b2 - a2) * (x - a1) / (b1 - a1) + a2
    
def cap(x, a, b):
    return max(min(x, b), a)
