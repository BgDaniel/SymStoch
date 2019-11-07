import sys
from symsprocesses.mathtools.complex_numbers import ComplexNumber, i
import math
import numpy as np
import enum

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
        if type(a) is float:
            a = ComplexNumber(a, .0)
        if type(b) is float:
            b = ComplexNumber(b, .0)
        if type(c) is float:
            c = ComplexNumber(c, .0)
        if type(d) is float:
            d = ComplexNumber(d, .0)
        self._a = a
        self._b = b
        self._c = c
        self._d = d

    def __call__(self, z):
        if type(z) is np.array or type(z) is np.ndarray:
            assert len(z) == 2, "z has wrong dimension!"
            z = ComplexNumber(z[0], z[1])
        elif type(z) is not ComplexNumber:
            raise Exception("Argument z is neither of type array nor type ComplexNumber!") 

        return (z * self._a + self._b) / (z * self._c + self._d)

    def __mul__(self, o):
        assert type(o) is Moeb or type(o) is MoebConj, "%s is not of type \"Moeb\"!" % str(o)

        return Moeb(self._a * o.a + self._b * o.c, self._a * o.b + self._b * o.d, 
            self._c * o.a + self._d * o.c, self._c * o.b + self._d * o.d)

    def conjugate(self, o):
        assert type(o) is Moeb, "%s is not of type \"Moeb\"!" % str(o)

        return (o.inverse()) * self * o

    def inverse(self):
        return Moeb(self._d, - self._b, - self._c, self._a)

    def plot(self, rectanlge):
        return None

class MoebConj(Moeb):
    def __init__(self, a, b, c, d):
        Moeb.__init__(self, a, b, c, d)

    def __call__(self, z):
        if type(z) is np.array or type(z) is np.ndarray or type(z) is list:
            assert len(z) == 2, "z has wrong dimension!"
            z = ComplexNumber(z[0], z[1])
        elif type(z) is not ComplexNumber:
            raise Exception("Argument z is neither of type array nor type ComplexNumber!") 
        return Moeb.__call__(self, z.conjugate())

class MoebCorr(Moeb):
    def __init__(self, a, b, c, d, rho):
        self._rho = rho
        Moeb.__init__(self, a, b, c, d)

    def __call__(self, z):
        z_x = z.RealPart
        z_y = z.ImaginaryPart
        u = z_x / self._rho + math.sqrt(1.0 - self._rho * self._rho) / self._rho * z_y
        v = z_y
        z = ComplexNumber(u, v)
        w = Moeb.__call__(self, z)
        w_x = w.RealPart
        w_y = w.ImaginaryPart
        u = self._rho * w_x + math.sqrt(1.0 - self._rho * self._rho) * w_y
        v = w_y
        return ComplexNumber(u, v)

class LineType(enum.Enum):
    CIRCLE = 1
    VERTICAL = 2

class Position(enum.Enum):
    IN = 1
    OUT = 2
    ON = 3

def opposite(position):
    if position == Position.IN:
        return Position.OUT
    elif position == Position.OUT:
        return Position.IN
    else:
        return Position.ON

class HalfSpace:
    def __init__(self, line):
        self._line = line
        self._reflection = reflection(line)

    def position(self, x):
        if type(x) is np.array or type(x) is np.ndarray or type(x) is list:
            assert len(x) == 2, "z has wrong dimension!"
        elif type(x) is ComplexNumber:
            x = x.ToVector()
        else:
            raise Exception("Argument z is neither of type array nor type ComplexNumber!") 

        level = self._line.LevelFunction(x[0], x[1])

        if level < .0:
            return Position.IN
        elif level == .0:
            return Position.ON
        else:
            return Position.OUT

    def reflect(self, x):
        return self._reflection(x) 


