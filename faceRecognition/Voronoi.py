import cv2
import numpy as np
import random
import copy

def get_delaunay_lineset(points, shapeX, shapeY,name,i) :
	points = copy.deepcopy(points)
	rect = (0,0,shapeX,shapeY)
	subdiv = cv2.Subdiv2D(rect);
	for p in points :
	    subdiv.insert(tuple(p))
	triangleList = subdiv.getTriangleList();
	veronoiLEM = []
	for t in triangleList :
		pt1 = [t[0], t[1]]
		pt2 = [t[2], t[3]]
		pt3 = [t[4], t[5]]
		line1 = [pt1,pt2]
		line2 = [pt2,pt3]
		line3 = [pt1,pt3]
		if(line1 not in veronoiLEM):
			veronoiLEM.append(line1)
		if(line2 not in veronoiLEM):
			veronoiLEM.append(line2)
		if(line3 not in veronoiLEM):	
			veronoiLEM.append(line3)
	# print(i,name,veronoiLEM)
	return veronoiLEM

# points = input()
# points = [[int(j) for j in i.split()] for i in points.split(',')]
# lineset = get_delaunay_lineset(points,200,200)
# print(lineset, len(lineset))