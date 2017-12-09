import numpy as np
import math
import copy
import matplotlib.pyplot as plt
import itertools 

def addFullCurve(points):
	lineset = []
	for i in range(1,len(points)):
		lineset.append([points[i-1],points[i]])
	lineset.append([points[0],points[len(points)-1]])
	return lineset

def buildLineset(shape):
	face_curve = shape[:17]
	left_eyebro = shape[17:22]
	right_eyebro = shape[22:27]
	nose = shape[27:36]
	left_eye = shape[36:42]
	right_eye = shape[42:48]
	mouth = shape[48:]
	lineset = []
	lineset.extend(addFullCurve(face_curve))
	lineset.extend(addFullCurve(left_eyebro))
	lineset.extend(addFullCurve(right_eyebro))
	lineset.append([shape[21],shape[22]])
	lineset.append([shape[21],shape[27]])
	lineset.append([shape[22],shape[27]])
	lineset.extend(addFullCurve(nose))
	lineset.append([shape[35],shape[30]])
	lineset.extend(addFullCurve(left_eye))
	lineset.extend(addFullCurve(right_eye))
	lineset.extend(addFullCurve(mouth))
	lineset.append([shape[51],shape[57]])
	lineset.append([shape[48],shape[54]])
	lineset.append([shape[1],shape[15]])
	lineset.append([shape[2],shape[14]])
	lineset.append([shape[3],shape[13]])
	lineset.append([shape[4],shape[12]])
	lineset.append([shape[5],shape[11]])
	lineset.append([shape[6],shape[10]])
	lineset.append([shape[7],shape[9]])
	x_mid = (shape[19][0]+shape[24][0])/2
	y_mid = (shape[19][1]+shape[24][1])/2
	lineset.append([[x_mid,y_mid],shape[8]])
	return lineset

def convert(s):
	l = [[int(x) for x in i.split()] for i in s.split(',')]
	lineset = buildLineset(l)
	return lineset

def penalty(angle):
	return angle**2;

def dist(x,y):
	return ((x[0]-y[0])**2 + (x[1]-y[1])**2)**(1/2)

def samePoint(x,y):
	if(x[0] == y[0] and x[1] == y[1]):
		return True
	return False

def closePoints(line1,line2):
	# print(line1,line2)
	def getQuadrant(x,y):
		if (x>=0 and y>=0):
			return 1
		elif (x<=0 and y>=0):
			return 2
		elif (x<=0 and y<=0):
			return 3
		else:
			return 4

	def getPoints(l,x,y):
		q = getQuadrant(x,y)
		if(q in [1,2]):
			return l
		else:
			return l[::-1]

	diff_x_1 = line1[1][0]-line1[0][0]
	diff_x_2 = line2[1][0]-line2[0][0]
	diff_y_1 = line1[1][1]-line1[0][1]
	diff_y_2 = line2[1][1]-line2[0][1]
	line1 = getPoints(line1,diff_x_1,diff_y_1)
	line2 = getPoints(line2,diff_x_2,diff_y_2)
	# print(line1,line2)
	# print ([[line1[0],line2[0]],[line1[1],line2[1]]])
	return [[line1[0],line2[0]],[line1[1],line2[1]]]


def getSlope(x,y):
	if(not x):
		if(y >= 0):
			return math.pi/2
		else:
			return - math.pi/2
	else:
		return math.atan(y/x)

def rotate(line1,line2,length,angle):
	if(angle == 0.0):
		return line1
	slope1 = getSlope(line1[1][0]-line1[0][0],line1[1][1] - line1[0][1])
	slope2 = getSlope(line2[1][0]-line2[0][0],line2[1][1] - line2[0][1])
	rotate_angle = (math.pi/2) - max(slope1,slope2) + (angle/2)
	# print("Slope 1 : ",slope1, " slope2 : ",slope2 , length, math.degrees(angle))
	# print("Angle to rotate_angle", math.degrees(rotate_angle))
	delta_y = length * math.sin(angle/2) * math.sin(rotate_angle)
	delta_x = length * math.sin(angle/2) * math.cos(rotate_angle)
	# print(delta_x,delta_y)
	# print(slope1,slope2)
	if(slope1 < slope2):
		if(line1[0][0] - line1[1][0] < 0 or line1[0][1] - line1[1][1] < 0):
			line1[0][0] += delta_x
			line1[0][1] -= delta_y
			line1[1][0] -= delta_x
			line1[1][1] += delta_y
		else:
			line1[0][0] -= delta_x
			line1[0][1] += delta_y
			line1[1][0] += delta_x
			line1[1][1] -= delta_y
	elif(slope1 > slope2):
		if(line1[0][0] - line1[1][0] < 0 or line1[0][1] - line1[1][1] < 0):
			line1[0][0] -= delta_x
			line1[0][1] += delta_y
			line1[1][0] += delta_x
			line1[1][1] -= delta_y
		else:
			line1[0][0] += delta_x
			line1[0][1] -= delta_y
			line1[1][0] -= delta_x
			line1[1][1] += delta_y
	return line1

