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
	# l = [[int(x) for x in i.split()] for i in s.split(',')]
	# lineset = buildLineset(l)
	l=s
	lineset = addFullCurve(l)
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

def sortLine(line):
	x_diff = line[0][0] - line[1][0]
	y_diff = line[0][1] - line[1][1]
	lineSwap = False
	if(x_diff > 0):
		lineSwap = True
	elif(x_diff == 0):
		if(y_diff < 0):
			lineSwap = True
	if(lineSwap):
		return line[::-1]
	return line

def rotate(line1, length, angle):
	if(angle == 0.0):
		return line1
	midPointX = (line1[0][0] + line1[1][0])/2
	midPointY = (line1[0][1] + line1[1][1])/2
	
	line1[0][0] = line1[0][0] - midPointX
	line1[1][0] = line1[1][0] - midPointX
	line1[0][1] = line1[0][1] - midPointY
	line1[1][1] = line1[1][1] - midPointY

	slope1 = getSlope(line1[1][0]-line1[0][0],line1[1][1]-line1[0][1])

	newAngle = slope1 + angle
	newX2 = length/2 * math.cos(newAngle)
	newY2 = length/2 * math.sin(newAngle)
	newX1 = length/2 * math.cos(math.pi + newAngle)
	newY1 = length/2 * math.sin(math.pi + newAngle)

	return [[newX1 + midPointX,newY1 + midPointY],[newX2 + midPointX,newY2 + midPointY]]

def findAngleDiff(line1,line2):
	# print(line1,line2)
	slope1 = getSlope(line1[1][0]-line1[0][0],line1[1][1]-line1[0][1])
	slope2 = getSlope(line2[1][0]-line2[0][0],line2[1][1]-line2[0][1])
	# print(math.degrees(slope1),math.degrees(slope2))
	angleDiff = slope2 - slope1
	return angleDiff

def LHD(line1,line2):
	# print(line1, line2)
	line11 = copy.deepcopy(line1)
	line21 = copy.deepcopy(line2)
	line1 = copy.deepcopy(line1)
	line2 = copy.deepcopy(line2)
	angleDiff = findAngleDiff(line1,line2)
	# print("angleDiff :: ", math.degrees(angleDiff))
	line1 = sortLine(line1)
	line2 = sortLine(line2)	
	
	vec1Len = dist(line1[0],line1[1])
	vec2Len = dist(line2[0],line2[1])
	# print("Before :: ",line1,line2,vec1Len,vec2Len)
	if(vec1Len < vec2Len):
		# print("Path 1")
		line1 = rotate(line1, vec1Len, angleDiff)
	else:
		# print("Path 2")
		line2 = rotate(line2, vec2Len, -angleDiff)
	# print("\tAfter :: ",line1,line2,end=" ")
	# print("Angle Difference :: ", math.degrees(int(findAngleDiff(line1,line2))),end = " ")
	# if(int(findAngleDiff(line1,line2)) != 0):
	# 	print(line11,line21,math.degrees(findAngleDiff(line1,line2)))
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
	value = (penalty(angleDiff)**2 + perDist**2 + parDist**2 )**0.5
	# print("LHD :: ", value)
	return value
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
		LHDSum += line1Len * max(l)
	if(p):
		print("______________________________________________________________________________________")
	return LHDSum/totalLength

def primaryLHD(lineSet1,lineSet2):
	set1 = LHD_set_lines(lineSet1,lineSet2)
	set2 = LHD_set_lines(lineSet2,lineSet1)
	# print("LHD_values",set1,set2)
	return max(set1,set2)

def newLHD(lineSet1,lineSet2,p=False,search=1):
	LHDSum = 0
	totalLength = 0
	run_len = min(len(lineSet1),len(lineSet2))
	for i in range(run_len):
		line1 = lineSet1[i]
		line1Len = dist(line1[0],line1[1])
		totalLength += line1Len
		boundary1=(i-search//2)
		boundary2=(i+search//2)+1
		LHDval = []
		for j in range(boundary1,boundary2):
			if(j < 0):
				continue
			if(j > len(lineSet2)-1):
				break
			line2 = lineSet2[j]			
			LHDval.append(LHD(line1,line2))
		LHDSum += line1Len * min(LHDval)		
		if(p):
			print(i, line1, line2, LHDval, LHDSum/totalLength)
	return LHDSum/totalLength

def newPrimaryLHD(lineSet1,lineSet2,search=1):

	set1 = newLHD(lineSet1,lineSet2,search=search)
	set2 = newLHD(lineSet2,lineSet1,search=search)
		
	
	return max(set1,set2)
	

# a = [[1,1],[-1,-1]]
# print(dist(a[0],a[1]))
# degrees = -45
# b = rotate(a,dist(a[0],a[1]),math.radians(degrees))
# print(b)
# print(dist(b[0],b[1]))

# print(math.degrees(findAngleDiff(a,b)))

 
# lineSet1 = addFullCurve(eval(input()))
# lineSet2 = convert(input())

# print(newPrimaryLHD(lineSet1,lineSet2))
# # # print(primaryLHD(lineSet1,lineSet2))

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

# # for l in lineSet3:
# # 	plt.plot(
# # 	    *zip(*itertools.chain.from_iterable(itertools.combinations(l, 2))),
# # 	    color = 'green', marker = 'o')

# plt.show()
