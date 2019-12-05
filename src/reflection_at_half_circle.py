from symsprocesses.process_factory import *
from symsprocesses.process_h_plus import *
from hypgeo.transformations import refl
from hypgeo.geometry import *


class ReflectAtHalfspace:
    def __init__(self, simu_config, S_0s, sigma_0s, sigma_S, sigma_sigma, half_circle):
        self._simu_config = simu_config
        self._S_0s = S_0s
        self._sigma_0s = sigma_0s
        self._sigma_S = sigma_S
        self._sigma_sigma = sigma_sigma
        self._half_circle = half_circle

        def _mu_1(x):
            return .0

        def _mu_2(x):
            return .0

        self._mu = Mu([_mu_1, _mu_2])

    def execute(self):        
        for S_0 in S_0s:
            for sigma_0 in sigma_0s:
                process = ProcessHPlus(self._simu_config, S_0, sigma_0, self._mu, self._sigma_S, self._sigma_sigma)

                '''generate paths'''
                paths = process.generatePaths()
                drift = calculateDrift(paths)

                '''reflect paths'''
                reflected_paths = process.reflectAtHalfSpace(paths, self._half_circle)
                drift_reflected = calculateDrift(reflected_paths)

                np.savetxt('drift_{}_{}.csv'.format(str(S_0), str(sigma_0)), drift, fmt='%.4f', delimiter=';')
                np.savetxt('drift_reflected_{}_{}.csv'.format(str(S_0), str(sigma_0)), drift_reflected, fmt='%.4f', delimiter=';')



simuConfig = SimulationConfig(25.0, 10000, 5000, False)
half_circle = HalfCircle(1.0, 0.0)

S_0s = [0.0, 0.5, 1.0, 1.5, 2.0]
sigma_0s = [0.5, 1.0, 1.5, 2.0]

sigma_S = 0.35
sigma_sigma = 0.3

reflect = ReflectAtHalfspace(simuConfig, S_0s, sigma_0s, sigma_S, sigma_sigma, half_circle)
reflect.execute()