def findAngleDiff(line1,line2):
	# print(line1,line2)
	slope1 = getSlope(line1[1][0]-line1[0][0],line1[1][1]-line1[0][1])
	slope2 = getSlope(line2[1][0]-line2[0][0],line2[1][1]-line2[0][1])
	# print(math.degrees(slope1),math.degrees(slope2))
	angleDiff = slope2 - slope1
	return abs(angleDiff)

def LHD(line1,line2):
	# print(line1,line2)
	line1 = copy.deepcopy(line1)
	line2 = copy.deepcopy(line2)

	angleDiff = findAngleDiff(line1,line2)
	# print("angleDiff :: ",math.degrees(angleDiff))
	
	line1Vect = np.array([line1[1][0]-line1[0][0],line1[1][1] - line1[0][1]])
	line2Vect = np.array([line2[1][0]-line2[0][0],line2[1][1] - line2[0][1]])
	vec1Len = np.linalg.norm(line1Vect)
	vec2Len = np.linalg.norm(line2Vect)
	# print("Before :: ",line1,line2)
	if(vec1Len < vec2Len):
		# print("Path 1")
		line1 = rotate(line1, line2, vec1Len, angleDiff)
	else:
		# print("Path 2")
		line2 = rotate(line2, line1, vec2Len, angleDiff)
	# print("After :: ",line1,line2)
	# print("Angle Difference :: ", math.degrees(findAngleDiff(line1,line2)),end = "\n\n")
	slope = getSlope(line1[1][0]-line1[0][0],line1[1][1] - line1[0][1]) + getSlope(line2[1][0]-line2[0][0],line2[1][1] - line2[0][1])
	slope /= 2
	points = closePoints(line1,line2)
	# print(points)
	edgeSlopes = [abs(getSlope(i[1][0]-i[0][0],i[1][1]-i[0][1])) for i in points]
	# print([math.degrees(i) for i in edgeSlopes] , math.degrees(slope))
	edgeAngle = [((math.pi/2) - abs(slope-angle)) for angle in edgeSlopes]
	# print("The angles : ",[math.degrees(i) for i in edgeAngle])
	perDist = [dist(points[i][0],points[i][1])*math.cos(edgeAngle[i]) for i in range(len(points))]
	perDist = sum(perDist)/len(perDist)
	# print("Perpendicular Distance : ",perDist)
	parDist = [dist(points[i][0],points[i][1])*math.sin(edgeAngle[i]) for i in range(len(points))]
	parDist = min(parDist)
	# print("Parallel Distance : ",parDist)
	# print(line1,line2)
	return (penalty(angleDiff)**4 + perDist**4 + parDist**4 )**0.25
	# print(perDist)

def LHD_set_lines(lineSet1,lineSet2,p=False):
	totalLength = 0
	LHDSum = 0
	for line1 in lineSet1:
		line1Len = dist(line1[0],line1[1])
		totalLength += line1Len
		l = [LHD(line1,line2) for line2 in lineSet2]
		if(p):
			print(lineSet1.index(line1),line1, "______________________________")
			for i in range(len(l)):
				print(lineSet2[i], " :: ", l[i])
			print("______________________________", line1Len, min(l), l.index(min(l)), lineSet2[l.index(min(l))],"______________________________")
		LHDSum += line1Len * min(l)
	if(p):
		print("______________________________________________________________________________________")
	return LHDSum/totalLength

def primaryLHD(lineSet1,lineSet2):
	set1 = LHD_set_lines(lineSet1,lineSet2)
	set2 = LHD_set_lines(lineSet2,lineSet1)
	return max(set1,set2)

def newLHD(lineSet1,lineSet2,p=False):
	LHDSum = 0
	totalLength = 0
	for i in range(len(lineSet1)):
		line1 = lineSet1[i]
		line2 = lineSet2[i]
		line1Len = dist(line1[0],line1[1])
		totalLength += line1Len
		LHDval = LHD(line1,line2)
		LHDSum += line1Len * LHDval
		if(p):
			print(line1, line2, LHDval, LHDSum)
	return LHDSum/totalLength

def newPrimaryLHD(lineSet1,lineSet2):
	set1 = newLHD(lineSet1,lineSet2)
	set2 = newLHD(lineSet2,lineSet1)
	return max(set1,set2)

# lineSet1 = convert(input())
# lineSet2 = convert(input())

# print(newPrimaryLHD(lineSet1,lineSet2))
# print(primaryLHD(lineSet1,lineSet2))

# fig=plt.figure()
# ax=fig.add_subplot(111)
# ax.xaxis.set_ticks_position('top')
# ax.invert_yaxis()
# for l in lineSet1:
# 	plt.plot(
# 	    *zip(*itertools.chain.from_iterable(itertools.combinations(l, 2))),
# 	    color = 'brown', marker = 'o')

# for l in lineSet2:
# 	plt.plot(
# 	    *zip(*itertools.chain.from_iterable(itertools.combinations(l, 2))),
# 	    color = 'red', marker = 'o')

# for l in lineSet3:
# 	plt.plot(
# 	    *zip(*itertools.chain.from_iterable(itertools.combinations(l, 2))),
# 	    color = 'green', marker = 'o')

# plt.show()
