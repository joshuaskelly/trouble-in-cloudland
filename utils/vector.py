import math
import operator

from utils.fastmath import cos, sin


class Vector2d(object):
    def __init__(self, x_or_sequence, y = None):
        if y is None:
            try:
                self.vector = [x_or_sequence[0], x_or_sequence[1]]
            except TypeError:
                raise TypeError('Vector2d requires a tuple or two arguments')
            
        else:
            self.vector = [x_or_sequence, y]
            
    def getX(self):
        return self.vector[0]

    def setX(self, value):
        self.vector[0] = value

    x = property(getX, setX)
    
    def getY(self):
        return self.vector[1]

    def setY(self, value):
        self.vector[1] = value

    y = property(getY, setY)    
    
    def set(self, x, y):
        self.vector[0] = x
        self.vector[1] = y
        
    def __repr__(self):
        return 'Vector2d(%s, %s)' % (self.x, self.y)
    
    def __len__(self):
        return 2
    
    def __getitem__(self, key):
        return self.vector[key]
    
    def __setitem__(self, key, value):
        self.vector[key] = value
        
    def __eq__(self, other):
        return self.vector[0] == other[0] and self.vector[1] == other[1]
    
    def __ne__(self, other):
        return self.vector[0] != other[0] or self.vector[1] != other[1]
    
    def __nonzero__(self):
        return bool(self.vector[0]) or bool(self.vector[1])
    
    # Generic Operation Handling
    def _o2(self, other, operation):
        try:
            return Vector2d(operation(self.vector[0], other[0]), operation(self.vector[1], other[1]))

        except TypeError:
            return Vector2d(operation(self.vector[0], other), operation(self.vector[1], other))
             
    def _r_o2(self, other, operation):
        try:
            return Vector2d(operation(other[0], self.vector[0]), operation(other[1], self.vector[1]))

        except TypeError:
            return Vector2d(operation(other, self.vector[0]), operation(other, self.vector[1]))
            
    def _o1(self, operation):
        return Vector2d(operation(self.vector[0]), operation(self.vector[1]))
        
    def __add__(self, other):
        return self._o2(other, operator.add)

    __radd__ = __add__
    
    def __sub__(self, other):
        return self._o2(other, operator.sub)
    
    def __rsub__(self, other):
        return self._r_o2(other, operator.sub)
    
    def __mul__(self, other):
        return self._o2(other, operator.mul)

    __rmul__ = __mul__
    
    def __div__(self, other):
        return self._o2(other, operator.div)
    
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__

    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
    
    def __neg__(self, other):
        return self._o2(other, operator.neg)

    def __pos__(self, other):
        return self._o2(other, operator.pos)
    
    def __abs__(self, other):
        return self._o2(other, operator.abs)
    
    def __invert__(self, other):
        return self._o2(other, operator.invert)
    
    # Vector Functions
    def get_magnitude(self):
        return math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2)

    def set_magnitude(self, value):
        self.make_normal()
        self.vector[0] *= value
        self.vector[1] *= value
        
    magnitude = property(get_magnitude, set_magnitude)

    def make_normal(self):
        magnitude = self.get_magnitude()

        if magnitude != 0:
            self.vector[0] /= magnitude
            self.vector[1] /= magnitude
        
        return Vector2d(self.vector[0], self.vector[1])
            
    def get_angle(self):
        if self.vector[0] == 0 and self.vector == 0:
            return 0
        return math.degrees(math.atan2(self.vector[1], self.vector[0]))
    
    def set_angle(self, value):
        self.vector[0] = self.get_magnitude()
        self.vector[1] = 0
        x = self.vector[0] * cos[int(value)] - self.vector[1] * sin[int(value)]
        y = self.vector[0] * sin[int(value)] + self.vector[1] * cos[int(value)]
        
        self.vector[0] = x
        self.vector[1] = y
        
    angle = property(get_angle, set_angle, None, 'Gets or Sets the magnitude of a Vector')
    
    def get_perpendicular(self):
        return Vector2d(-self.vector[1], self.vector[0])
    
    def dot(self, other):
        return self.vector[0] * other[0] + self.vector[1] * other[1]
    
    def copy(self):
        return Vector2d(self.vector[0], self.vector[1])

Vector2d.zero = Vector2d(0.0, 0.0)
Vector2d.up = Vector2d(0.0, -1.0)
