from symsprocesses.process_factory import *
from symsprocesses.mathtools.complex_numbers import ComplexNumber
from symsprocesses.process_h_plus import *
from symsprocesses.mathtools.moebius_transfomation import *


simuConfig = SimulationConfig(2.0, 10, 50, True)

S_0 = 1.0
sigma_0 = 0.1

def _mu_1(x):
    return .0

def _mu_2(x):
    return .0

mu = Mu([_mu_1, _mu_2])

sigma_S = 0.2
sigma_sigma = 0.05

process = ProcessHPlus(simuConfig, S_0, sigma_0, mu, sigma_S, sigma_sigma)


if not(simuConfig.Parallel):
    paths = process.generatePaths()
else:
    paths = process.getZeroPaths()
    nb_cpu = multiprocessing.cpu_count()
    chunks = process.getSimulationChunks(nb_cpu)

    if __name__ == '__main__':
        pool = multiprocessing.Pool(processes=nb_cpu)
        paths_chunks = pool.map(process.generatePathsChunked, (chunk for chunk in chunks))
        paths = process.mergePathsChunks(paths, paths_chunks, chunks)



#drift = calculateDrift(paths)

#paths_transformed = applyTransformation(paths, reflection(UnitCircle))