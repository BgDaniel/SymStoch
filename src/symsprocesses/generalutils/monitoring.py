import sys
import time
import multiprocessing
import math

class ProgressBar:

    def __init__(self, length, message, number):
        self._length = length
        self._number = number
        self._message = message
        self._bar = "|{}|".format(" " * self._length)

    def showProgress(self):
        sys.stdout.write(self._message + "    " + self._bar + "\r")

    def update(self, progress):
        percent_done = int(100.00 * float(progress) / float(self._number))
        self._progress = int(self._length * float(progress) / float(self._number))
        self._bar = "|{}| {}%, {} of {} paths".format("#" * self._progress + " " * (self._length - self._progress),
            percent_done, progress, self._number)

    def updateAndShow(self, progress):
        self.update(progress)
        self.showProgress()

def TrackExecutionTime(function):
    def _function(args):
        start_time = time.time()
        return function(args)
        elapsedTime = time.time() - start_time
        sys.stdout.write("Execution of function %s takes %d seconds." % (function.__name__, elapsedTime))

    return _function
        

