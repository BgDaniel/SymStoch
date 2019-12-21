from symsprocesses.process_factory import *
from symsprocesses.process_h_plus import *
from hypgeo.transformations import refl
from hypgeo.geometry import *
from symsprocesses.generalutils.gnuplot_data import *

class HProcesses:
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
        for S_0 in self._S_0s:
            for sigma_0 in self._sigma_0s:
                process = ProcessHPlus(self._simu_config, S_0, sigma_0, self._mu, self._sigma_S, self._sigma_sigma)

                '''generate paths'''
                paths = process.generatePaths()
                drift = calculateDrift(paths)

                '''reflect paths'''
                paths_reflected = process.reflectAtHalfSpace(paths, self._half_circle)
                drift_reflected = calculateDrift(paths_reflected)

                save_data('plot_data/reflection_S_{0}_{1}.data'.format(str(S_0), str(sigma_0)), drift_S=drift[0], drift_S_reflected=drift_reflected[0])
                save_data('plot_data/reflection_sigma_{0}_{1}.data'.format(str(S_0), str(sigma_0)), drift_sigma=drift[1], drift_sigma_reflected=drift_reflected[1])
                
                half_circle = HalfCircle(1.0, 2.5)

                '''calculate distributions'''
                entered_dist = process.entered_dist(half_circle, paths)
                touch_dist = process.touch_dist(half_circle, paths)

                save_data('plot_data/absorption_{0}_{1}.data'.format(str(S_0), str(sigma_0)), entered=entered_dist, touched=touch_dist)
