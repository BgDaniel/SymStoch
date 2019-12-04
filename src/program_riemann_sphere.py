from symsprocesses.process_factory import *
from symsprocesses.process_riemann_sphere import *
from symsprocesses.mathtools.plot import *





simuConfig = SimulationConfig(50.0, 1, 50000, False)

x0 = .0
y0 = 1.0

def _mu_1(x):
    return .0

def _mu_2(x):
    return .0

mu = Mu([_mu_1, _mu_2])

sigma = 0.3


process = ProcessRiemannSphere(simuConfig, x0, y0, sigma, mu, False)
paths = process.generatePaths()
plot_paths2d(paths, -20.0, 20.0, -20.0, 20.0, process, 10)

