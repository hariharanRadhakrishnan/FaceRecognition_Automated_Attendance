import cv2
import numpy as np
import random


def draw_delaunay(img, subdiv, delaunay_color ) :

    triangleList = subdiv.getTriangleList();
    
   # size = img.shape
    #r = (0, 0, size[1], size[0])
    veronoiLEM = []
    for t in triangleList :

        pt1 = [t[0], t[1]]
        pt2 = [t[2], t[3]]
        pt3 = [t[4], t[5]]
        veronoiLEM.append([pt1,pt2])
        veronoiLEM.append([pt2,pt3])
        veronoiLEM.append([pt1,pt3])

    return veronoiLEM