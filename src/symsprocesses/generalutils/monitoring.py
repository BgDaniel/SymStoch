import sys
import time
import multiprocessing
import math
import time
import numpy as np
from datetime import timedelta

class ProgressBar:
    def __init__(self, length, message, number):
        self._length = length
        self._number = number
        self._message = message
        self._bar = "|{}|".format(" " * self._length)
        self._time_for_steps = []
        self._last_stopped_time = None

    def showProgress(self):
        sys.stdout.write(self._message + "    " + self._bar + "\r")

    def update(self, progress):
        percent_done = int(100.00 * float(progress) / float(self._number))
        self._progress = int(self._length * float(progress) / float(self._number))

        remaining_time = ''
        if self._last_stopped_time != None:
            remaining_time = self.estimateRemainingTime(progress)
        self._last_stopped_time = time.time()

        self._bar = "|{}| {}%, {} of {} paths, {}".format("#" * self._progress + " " * (self._length - self._progress),
            percent_done, progress, self._number, remaining_time)

    def updateAndShow(self, progress):
        self.update(progress)
        self.showProgress()

    def estimateRemainingTime(self, progress):
        elapsed_time = time.time() - self._last_stopped_time
        self._time_for_steps.append(elapsed_time)
        mean_time_for_step = np.mean(np.array(self._time_for_steps))
        estimated_time =(self._number - progress ) * mean_time_for_step

        hours = int(estimated_time // 3600)
        minutes = int((estimated_time % 3600) // 60)
        seconds = int(estimated_time % 60)

        ret = ''
        if hours != 0:
            ret += str(hours) + 'h '
        if minutes != 0:
            ret += str(minutes) + 'min '
        if seconds != 0:
            ret += str(seconds) + 'sec '
        return 'remaining time: {}'.format(ret)

def TrackExecutionTime(function):
    def _function(args):
        start_time = time.time()
        return function(args)
        elapsedTime = time.time() - start_time
        sys.stdout.write("Execution of function %s takes %d seconds." % (function.__name__, elapsedTime))

    return _function
        

