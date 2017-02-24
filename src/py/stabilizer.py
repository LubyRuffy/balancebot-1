"""
Keeps the robot upright at a certain angle
"""
from curses import wrapper
import re
import threading
import time

import util


class InputThread(threading.Thread):

    def __init__(self, ctrl):
        self.ctrl = ctrl

    def run(self):
        while True:
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


def main(stdscr):
    ctrl = util.PIDController(1, 0, 0, lambda: 1, lambda x: print(x))

    InputThread(ctrl).start()

    timer = util.ElapsedTime()

    while True:
        stdscr.clear()

        dt = timer.get_time()

        ctrl.update(dt)

        timer.reset()
        time.sleep(0.02)

        stdscr.refresh()


if __name__ == '__main__':
    wrapper(main)