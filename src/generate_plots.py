from symsprocesses.process_factory import *
from symsprocesses.process_h_plus import *
from hypgeo.transformations import refl
from hypgeo.geometry import *
from h_processes import *

'''set up simulation config'''
simuConfig = SimulationConfig(15.0, 15000, 5000, False)
half_circle = HalfCircle(1.0, 0.0)

S_0s = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
sigma_0s = [0.5, 1.0, 1.5, 2.0, 2.5]

sigma_S = 0.35
sigma_sigma = 0.35

reflect = HProcesses(simuConfig, S_0s, sigma_0s, sigma_S, sigma_sigma, half_circle)
reflect.execute()