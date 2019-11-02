from symsprocesses.process_factory import MultiDimensionItoProcess, Cov
from symsprocesses.mathtools.math_utils import Const

class ProcessHPlus(MultiDimensionItoProcess):
    def __init__(self, simuConfig, S_0, sigma_0, mu, sigma_S, sigma_sigma, parallel=True):
        
        def _cov_ii(x):
            assert len(x) == 2, "Wrong input dimension!"
            return sigma_S * x[1]
                    
        def _cov_ij(x):
            assert len(x) == 2, "Wrong input dimension!"
            return .0

        cov = Cov([[_cov_ii, _cov_ij], [_cov_ij, _cov_ii]])        
        MultiDimensionItoProcess.__init__(self, simuConfig, mu, cov, [S_0, sigma_0], parallel)

  
    


