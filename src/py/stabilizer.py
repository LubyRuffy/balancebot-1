"""
Keeps the robot upright at a certain angle
"""
import re
import threading
import time

from py import util

ctrl = util.PIDController(1, 0, 0, lambda: 1, lambda x: print(x))


class InputThread(threading.Thread):

    def run(self):
        while True:
            match = re.search(r'([a-z])(\d*\.?\d*)', input())
            a = match.group(1)
            n = match.group(2)
            if a and n:
                n = float(n)
                if a == 'p':
                    ctrl.p = n
                elif a == 'i':
                    ctrl.i = n
                elif a == 'd':
                    ctrl.d = n
                elif a == 't':
                    ctrl.set_target(n)


class Updater(threading.Thread):

    def __init__(self):
        super(Updater, self).__init__()

    def run(self):
        timer = util.ElapsedTime()

        while True:
            dt = timer.get_time()

            ctrl.update(dt)

            timer.reset()
            time.sleep(0.02)

InputThread().start()
Updater().start()