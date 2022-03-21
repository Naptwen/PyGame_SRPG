import numpy as np
import math

class pyCamera:
    eye = np.array([0,0,0])
    pyCamera = np.array([10,10,10])

def unit_vec(self, vec):
    len = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
    nor = np.array([vec[0] / len, vec[1] / len, vec[2] / len ])
    return nor

#pyCamera x, y
def pyCamera_mov(self, pyCamera, x, y):
    vec = pyCamera[0] - pyCamera[1]
    up  = np.array([0,0,1])
    hor = self.unit_vec(np.cross(vec, up))
    if x != 0:
        pyCamera[0] = pyCamera[0] + hor * x
        pyCamera[1] = pyCamera[1] + hor * x
    else :
        pyCamera[0] = pyCamera[0] + np.array([0, 0 ,1]) * y
        pyCamera[1] = pyCamera[1] + np.array([0, 0 ,1]) * y

#pyCamera rotating
#pyCamera, r 
def pyCamera_rot_xy(self, pyCamera, r):
    vec = pyCamera[1] - pyCamera[0]
    r = math.radians(r)
    _x = math.cos(r) * vec[0] - math.sin(r) * vec[1]
    _y = math.sin(r) * vec[0] + math.cos(r) * vec[1]
    new_vec = np.array([_x + pyCamera[0][0], _y + pyCamera[0][1], pyCamera[1][2]])
    pyCamera[1] = new_vec
    return pyCamera

#eye rotating
#pyCamera, r 
def eye_rot_xy(self, pyCamera, r):
    vec = pyCamera[1] - pyCamera[0]
    r = math.radians(r)
    _x = math.cos(r) * vec[0] - math.sin(r) * vec[1]
    _y = math.sin(r) * vec[0] + math.cos(r) * vec[1]
    new_vec = np.array([_x + pyCamera[0][0], _y + pyCamera[0][1], pyCamera[1][2]])
    pyCamera[0] = new_vec
    return pyCamera 

#pyCamera, zoom
def pyCamera_zoom(self, pyCamera, zoom):
    vec = pyCamera[1] - pyCamera[0]
    new_vec = pyCamera[1] + vec * zoom
    pyCamera[1] = new_vec
    return pyCamera