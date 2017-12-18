import lineHausdorffDistance as LHD
import cv2
import copy

def get_delaunay_lineset(points, shapeX, shapeY) :
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
	return veronoiLEM

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

def convertString(s):
	x = s.split(',')
	name = x[-1]
	x = x[:-1]
	l = [[int(x) for x in i.split()] for i in x]
	lineset = addFullCurve(l)
	# lineset = buildLineset(l)
	# lineset = get_delaunay_lineset(l,220,220)
	return lineset,name

def convertToLineSet(s):
	lineset = addFullCurve(s)
	# lineset = buildLineset(s)
	# lineset = get_delaunay_lineset(s,220,220)
	return lineset

def run(newData , tp="normal"):
	if(tp == "normal"):
		newData = convertToLineSet(newData)
		# print("Test :: ")
		# print(newData)
		# print(len(newData),end=' ,')
		file = open("../imageDatabase/line_edge_maps2.csv",'r')
		f = file.read()
		f = f.split('\n')
		fin = []
		for i in range(len(f)-1):
			li, name = convertString(f[i])
			# print(name + ' ::')
			# print(li)
			# print(len(li))
			findDist = LHD.newPrimaryLHD(li,newData)
			fin.append([findDist, name])
		return fin , min(fin)