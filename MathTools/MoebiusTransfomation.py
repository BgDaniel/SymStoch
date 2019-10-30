from ComplexNumbers import ComplexNumber, i
import math
import matplotlib.pyplot as plt
import numpy as np

class Moeb:

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c

    @property
    def d(self):
        return self._d

    def __init__(self, a, b, c, d):
        self._a = a
        self._b = b
        self._c = c
        self._d = d

    def __call__(self, z):
        return (z * self._a + self._b) / (z * self._c + self._d)

    def __mul__(self, o):
        assert type(o) is Moeb, "%s is not of type \"Moeb\"!" % str(o)

        return Moeb(self._a * o.a + self._b * o.c, self._a * o.b + self._b * o.d, 
            self._c * o.a + self._d * o.c, self._c * o.b + self._d * o.d)

    def conjugate(self, o):
        assert type(o) is Moeb, "%s is not of type \"Moeb\"!" % str(o)

        return (o.inverse()) * self * o

    def inverse(self):
        return Moeb(self._d, - self._b, - self._c, self._a)

class MoebConj(Moeb):
    def __init__(self, a, b, c, d):
        Moeb.__init__(self, a, b, c, d)

    def __call__(self, z):
        return Moeb.__call__(self, z.conjugate())



def MoebFromTo(z_0, z_1):
    Re_z_0 = z_0.RealPart
    Im_z_0 = z_0.ImaginaryPart
    Re_z_1 = z_1.RealPart
    Im_z_1 = z_1.ImaginaryPart

    a = math.sqrt(Im_z_1 / Im_z_0)
    b = - Re_z_0 * math.sqrt(Im_z_1 / Im_z_0) + Re_z_1 * math.sqrt(Im_z_0 / Im_z_1)
    c = .0
    d = math.sqrt(Im_z_0 / Im_z_1)

    return Moeb(a, b, c, d)

#rotation around i 
def Elliptic0(t):
    return Moeb(math.cos(t), math.sin(t), - math.sin(t), math.cos(t))

#rotation around u
def Elliptic(t, u):
    return Elliptic0(t).conjugate(MoebFromTo(u, i))
      
#scaling with positive real
def Loxodromic0(t):
    return Moeb(math.exp(.5 * t), .0, .0, math.exp(- .5 * t))

#translation in x-direction
def Parabolic0(t):
    return Moeb(1.0, t, .0, 1.0) 

#reflection at half circle around (0,0) of radius r
def Reflection0(R):
    iR = ComplexNumber(.0, R)
    return MoebConj(.0, iR, 1 / iR, .0)  

#reflection at half circle around (u,0) of radius r
def RelfectionCirc(u, R):
    return MoebConj(u / (R * R), R * R - u * u / (R * R), 1 / (R * R), - u / (R * R))  

#reflection at line x=u
def RelfectionLine(x):
    return MoebConj()

refl = Reflection0(1.0)
z = ComplexNumber(.0, 1.0)

print(refl(z))
