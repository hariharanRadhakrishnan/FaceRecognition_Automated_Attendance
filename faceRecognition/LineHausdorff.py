import numpy as np
import math
import copy
import matplotlib.pyplot as plt
import itertools 

def convert(s):
	# l = [[int(x) for x in i.split()] for i in s.split(',')]
	l=s
	lineset = []
	for i in range(1,len(l)):
		line = []
		line.append(l[i-1])
		line.append(l[i])
		lineset.append(line)
	lineset.append([l[len(l)-1],l[0]])
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

def LHD_set_lines(lineSet1,lineSet2):
	totalLength = 0
	LHDSum = 0
	for line1 in lineSet1:
		# print(line1)
		line1Len = dist(line1[0],line1[1])
		totalLength += line1Len
		l = [LHD(line1,line2) for line2 in lineSet2]
		# print(l,end="\n\n")
		LHDSum += line1Len * min(l)
	return LHDSum/totalLength

def primaryLHD(lineSet1,lineSet2):
	set1 = LHD_set_lines(lineSet1,lineSet2)
	set2 = LHD_set_lines(lineSet2,lineSet1)
	# print("SET VALUES" , set1,set2)
	return max(set1,set2)


# line1 = [[[8,10],[-9,-20]]]
# line2 = [[[4,5],[8,10]]]
# lineSet1 = convert(input())# [[[27, 110],[31, 129]],[[36, 147],[42, 165]],[[54, 179],[68, 192]],[[85, 202],[105, 203]],[[124, 200],[139, 188]],[[151, 173],[160, 157]],[[165, 138],[168, 119]],[[169, 100],[168, 80]]]
# lineSet2 = convert(input())# [[[27, 111],[31, 130]],[[36, 147],[43, 163]],[[54, 178],[66, 191]],[[82, 201],[101, 203]],[[121, 201],[135, 189]],[[147, 173],[157, 156]],[[163, 138],[166, 119]],[[166, 100],[165, 81]]]
# lineSet3 = convert(input())# [[[34, 125],[39, 144]],[[46, 161],[57, 177]],[[70, 191],[86, 201]],[[107, 202],[128, 201]],[[145, 192],[158, 178]],[[169, 161],[176, 143]],[[179, 123],[179, 103]]]
# lineSet4 = [[[26, 92], [28, 110]], [[28, 110], [32, 127]], [[32, 127], [37, 144]], [[37, 144], [43, 161]], [[43, 161], [54, 176]], [[54, 176], [67, 186]], [[67, 186], [86, 196]], [[86, 196], [105, 197]], [[105, 197], [124, 194]], [[124, 194], [140, 185]], [[140, 185], [154, 174]], [[154, 174], [165, 158]], [[165, 158], [171, 138]], [[171, 138], [174, 119]], [[174, 119], [175, 98]], [[175, 98], [173, 79]]]
# lineSet5 = [[[29, 81], [30, 100]], [[30, 100], [31, 119]], [[31, 119], [33, 139]], [[33, 139], [38, 158]], [[38, 158], [49, 175]], [[49, 175], [62, 190]], [[62, 190], [80, 202]], [[80, 202], [101, 204]], [[101, 204], [123, 202]], [[123, 202], [140, 190]], [[140, 190], [153, 175]], [[153, 175], [163, 159]], [[163, 159], [169, 140]], [[169, 140], [172, 120]], [[172, 120], [172, 100]], [[172, 100], [172, 81]]]
# lineSet6 = [[[23, 75], [23, 97]], [[23, 97], [25, 118]], [[25, 118], [28, 138]], [[28, 138], [33, 158]], [[33, 158], [44, 177]], [[44, 177], [57, 192]], [[57, 192], [75, 203]], [[75, 203], [96, 204]], [[96, 204], [117, 202]], [[117, 202], [132, 191]], [[132, 191], [143, 176]], [[143, 176], [152, 160]], [[152, 160], [159, 141]], [[159, 141], [164, 123]], [[164, 123], [168, 103]], [[168, 103], [169, 82]]]
# print(lineSet1,lineSet2,lineSet3,sep="\n\n",end="\n\n")
# print(primaryLHD(lineSet1,lineSet1))
# print(lineSet1,lineSet2,lineSet3,sep="\n\n",end="\n\n")
# print(primaryLHD(lineSet1,lineSet3))
# print(lineSet1,lineSet2,lineSet3,sep="\n\n",end="\n\n")
# print(primaryLHD(lineSet2,lineSet3))
# print(lineSet1,lineSet2,lineSet3,sep="\n\n",end="\n\n")
# print(primaryLHD(line1,line2))


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
# 	    color = 'yellow', marker = 'o')


# for l in lineSet3:
# 	plt.plot(
# 	    *zip(*itertools.chain.from_iterable(itertools.combinations(l, 2))),
# 	    color = 'green', marker = 'o')

# plt.show()
# print(primaryLHD(copy.deepcopy(lineSet4),copy.deepcopy(lineSet4)))
# print(primaryLHD(copy.deepcopy(lineSet6),copy.deepcopy(lineSet6)))
