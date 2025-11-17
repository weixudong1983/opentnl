"""
Zap Game - Python Version
Simplified reimplementation of the OpenTNL Zap game

Core geometric and math classes
"""
import math


class Point:
    """2D Point with vector operations"""
    
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
    
    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def len(self):
        """Length of vector"""
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def len_squared(self):
        """Squared length (faster, no sqrt)"""
        return self.x * self.x + self.y * self.y
    
    def normalize(self, new_len=1.0):
        """Normalize to unit vector or specified length"""
        length = self.len()
        if length == 0:
            self.x = new_len
            self.y = 0
        else:
            factor = new_len / length
            self.x *= factor
            self.y *= factor
    
    def normalized(self, new_len=1.0):
        """Return normalized copy"""
        result = Point(self.x, self.y)
        result.normalize(new_len)
        return result
    
    def dot(self, other):
        """Dot product"""
        return self.x * other.x + self.y * other.y
    
    def set(self, x, y):
        """Set coordinates"""
        self.x = float(x)
        self.y = float(y)
    
    def copy(self):
        """Return a copy"""
        return Point(self.x, self.y)
    
    def to_tuple(self):
        """Convert to tuple for pygame"""
        return (int(self.x), int(self.y))


class Color:
    """RGB color"""
    
    def __init__(self, r=1.0, g=1.0, b=1.0):
        self.r = r
        self.g = g
        self.b = b
    
    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)
    
    def __mul__(self, scalar):
        return Color(self.r * scalar, self.g * scalar, self.b * scalar)
    
    def interp(self, t, c1, c2):
        """Interpolate between two colors"""
        one_minus_t = 1.0 - t
        self.r = c1.r * t + c2.r * one_minus_t
        self.g = c1.g * t + c2.g * one_minus_t
        self.b = c1.b * t + c2.b * one_minus_t
    
    def to_pygame(self):
        """Convert to pygame RGB tuple (0-255)"""
        return (
            int(max(0, min(255, self.r * 255))),
            int(max(0, min(255, self.g * 255))),
            int(max(0, min(255, self.b * 255)))
        )


class Rect:
    """Axis-aligned bounding rectangle"""
    
    def __init__(self, p1=None, p2=None):
        if p1 is None:
            self.min = Point()
            self.max = Point()
        else:
            self.set(p1, p2)
    
    def set(self, p1, p2):
        """Set rectangle from two points"""
        self.min = Point(min(p1.x, p2.x), min(p1.y, p2.y))
        self.max = Point(max(p1.x, p2.x), max(p1.y, p2.y))
    
    def get_center(self):
        """Get center point"""
        return (self.min + self.max) * 0.5
    
    def contains(self, p):
        """Check if point is inside rectangle"""
        return (p.x >= self.min.x and p.x <= self.max.x and
                p.y >= self.min.y and p.y <= self.max.y)
    
    def intersects(self, other):
        """Check if rectangles intersect"""
        return (self.min.x < other.max.x and self.min.y < other.max.y and
                self.max.x > other.min.x and self.max.y > other.min.y)
    
    def union_point(self, p):
        """Expand to include point"""
        self.min.x = min(self.min.x, p.x)
        self.min.y = min(self.min.y, p.y)
        self.max.x = max(self.max.x, p.x)
        self.max.y = max(self.max.y, p.y)
    
    def expand(self, delta):
        """Expand by delta"""
        self.min -= delta
        self.max += delta
    
    def get_extents(self):
        """Get size"""
        return self.max - self.min
