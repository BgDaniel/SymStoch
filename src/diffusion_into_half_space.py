from symsprocesses.process_factory import *
from symsprocesses.process_h_plus import *
from hypgeo.transformations import refl
from hypgeo.geometry import *
from symsprocesses.generalutils.gnuplot_data import *

'''set up simulation config'''
simuConfig = SimulationConfig(15.0, 10000, 1500, False)

'''define process parameters'''
S_0 = 1.0
sigma_0 = 0.4

def _mu_1(x):
    return .0

def _mu_2(x):
    return .0

mu = Mu([_mu_1, _mu_2])

sigma_S = 0.35
sigma_sigma = 0.35

process = ProcessHPlus(simuConfig, S_0, sigma_0, mu, sigma_S, sigma_sigma)

'''generate paths'''
paths = process.generatePaths()

'''define half circle'''
half_circle = HalfCircle(1.0, 2.5)

'''calculate distributions'''
entered_dist = process.entered_dist(half_circle, paths)
touch_dist = process.touch_dist(half_circle, paths)

arrange_data('in_half_space.data', entered=entered_dist, touched=touch_dist)


