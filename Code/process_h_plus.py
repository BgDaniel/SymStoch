from process_factory import MultiDimensionItoProcess, Cov
from mathtools.math_utils import Const

class ProcessHPlus(MultiDimensionItoProcess):
    def __init__(self, simuConfig, S_0, sigma_0, mu, sigma_S, sigma_sigma, parallel=True):
        
        cov = Cov([[lambda s, sigma: sigma_S / sigma, lambda s, sigma: .0], [lambda s, sigma: .0, lambda s, sigma: sigma_S / sigma]])        
        MultiDimensionItoProcess.__init__(self, simuConfig, mu, cov, [S_0, sigma_0], parallel)

  
    


