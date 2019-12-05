from symsprocesses.process_factory import *
from symsprocesses.process_h_plus import *
from hypgeo.transformations import refl
from hypgeo.geometry import *

'''set up simulation config'''
simuConfig = SimulationConfig(25.0, 100, 50, False)

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

'''calculate distribution'''
dist_is_in, dist_has_entered = process.calc_absorption(half_circle, paths)


np.savetxt('in_half_space.csv'.format(), dist_is_in, fmt='%.4f', delimiter=';')
np.savetxt('touching_half_circle.csv'.format(), dist_has_entered, fmt='%.4f', delimiter=';')
