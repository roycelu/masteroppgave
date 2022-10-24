"""
This module is used for utility and helper functions.
Class:
Vector2: 2D vector class representation with x and y components
Function:
pose_dist: calculate distance between two ROS Pose type variables
"""
import math

class Vector2(object):
    """
    2D vector class representation with x and y components.
    Supports simple addition, subtraction, multiplication, division and
    normalization, as well as getting norm and angle of the vector and
    setting limit and magnitude.
    Attributes:
    x (float): x component of the vector
    y (float): y component of the vector
    Methods:
    norm(self): Return the norm of the vector
    arg(self): Return the angle of the vector
    normalize(self): Normalize the vector
    limit(self, value): Limit vector’s maximum magnitude to given value
    set_mag(self, value): Set vector’s magnitude without changing direction
    """
    def __init__(self, x=0, y=0):
        """
        Initialize vector components.
        Args:
        x (float): x component of the vector
        y (float): y component of the vector
        """
        self.x = x
        self.y = y

    @classmethod
    def from_norm_arg(cls, norm=0, arg=0):
        inst = cls(1, 1)
        inst.set_mag(norm)
        inst.set_angle(arg)
        return inst

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x - other, self.y - other)
    
    def __div__(self, other):
        if isinstance(other, self.__class__):
            raise ValueError("Cannot divide two vectors!")
        elif isinstance(other, int) or isinstance(other, float):
            if other != 0:
                return Vector2(self.x / other, self.y / other)
            else:
                return Vector2()

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            raise NotImplementedError("Multiplying vectors is not implemented!")
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __str__(self):
        return "({: .5f}, {: 6.1f})".format(self.norm(), self.arg())
        # return "({: .3f}, {: .3f})".format(self.x, self.y)
    
    def __repr__(self):
        return "Vector2({0}, {1})\n\t.norm = {2}\n\t.arg = {3}".format(self.x, self.y, self.norm(), self.arg())
    
    def norm(self):
        """Return the norm of the vector."""
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))
    
    def arg(self):
        """Return the angle of the vector."""
        return math.degrees(math.atan2(self.y, self.x))

    def set_mag(self, value):
        """Set vector’s magnitude without changing direction."""
        if self.norm() == 0:
            self.x = 1
            self.y = 0
        else:
            self.normalize()
        self.x *= value
        self.y *= value
        
    def set_angle(self, value):
        """Set vector’s direction without changing magnitude."""
        if self.norm() == 0:
            self.x = 1
            self.y = 0
        delta = angle_diff(self.arg(), value)
        self.rotate(delta)

    def rotate(self, value):
        """Rotate vector by degrees specified in value."""
        value = math.radians(value)
        self.x, self.y = math.cos(value) * self.x - math.sin(value) * self.y, \
        math.sin(value) * self.x + math.cos(value) * self.y


    def normalize(self, ret=False):
        """Normalize the vector."""
        d = self.norm()
        if d:
            if not ret:
                self.x /= d
                self.y /= d
            else:
                return Vector2(self.x / d, self.y / d)
    
    def limit(self, value):
        """Limit vector’s maximum magnitude to given value."""
        if self.norm() > value:
            self.set_mag(value)
    
    def limit_lower(self, value):
        """Limit vector’s minimum magnitude to given value."""
        if self.norm() < value:
            self.set_mag(value)
    
    def constrain(self, old_value, max_value):
        """Limit vector’s change of direction to max_value from old_value."""
        desired_value = self.arg()
        delta = angle_diff(old_value, desired_value)
        if abs(delta) > max_value:
            value = angle_diff(desired_value, old_value + math.copysign(max_value, delta))
            self.rotate(value)
    
    def angle_diff(from_angle, to_angle):
        diff = (to_angle - from_angle) % 360
        if diff >= 180:
            diff -= 360
        return diff
    
    def pose_dist(pose1, pose2):
        """Return Euclidean distance between two ROS poses."""
        x1 = pose1.position.x
        y1 = pose1.position.y
        x2 = pose2.position.x
        y2 = pose2.position.y
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
