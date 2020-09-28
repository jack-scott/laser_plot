#!/usr/bin/python3

import sys
import time
import matplotlib.pyplot as plt
from math import pi
import numpy as np

class Clock:
    def __init__(self):
        self.diameter = 350 #mm
    
    def generate_points(self):
        num_points = 50; 
        rotation = 2*pi
        step = rotation/num_points
        points = np.empty((num_points,2))
        for val in range(0, num_points):
            angle = val*step
            angle_deg = angle * 180/pi
            print(angle_deg)
            points[val,:] = [angle, self.diameter]
        print(str(points)  +  " " + str(points.shape))
        return points

    def plot_clock(self, points):
        plt.polar(points[:,0], points[:, 1],color='green', marker='o', linestyle="", markersize=2)
        # plt.
        plt.show()

if __name__ == "__main__":
    clock = Clock()
    points = clock.generate_points()
    clock.plot_clock(points)


