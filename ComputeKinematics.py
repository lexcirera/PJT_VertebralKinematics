
import scipy.optimize
from mpl_toolkits.mplot3d import Axes3D


import PIL.Image
from PIL import Image, ImageEnhance,ImageDraw,ImageFont
import numpy as np
import matplotlib
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.cluster import DBSCAN
from pylab import *
import copy
import sys


def barryCentre(x,y,z):
    """
    return the center of gravity of the points given to define the vertebra, not taking into account the vertebras' weight repartition
    """
    xg = np.average(x)
    yg = np.average(y)
    zg = np.average(z)
    return xg,yg,zg


def Minimax(x, y, z):
    """
    return the coefficient of the least square plan of the given points
    """
    #fit a plan
    tmp_A = []
    tmp_b = []
    for i in range(len(x)):
        tmp_A.append([x[i], y[i], 1])
        tmp_b.append(z[i])
    b = np.matrix(tmp_b).T
    A = np.matrix(tmp_A)
    fit = (A.T * A).I * A.T * b

    #plane coefficient
    a,b,c = float(fit[0]), float(fit[1][0]), float(fit[2][0])
    return a, b, c

def MobileBase(a,b,c):
    """
    take a,b,c the coefficient of the plane defined by : Z=ax+by+c, return the vectors' directions of the local base
    """
    a = round(a,2)
    b = round(b,2)

    vectNormal =np.array([a,b,-1])*(1/np.linalg.norm([a,b,-1]))
    vectI = np.array([-b,a,0])*(1/np.linalg.norm([-b,a,0]))
    vectJ = np.cross(vectI,vectNormal)

    return vectNormal,vectI,vectJ