import math
import numpy as np
import math


def CheckType(operation):
    def _operation(instance, o):
        assert type(o) is ComplexNumber or type(o) is np.float64 or type(o) is float, "%s is not of type \"ComplexNumber\" or \"float\"!" % str(o)
        return operation(instance, o)
    return _operation

def MapFloat(operation):
    def _operation(instance, o):
        if type(o) is float or type(o) is np.float64:
            o = ComplexNumber(float(o), 0)
        return operation(instance, o)
    return _operation

class ComplexNumber:

    @property
    def RealPart(self):
        return self._realPart

    @property
    def ImaginaryPart(self):
        return self._imaginaryPart

    def __init__(self, realPart, imaginaryPart):
        self._realPart = realPart
        self._imaginaryPart = imaginaryPart

    @CheckType
    @MapFloat
    def __add__(self, o):
        ret = ComplexNumber(self._realPart + o.RealPart, self._imaginaryPart + o.ImaginaryPart)
        return ret

    @CheckType
    @MapFloat
    def __sub__(self, o):        
        return ComplexNumber(self._realPart - o.RealPart, self._imaginaryPart - o.ImaginaryPart)

    @CheckType
    @MapFloat
    def __mul__(self, o):
        return ComplexNumber(self._realPart * o.RealPart - self._imaginaryPart * o.ImaginaryPart,
            self._realPart * o.ImaginaryPart + o.RealPart * self._imaginaryPart)

    def __neg__(self):
        return ComplexNumber(- self._realPart, - self._imaginaryPart)  

    @CheckType
    @MapFloat
    def __truediv__(self, o):
        normSquaredInv = 1 / o.normSquared()
        return ComplexNumber(self._realPart * o.RealPart + self._imaginaryPart * o.ImaginaryPart,
            - self._realPart * o.ImaginaryPart + o.RealPart * self._imaginaryPart) * normSquaredInv

    def __str__(self):
        if self._realPart == .0 and self._imaginaryPart == .0:
            return "0.0"
        elif self._realPart == .0:
            return "{} * i".format(str(self._imaginaryPart)) 
        elif self._imaginaryPart == .0:
            return "{}".format(str(self._realPart)) 
        else:
            return "{} + {} * i".format(str(self._realPart), str(self._imaginaryPart))

    def __eq__(self, o):
        if type(o) is not ComplexNumber:
            return False
        elif(self._realPart == o.RealPart and self._imaginaryPart == o.ImaginaryPart):
            return True
        else:
            return False

    def normSquared(self):
        return self._realPart * self._realPart + self._imaginaryPart * self._imaginaryPart

    def norm(self):
        return math.sqrt(self.normSquared())

    def conjugate(self):
        return ComplexNumber(self._realPart, - self._imaginaryPart)

    def inverse(self):
        return self.conjugate() / self.normSquared()

    def toVector(self):
        return np.array([self._realPart, self._imaginaryPart])
    
    def fromVector(vector):
        return ComplexNumber(vector[0], vector[1])

i = ComplexNumber(0, 1)