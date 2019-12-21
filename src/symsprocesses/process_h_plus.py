from symsprocesses.process_factory import MultiDimensionItoProcess, Cov
from hypgeo.moebius import *
from hypgeo.geometry import *
from hypgeo.transformations import refl

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

    def reflectAtHalfSpace(self, paths, half_circle):
        assert len(paths) == 2, 'Process is not of dimension 2!'

        nb_simus = self._simuConfig.NumberSimus
        nb_times = self._simuConfig.TimeSteps
        paths_reflected = np.copy(paths)
        reflection = refl(half_circle)
        half_space = HalfSpace(half_circle)

        intial_position = half_space.position(self._S0)
        opposite_position = opposite(intial_position)
    
        for simu in range(0, nb_simus):
            for time in range(0, nb_times):
                if half_space.position(paths[:,simu,time]) == opposite_position:
                    for t in range(time, nb_times):
                        paths_reflected[:,simu,t] = reflection(paths[:,simu,t]).to_vec()
                    continue

        return paths_reflected

    def touch_dist(self, half_circle, paths):
        nb_simus = self._simuConfig.NumberSimus
        nb_times = self._simuConfig.TimeSteps
        has_touched = np.full(nb_simus, False)
        half_space = HalfSpace(half_circle)
        touch_dist = np.full(nb_times, .0)

        for i in range(0, nb_simus):
            for t in range(0, nb_times):                
                if has_touched[i]:
                    touch_dist[t] += 1
                else:                                        
                    if half_space.position(paths[:,i,t]) == Position.IN:
                        has_touched[i] = True
                        touch_dist[t] += 1

        for t in range(0, nb_times):      
            touch_dist[t] = float(touch_dist[t]) / float(nb_simus)

        return touch_dist

    def entered_dist(self, half_circle, paths):
        nb_simus = self._simuConfig.NumberSimus
        nb_times = self._simuConfig.TimeSteps
        half_space = HalfSpace(half_circle)
        entered_dist = np.full(nb_times, .0)

        for i in range(0, nb_simus):
            for t in range(0, nb_times):
                if half_space.position(paths[:,i,t]) == Position.IN:
                    entered_dist[t] += 1

        for t in range(0, nb_times):      
            entered_dist[t] = float(entered_dist[t]) / float(nb_simus)

        return entered_dist
    

  
    


