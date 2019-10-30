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
        self._progress = int(self._length * float(progress) / float(self._number))
        self._bar = "|{}|".format("#" * self._progress + " " * (self._length - self._progress))

    def updateAndShow(self, progress):
        self.update(progress)
        self.showProgress()

def TrackExecutionTime(function):
    def _function(args):
        start_time = time.time()
        function(args)
        elapsedTime = time.time() - start_time
        sys.stdout.write("Execution of function %s takes %d seconds." % (function.__name__, elapsedTime))

    return _function

class MultiThreadingProcessor:
    def __init__(self, instance, method):
        self._instance = instance
        self._method = method

    def methodToBeExecuted(range):
        return self._method(self._instance, range)

    def runMultiThreads(self):
        nb_cpu = multiprocessing.cpu_count()
        calc_range = range(0, self._instance.NbSimus)
        range_size = len(calc_range)
        chunk_size = int(math.ceil(float(range_size) /float(nb_cpu)))
        chunks = [calc_range[i:i + chunk_size - 1] for i in range(0, range_size, chunk_size)]

        pool = multiprocessing.Pool(processes=nb_cpu)
        result = pool.map(my_function, (chunk for chunk in chunks))

        return result
        



def my_function(range):
    sum = 0
    for i in range:
        sum += i
    return sum
