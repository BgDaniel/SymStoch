from process_factory import SimulationConfig, Mu
from mathtools.complex_numbers import ComplexNumber
from process_h_plus import *


simuConfig = SimulationConfig(2.0, 1000, 500)

S_0 = 1.0
sigma_0 = 0.1
mu = Mu([lambda x: .0, lambda x: .0])
sigma_S = 0.2
sigma_sigma = 0.05

process = ProcessHPlus(simuConfig, S_0, sigma_0, mu, sigma_S, sigma_sigma)
paths = process.generatePaths()
