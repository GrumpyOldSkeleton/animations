#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vector.py
#  
import math

class Vector2(object):
    
    def __init__(self,x,y):
        
        self.x = float(x)
        self.y = float(y)
                
    def add(self, v):
        
        self.x += v.x
        self.y += v.y
    
    def sub(self, v):
        
        self.x -= v.x
        self.y -= v.y
        
    def mult(self, m):
        
        self.x *= m
        self.y *= m
    
    def div(self, d):
        
        self.x /= float(d)
        self.y /= float(d)
        
    def mag(self):
        
        # the length of the vector        
        return math.sqrt(self.x * self.x + self.y * self.y)
        
    def normalise(self):
        
        m = self.mag()
        if m != 0:
            self.div(m)
            
    def getCopy(self):
        
        n = Vector2(self.x, self.y)
        return n
        
    def set(self, v):
        
        # set this vector to the same values as a vector passed in
        self.x = v.x
        self.y = v.y
        
    def setFromValues(self, x, y):
        
        # set this vector to x y passed in
        self.x = float(x)
        self.y = float(y)
        
    def setFromAngle(self, angle_degrees):
        
        # set the vector to angle_degrees (0..360)
        self.x = math.cos(math.radians(angle_degrees))
        self.y = math.sin(math.radians(angle_degrees))
        
    def rotate(self, angle_radians):
        
        # Rotate the vector by angle_radians radians
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y
        
    def rotate_degrees(self, angle_degrees):
        
        # rotate the vector by angle_degrees degrees
        self.rotate(math.radians(angle_degrees))
        
    def headingRadians(self):
        
        # returns the angle in radians of the vector
        m = self.mag()
        if m == 0:
            return 0
        else:
            return math.atan2(self.y, self.x)
            
    def headingDeg180(self):
        
        # returns the angle in degrees of the vector
        # below the line it goes 0-180, above -180-0
        return  math.degrees(self.headingRadians())
        
    def headingDeg360(self):
        
        # returns the heading of the vector in angle of 0..360 degrees
        angle = self.headingDeg180()
        if angle < 0:
            angle = angle + 360
        return angle
        
    def limit(self, minn, maxn):
        
        self.x = self.clamp(self.x, minn, maxn)
        self.y = self.clamp(self.y, minn, maxn)
            
    def clamp(self, n, minn, maxn):
        
        if n < minn:
            return minn
        elif n > maxn:
            return maxn
        else:
            return n
            
    def dot(self, other):
        
        # returns dot product of this vector and other vector
        return float(self.x * other.x + self.y * other.y)
        
    def angleBetween(self, other):
        
        # returns angle in radians between this vector and other vector
        cross = self.x * other.y - self.y * other.x
        dot = self.x * other.x + self.y * other.y
        return math.atan2(cross, dot)
        
    def angleBetweenDegrees180(self, other):
        
        # returns angle in degrees between this vector and other vector
        # below the line it goes 0-180, above -180-0
        return math.degrees(self.angleBetween(other))
        

    

