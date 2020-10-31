#!/usr/bin/python3

import sys
import time
import matplotlib.pyplot as plt
import math
import numpy as np

def cart_2_pol(x, y):
    try:
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
    except Exception as e:
        print(e)
    return(r, theta)

def pol_2_cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)


# point class adapted from stackoverflow: https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates

class Point(object):
    def __init__(self, x=None, y=None, r=None, theta=None):
        """x and y or r and theta(radians)
        """
        if x is not None and y is not None:
            self._init_rect(x, y)
        elif r is not None and theta is not None:
            self._init_polar(r, theta)
        else:
            raise ValueError('Must specify x and y or r and theta')
            
    def _init_rect(self, x, y):
        self._x = x
        self._y = y
        self._r, self._theta = cart_2_pol(self._x, self._y)

    def _init_polar(self, r, theta):
        """theta in radians
        """
        self._r = r
        self._theta = theta
        self._theta_radians = math.radians(theta)
        self._x, self._y = pol_2_cart(self._r, self._theta)

    def set_x(self, x):
        self._init_rect(x, self._y)   
    def get_x(self):
        return self._x
    x = property(fget = get_x, fset = set_x)
    
    def set_y(self, y):
        self._init_rect(self._x, y)
    def get_y(self):
        return self._y
    y = property(fget = get_y, fset = set_y)
   
    def set_xy(self, x, y):
        self._init_rect(x, y)
    def get_xy(self):
        return self._x, self._y
    xy = property(fget = get_xy, fset = set_xy)
    
    def set_r(self, r):
        self._init_polar(r, self._theta)
    def get_r(self):
        return self._r
    r = property(fget = get_r, fset = set_r)
    
    def set_theta(self, theta):
        """theta in radians
        """
        self._init_polar(self._r, theta)
    def get_theta(self):
        return self._theta
    theta = property(fget = get_theta, fset = set_theta)
    
    def set_r_theta(self, r, theta):
        """theta in radians
        """
        self._init_polar(r, theta)
    def get_r_theta(self):
        return self._r, self._theta
    r_theta = property(fget = get_r_theta, fset = set_r_theta)
    
    def __str__(self):
        return '({},{})'.format(self._x, self._y)


class LaserPlot(object):
    def __init__(self, diameter=None, height=None, width=None):
        if diameter is not None:
            self._init_circular_plot(diameter)
        elif height is not None and width is not None:
            self._init_rect_plot(height, width)
        else:
            raise ValueError("Requires max diameter(mm) or/ height and width (mm)")

    def _init_circular_plot(self, diameter):
        self._plot_func = "plot_polar"
        self.max_diameter = diameter
        self.max_radius = diameter/2

        #since we are not using a square plot set the max dimension beyond the
        #circular plot in order to pass validity checks
        self.max_width = self.max_radius
        self.max_height = self.max_radius

    def _init_rect_plot(self, height, width):
        self._plot_func = "plot_cart"
        self.max_height = height/2
        self.max_width = width/2

        #set the max radius and diameter beyond the rectangular plot to pass validity checks
        self.max_radius = np.sqrt(height**2 + width**2)
        self.max_diameter = 2 * self.max_radius


    def plot(self, points):
        method = getattr(self, self._plot_func)
        method(points)

    def plot_polar(self, points):
        r = []
        theta = []
        for point in points:
            r.append(point.r)
            theta.append(point.theta)
        plt.polar(theta, r,color='green', marker='o', linestyle="", markersize=2)

    def plot_cart(self, points):
        x = []
        y = []
        for point in points:
            x.append(point.x)
            y.append(point.y)
        plt.plot(x, y ,color='green', marker='o', linestyle="", markersize=2)

    def show_plot(self):
        plt.show()

    def add_point(self, _x=None, _y=None, _r=None, _theta=None):
        point = Point(x=_x, y=_y, r=_r, theta=_theta)
        # check if point lands within the plot
        if abs(point.r) > self.max_radius or abs(point.x) > self.max_width or abs(point.y) > self.max_height:
            raise ValueError("Point x:{} y:{} r:{} theta:{} lies beyond plotting area".format(point.x,point.y,point.r,point.theta))
        return point


class Clock(LaserPlot):
    def __init__(self):
        super(Clock, self).__init__(diameter=350)


if __name__ == "__main__":
    clock = Clock()
    points=[]
    # points.append(clock.add_point(_r=30, _theta=0.75))
    # clock.plot(points)
    # clock.show_plot()
    # laser =LaserPlot(height=20, width=20)
    # points.append(laser.add_point(_x=10, _y=10))
    # laser.plot(points)
    # laser.show_plot()

