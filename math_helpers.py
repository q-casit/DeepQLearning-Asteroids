from math import *

def rndint(num): return int(num+0.5)

def rotate_point(point, angle_rad):
    return [
        cos(angle_rad)*point[0] - sin(angle_rad)*point[1],
        sin(angle_rad)*point[0] + cos(angle_rad)*point[1]
    ]
