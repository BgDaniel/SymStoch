from symsprocesses.process_factory import *
from symsprocesses.mathtools.complex_numbers import ComplexNumber
from symsprocesses.process_h_plus import *
from symsprocesses.mathtools.moebius_transfomation import *


simuConfig = SimulationConfig(2.0, 10, 50)

S_0 = 1.0
sigma_0 = 0.1
mu = Mu([lambda x: .0, lambda x: .0])
sigma_S = 0.2
sigma_sigma = 0.05

process = ProcessHPlus(simuConfig, S_0, sigma_0, mu, sigma_S, sigma_sigma)
paths = process.generatePaths()
drift = calculateDrift(paths)

paths_transformed = applyTransformation(paths, reflection(UnitCircle))