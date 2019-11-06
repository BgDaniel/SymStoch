from symsprocesses.process_factory import MultiDimensionItoProcess, Cov
from symsprocesses.mathtools.math_utils import Const

class ProcessHPlus(MultiDimensionItoProcess):
    def _cov_11(self, x):
        assert len(x) == 2, "Wrong input dimension!"
        return self._sigma_S * x[1]
                    
    def _cov_22(self, x):
        assert len(x) == 2, "Wrong input dimension!"
        return self._sigma_sigma * x[1]

    def _cov_12(self, x):
        assert len(x) == 2, "Wrong input dimension!"
        return .0

    def _cov_21(self, x):
        return self._cov_12(x)

    def __init__(self, simuConfig, S_0, sigma_0, mu, sigma_S, sigma_sigma, parallel=True):
        self._sigma_S = sigma_S
        self._sigma_sigma = sigma_sigma

        cov = Cov([[self._cov_11, self._cov_12], [self._cov_21, self._cov_22]])        
        MultiDimensionItoProcess.__init__(self, simuConfig, mu, cov, [S_0, sigma_0], parallel)

  
    


