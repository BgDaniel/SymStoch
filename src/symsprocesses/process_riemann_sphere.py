from symsprocesses.process_factory import MultiDimensionItoProcess, Cov
from hypgeo.moebius import *
from hypgeo.geometry import *

class ProcessRiemannSphere(MultiDimensionItoProcess):
    def _cov_11(self, x):
        assert len(x) == 2, "Wrong input dimension!"
        return self._sigma * (1.0 + x[0] * x[0] + x[1] * x[1])
                    
    def _cov_22(self, x):
        assert len(x) == 2, "Wrong input dimension!"
        return self._sigma * (1.0 + x[0] * x[0] + x[1] * x[1])

    def _cov_12(self, x):
        assert len(x) == 2, "Wrong input dimension!"
        return .0

    def _cov_21(self, x):
        return .0

    def __init__(self, simuConfig, x0, y0, sigma, mu, parallel=True):
        self._sigma = sigma

        cov = Cov([[self._cov_11, self._cov_12], [self._cov_21, self._cov_22]])        
        MultiDimensionItoProcess.__init__(self, simuConfig, mu, cov, [x0, y0], parallel)