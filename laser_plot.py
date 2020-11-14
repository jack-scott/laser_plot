#!/usr/bin/python3

import sys
import time
import matplotlib.pyplot as plt
import math
import numpy as np
import svg.path

def cart_2_pol(x, y):
    try:
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
    except Exception as e:
        print(e)
    return(r, theta)

def cart_2_complex(x, y):
    return(complex(x,y))

def pol_2_cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)

def pol_2_complex(r, theta):
    x, y = pol_2_cart(r,theta)
    return(complex(x, y))

def complex_2_cart(complex_num):
    x = complex_num.real
    y = complex_num.imag
    return(x,y)

def complex_2_pol(complex_num):
    x = complex_num.real
    y = complex_num.imag
    return(cart_2_pol(x,y))



# point class adapted from stackoverflow: https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates

class Point(object):
    def __init__(self, x=None, y=None, r=None, theta=None, complex_num=None):
        """x and y or r and theta(radians)
        """
        if x is not None and y is not None:
            self._init_rect(x, y)
        elif r is not None and theta is not None:
            self._init_polar(r, theta)
        elif complex_num is not None:
            self._init_complex(complex_num)
        else:
            raise ValueError('Must specify x and y or r and theta')
            
    def _init_rect(self, x, y):
        self._x = x
        self._y = y
        self._complex = cart_2_complex(self._x, self._y)
        self._r, self._theta = cart_2_pol(self._x, self._y)

    def _init_complex(self, complex_num):
        self._complex = complex_num
        self._x, self._y = complex_2_cart(self._complex)
        self._r, self._theta = complex_2_pol(self._complex)

    def _init_polar(self, r, theta):
        """theta in radians
        """
        self._r = r
        self._theta = theta
        self._theta_radians = math.radians(theta)
        self._x, self._y = pol_2_cart(self._r, self._theta)
        self._complex = pol_2_complex(self._r, self._theta)

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
    
    def set_complex(self, complex_num):
        self._init_complex(complex_num)

    def get_complex(self):
        return self._complex
    complex_num = property(fget = get_complex, fset= set_complex)

    # TODO - make getter and setter methods for the complex type

    def __str__(self):
        return '({},{})'.format(self._x, self._y)


class Vector(object):
    # For info on adding new types to this class reference the svg.path module https://pypi.org/project/svg.path/
    def __init__(self):
        self.vect_obj = None
        self._get_point_vec = None
        # self._get_point_obj_vec = np.vectorize(Point)

    def get_point(self, pos):
        return Point(self.vect_obj.point[pos])

    def get_points(self, resolution):
        arr = np.arange(0,1, resolution)
        points = self._get_point_vec(arr)
        return points
class Line(Vector):
    def __init__(self, start, end):
        #TODO - Add a check to make sure inputs are of type Point
        self.vect_obj = svg.path.Line(start.complex_num, end.complex_num)
        func = lambda x: Point(complex_num=self.vect_obj.point(x))
        self._get_point_vec = np.vectorize(func)

class Path(Vector):
    def __init__(self, svg_path):
        self.vect_obj = svg.path.parse_path(svg_path)
        func = lambda x: Point(complex_num=self.vect_obj.point(x))
        self._get_point_vec = np.vectorize(func)

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
    # Using a hardware setup with a 200 step/rev stepper motor and a pulley reduction of 1/3.7
    # this means we have 741 steps per revolution. Also assuming a microstep of 1:8 this gives us 
    # 5929 steps of resolution in a rotation. 
    # Also assume we have 350 different steps of resolution in the radial direction
    def __init__(self):
        super(Clock, self).__init__(diameter=350)
        _rotational_resolution = 5929   #steps per 360 degrees
        _radial_resolution = 350    #steps over 350mm



if __name__ == "__main__":
    clock = Clock()
    points=[]
    # Point(complex_num=0+1j)
    square_plot = LaserPlot(height= 400, width = 400)
    line = Line(Point(x=0,y=0), Point(x=10, y=10))
    # path = Path('m 0.05357144,992.21517 2.07142876,-2.875')
    # points = path.get_points(0.05)
    # square_plot.plot(points)
    # square_plot.show_plot()
    points = line.get_points(0.05)
    clock.plot(points)
    clock.show_plot()