class Line:
    @property
    def Radius(self):       
        return self._radius

    @property
    def Center(self):
        return self._center

    @property
    def IntersectionXaxis(self):
        return self._intersectionXaxis

    @property
    def Type(self):
        return self._type

    @property
    def z0(self):
        return self._z0

    @property
    def z1(self):
        return self._z1

    @property
    def LevelFunction(self):
        return self._levelFunction

    def __init__(self, z0, z1):
        assert type(z0) is ComplexNumber, "z0 is not of type \"ComplexNumber\"!"
        assert type(z1) is ComplexNumber, "z1 is not of type \"ComplexNumber\"!"
        assert z0 != z1, "A line in HPlus can only be determined by two different complex numbers!"
        assert z0.ImaginaryPart > 0, "z0 is not contained in HPlus!"
        assert z1.ImaginaryPart > 0, "z1 is not contained in HPlus!"

        self._z0 = z0
        self._z1 = z1

        if self._z0.RealPart == self._z1.RealPart:
            self._type = LineType.VERTICAL
            self._intersectionXaxis = self._z0.RealPart
            self._center = None
            self._radius = float('inf')
            self._levelFunction = lambda x, y: y - self._intersectionXaxis

        else:
            self._type = LineType.CIRCLE
            self._intersectionXaxis = - float('inf')
            x0 = self._z0.RealPart
            y0 = self._z0.ImaginaryPart
            x1 = self._z1.RealPart
            y1 = self._z1.ImaginaryPart
            self._center = 1.0 / 2.0 * (y1 ** 2 - y0 ** 2 - x0 ** 2 + x1 ** 2) / (x1 - x0)
            self._radius = 1.0 / ( 2.0 * (abs(x1 - x0))) * math.sqrt(((x1 - x0) ** 2 + (y1 - y0) ** 2) * ((x1 - x0) ** 2 + (y1 + y0) ** 2))
            self._levelFunction = lambda x, y: (x - self._center) * (x - self._center) + y * y - self._radius * self._radius

    def getTrace(self, step_width, y_max):
        trace = []
        if self._type == LineType.VERTICAL:
            i = 0
            while i * step_width <= y_max:
                trace.append([self._intersectionXaxis, i * step_width])
                i += 1
        else:
            angles = np.arange(.0, math.pi * self._radius + step_width, step_width)
            for phi in angles:
                trace.append([math.sin(phi) * self._radius, math.cos(phi) * self._radius])

        return trace



UnitCircle = Line(ComplexNumber(- 1.0 / (math.sqrt(2.0)), 1.0 / (math.sqrt(2.0))), ComplexNumber(+ 1.0 / (math.sqrt(2.0)), 1.0 / (math.sqrt(2.0)))) 

def moebFromTo(z_0, z_1):
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
def elliptic0(t):
    return Moeb(math.cos(t), math.sin(t), - math.sin(t), math.cos(t))

#rotation around u
def elliptic(t, u):
    return elliptic0(t).conjugate(moebFromTo(u, i))
      
#scaling with positive real
def loxodromic0(t):
    return Moeb(math.exp(.5 * t), .0, .0, math.exp(- .5 * t))

#translation in x-direction
def parabolic0(t):
    return Moeb(1.0, t, .0, 1.0) 

#reflection at half circle around (0,0) of radius r
def reflection0(R):
    iR = ComplexNumber(.0, R)
    idivR = ComplexNumber(.0, 1.0 / R)
    return MoebConj(.0, iR, idivR, .0)  

#reflection at half circle around (u,0) of radius r
def relfectionCirc(u, R):
    return MoebConj(u / (R * R), R * R - u * u / (R * R), 1 / (R * R), - u / (R * R))  

#reflection at line x=u
def relfectionLine(x):
    return MoebConj()

#map line to line (transitivity of Moeb on Lines(HPlus))
def lineToLine(line0, line1):
    if line0.Type == LineType.VERTICAL and line1.Type == LineType.VERTICAL:
        return verticalToVertical(line, line)
    elif line0.Type == LineType.VERTICAL and line1.Type == LineType.CIRCLE:
        return verticalToCircle(line, line)
    elif line0.Type == LineType.CIRCLE and line1.Type == LineType.VERTICAL:
        return circalToVertical(line, line)
    else:
        return circleToCircle(line0, line1)
    
def verticalToCircle(vertical, circle):
    return circleToVertical(circle, vertical).inverse()    

def circleToVertical(circle, vertical):
    u = vertical.IntersectionXaxis
    return Moeb(1.0, u, .0, 1.0) * circleToYAxis(circle)

def circleToYAxis(circle):
    c = circle.Center
    r = circle.Radius

    return Moeb(1 / (math.sqrt(2.0 * r)), - c / (math.sqrt(2.0 * r)) + math.sqrt(r / 2.0), 
        - 1 / (math.sqrt(2.0 * r)), c / (math.sqrt(2.0 * r)) + math.sqrt(r / 2.0))

def verticalToVertical(vertical0, vertical1):
    return Moeb(1.0, vertical0.z1.RealPart - vertical.z0.RealPart, .0, 1.0)

def circleToCircle(circle0, circle1):
    c0 = circle0.Center
    r0 = circle0.Radius
    c1 = circle1.Center
    r1 = circle1.Radius
    
    return moebFromTo(ComplexNumber(c0, r0), ComplexNumber(c1, r1))

def reflection(line):
    return reflection0(1.0).conjugate(lineToLine(line, UnitCircle))




