from symsprocesses.process_factory import MultiDimensionItoProcess, Cov
from symsprocesses.mathtools.math_utils import Const
from symsprocesses.mathtools.moebius_transfomation import *

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

    def reflectAtHalfSpace(self, paths, halfSpace):
        assert len(paths) == 2, 'Process is not of dimension 2!'

        nb_simus = len(paths[0])
        nb_steps = len(paths[0][0])
        paths_reflected = np.copy(paths)

        intial_position = halfSpace.position(self._S0)
        opposite_position = opposite(intial_position)
    
        for simu in range(0, nb_simus):
            for time in range(0, nb_steps):
                if halfSpace.position(paths[:,simu,time]) == opposite_position:
                    paths_reflected[:,simu,time] = halfSpace.reflect(paths[:,simu,time]).toVector()

        return paths_reflected
    

  
    


