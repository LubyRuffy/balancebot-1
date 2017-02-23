import time


class PIDController:
    """
    A controller for PID
    """

    def __init__(self, p: float, i: float, d: float, feedback: callable, output: callable):
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
        self.output(self.last_output)

        self._last_error = error

    def set_target(self, target):
        self.target = target


class ElapsedTime:

    def __init__(self):
        self._base = 0
        self.reset()

    def reset(self):
        self._base = time.clock()

    def get_time(self):
        return time.clock() - self._base