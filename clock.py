#!/usr/bin/python3

import sys
import time
import matplotlib.pyplot as plt
import math
import numpy as np

class Clock:
    def __init__(self):
        self.clock_diam = 350 #mm
    
    def generate_points(self):
        num_points = 50; 
        rotation = 2*math.pi
        step = rotation/num_points
        points = np.empty((num_points,2))
        for val in range(0, num_points):
            angle = val*step
            angle_deg = angle * 180/math.pi
            print(angle_deg)
            points[val,:] = [angle, self.diameter]
        print(str(points)  +  " " + str(points.shape))
        return points

    def plot_points_pol(self, points):
        plt.polar(points[:,0], points[:, 1],color='green', marker='o', linestyle="", markersize=2)

    def plot_points_cart(self, points):
        plt.plot(points[:,0], points[:, 1],color='green', marker='o', linestyle="", markersize=2)

    def generate_circle_pol(self, diameter, num_points):
        rotation = 2*math.pi
        step = rotation/num_points
        points = np.empty((num_points,2))
        for val in range(0, num_points):
            angle = val*step
            points[val,:] = [angle, diameter]
        return points
    
    # def generate_circle_cartesian(self, diameter, x_pos, y_pos, num_points):
    #     points = np.empty((num_points,2))
    #     for x_val in range()

    def generate_rect_cart(self, x_len, y_len, x_pos, y_pos, num_points):
        points = np.empty((num_points,2))
        step = ((x_len+y_len)/(num_points/4))
        print(step)
        array_enum = 0
        neg_x = (-x_len/2) + x_pos
        pos_x = (x_len/2) + x_pos
        neg_y = (-y_len/2) + y_pos
        pos_y = (y_len/2) + y_pos
        print(-x_len/2)
        for x_val in np.arange(neg_x, pos_x, step):
            points[array_enum, :] = [x_val, pos_y]
            array_enum = array_enum + 1
            points[array_enum, :] = [x_val, neg_y]
            array_enum = array_enum + 1
        
        print(array_enum)
        for y_val in np.arange(neg_y, pos_y, step):
            points[array_enum, :] = [pos_x, y_val]
            array_enum = array_enum + 1
            points[array_enum, :] = [neg_x, y_val]
            array_enum = array_enum + 1
        
        return points

    def convert_to_pol(self, points):
        polar_points = np.empty_like(points)
        for idx, point in enumerate(points):
            polar_points[idx,:] = cart_2_pol(point)
        
        return polar_points

    def offset_points(self, points, x_pos, y_pos):
        offset_points = np.empty_like(points)
        for idx,point in enumerate(points):
            offset_points[idx,0] = point[0]
            offset_points[idx,1] = 2*x_pos*math.cos(point[0])
        return offset_points

    def plot_show(self):
        plt.show()


def cart_2_pol(point):
    rad = np.sqrt(point[0]**2 + point[1]**2)
    theta = np.arctan2(point[1], point[0])
    return([theta, rad])
        
if __name__ == "__main__":
    clock = Clock()
    # points = clock.generate_points()
    # points = clock.generate_circle_pol(40,80)
    # clock.plot_points_pol(points)
    # offset_points = clock.offset_points(points, 0,0)
    square = clock.generate_rect_cart(5, 5, -5, 10, 20)
    # clock.plot_points_cart(square) 
    square_pol = clock.convert_to_pol(square)
    print(square_pol)
    clock.plot_points_pol(square_pol)
    clock.plot_show()


# from stackoverflow: https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates

# class Point(object):
#     def __init__(self, x=None, y=None, r=None, theta=None):
#         """x and y or r and theta(degrees)
#         """
#         if x and y:
#             self.c_polar(x, y)
#         elif r and theta:
#             self.c_rect(r, theta)
#         else:
#             raise ValueError('Must specify x and y or r and theta')
#     def c_polar(self, x, y, f = polar):
#         self._x = x
#         self._y = y
#         self._r, self._theta = f(self._x, self._y)
#         self._theta_radians = math.radians(self._theta)
#     def c_rect(self, r, theta, f = rect):
#         """theta in degrees
#         """
#         self._r = r
#         self._theta = theta
#         self._theta_radians = math.radians(theta)
#         self._x, self._y = f(self._r, self._theta)
#     def setx(self, x):
#         self.c_polar(x, self._y)
#     def getx(self):
#         return self._x
#     x = property(fget = getx, fset = setx)
#     def sety(self, y):
#         self.c_polar(self._x, y)
#     def gety(self):
#         return self._y
#     y = property(fget = gety, fset = sety)
#     def setxy(self, x, y):
#         self.c_polar(x, y)
#     def getxy(self):
#         return self._x, self._y
#     xy = property(fget = getxy, fset = setxy)
#     def setr(self, r):
#         self.c_rect(r, self._theta)
#     def getr(self):
#         return self._r
#     r = property(fget = getr, fset = setr)
#     def settheta(self, theta):
#         """theta in degrees
#         """
#         self.c_rect(self._r, theta)
#     def gettheta(self):
#         return self._theta
#     theta = property(fget = gettheta, fset = settheta)
#     def set_r_theta(self, r, theta):
#         """theta in degrees
#         """
#         self.c_rect(r, theta)
#     def get_r_theta(self):
#         return self._r, self._theta
#     r_theta = property(fget = get_r_theta, fset = set_r_theta)
#     def __str__(self):
#         return '({},{})'.format(self._x, self._y)
