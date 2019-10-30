import numpy as np
import math
import matplotlib.pyplot as plt
import time
import sys
from Utils.Utils import ProgressBar, TrackExecutionTime, MultiThreadingProcessor
import multiprocessing


class SimulationConfig:

    @property
    def T(self):
        return self._T

    @property
    def NumberSimus(self):
        return self._numberSimus

    @property
    def TimeSteps(self):
        return self._timeSteps

    @property
    def Dt(self):
        return self._T / self._timeSteps

    def __init__(self, T, numberSimus, timeSteps):
        self._T = T
        self._numberSimus = numberSimus
        self._timeSteps = timeSteps
        self._dt = .0

class Mu:

    @property
    def Entries(self):
        return self._entries

    def __init__(self, entries):
        self._entries = entries

    def __call__(self, s, dW):                
        assert len(self._entries) == len(s), 'x is of wrong length!'
        l = len(s)
        ret = np.zeros(l)

        for i in range(0, l):
            ret[i] = self._entries[i](s) * dW[i]

        return ret

class Cov:

    def __init__(self, cov):
        self._cov = cov

    def __call__(self, s, dW):            
        assert len(self._cov) == len(s), 'x is of wrong length!'
        l = len(s)
        ret = np.zeros(l)

        for i in range(0, l):
            v = 0
            for j in range(0, l):
                v += self._cov[i][j](s) * dW[j]
            ret[i] = v

        return ret

class Const:
    def  __init__(self, value):
        self._value = value

    def __call__(self, x):
        return self._value

class Identity:
    def __call__(self, x):
        return x

class Transformation:
    def __init__(self, transformation):      
        self._transformation = transformation        

    
    def __call__(self, value):
        l = len(value)
        ret = np.zeros(l)

        for i in range(0, l):
            ret[i] = self._transformation[i](value)

def my_function(range):
    sum = 0
    for i in range:
        sum += i
    return sum


class MultiDimensionItoProcess:

    @property
    def NbSimus(self):
        return self._nbSimus

    def __init__(self, simuConfig, mu, cov, S0, parallel=True):
        self._simuConfig = simuConfig      
        self._mu = mu
        self._cov = cov
        self._dim = len(mu.Entries)        
        self._dW_t = np.zeros((self._dim, self._simuConfig.NumberSimus, self._simuConfig.TimeSteps))
        self._S0 = S0
        self._nbSimus = self._simuConfig.NumberSimus
        self._nbSteps = self._simuConfig.TimeSteps
        self._parallel = parallel
        self.initialize()
    
    @TrackExecutionTime
    def generatePaths(self):
        if self._parallel:
            if __name__ == "__main__":
                paths = np.zeros((self._dim, self._simuConfig.NumberSimus, self._simuConfig.TimeSteps))
                nb_cpu = multiprocessing.cpu_count()
                calc_range = range(0, self._simuConfig.NumberSimus)
                range_size = len(calc_range)
                chunk_size = int(math.ceil(float(range_size) /float(nb_cpu)))
                chunks = [calc_range[i:i + chunk_size - 1] for i in range(0, range_size, chunk_size)]

                pool = multiprocessing.Pool(processes=nb_cpu)
                paths_chunks = pool.map(self._generatePaths, (chunk for chunk in chunks))
                
                for i, paths_chunk in enumerate(paths_chunks):
                    simus = chunks[i]
                    for j, k in enumerate(simus):
                        paths[:,k,:] = paths_chunk[:,j,:]
                
                return paths
        else:
            progressBar = ProgressBar(50, "Generating paths ...", self._nbSimus)
            return self._generatePaths(range(0, self._nbSimus))

    def _generatePaths(self, range_simus):
        ell = len(range_simus)
        paths = np.zeros((self._dim, ell, self._simuConfig.TimeSteps))

        for simu in range(0, ell):
            paths[:,simu,0] = self._S0

        for simu in range(0, ell):
            for time in range(1, self._nbSteps):
                paths[:,simu,time] = paths[:,simu,time-1] + self._cov(paths[:,simu,time-1], self._dW_t[:,range_simus[simu],time]) 
                paths[:,simu,time] = paths[:,simu,time] + self._mu(paths[:,simu,time-1], self._dW_t[:,range_simus[simu],time])

        return paths

    def initialize(self):
        dt = self._simuConfig.Dt
        dt_sqrt = math.sqrt(dt)
       
        self._dW_t = np.random.normal(size =(self._dim, self._nbSimus, self._nbSteps)) * dt_sqrt

    def calculateDrift(self, paths):
        drift = np.zeros((self._dim, self._nbSteps))

        for dim in range(0, self._dim):
            for time in range(0, self._nbSteps):
                drift[dim,time] = np.mean(self._paths[dim,:,time])

        return drift

    def applyTransformation(self, transformation):
        transformedProcess = MultiDimensionItoProcess(self._simuConfig, self._mu, self._cov, self._S0)
        transformedS0 = transformation(self._S0)
        transformedS = np.zeros((self._dim, self._simuConfig.NumberSimus, self._simuConfig.TimeSteps))

        for simu in range(0, self._nbSimus):
            for time in range(0, self._nbSteps):
                transformedS[:,simu,time] = transformation(self._S[:,simu,time])

        return None

      

mu = Mu([Const(0.01), Const(0.03)])
cov = Cov([[Const(.1), Const(.0)], [Const(.0), Const(.35)]])
S_0 = [.3, .7]

simuConfig = SimulationConfig(1.0, 500, 500)
process = MultiDimensionItoProcess(simuConfig, mu, cov, S_0)
paths = process.generatePaths()
#drift = process.calculateDrift()
transformation =  Transformation([Identity(), Identity()])

#transformedProcess = process.applyTransformation(transformation)





     




  













