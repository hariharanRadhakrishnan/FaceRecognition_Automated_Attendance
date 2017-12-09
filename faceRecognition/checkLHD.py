from lineHausdorffDistance import newPrimaryLHD
import copy

def convert(s):
	x = s.split(',')
	name = x[-1]
	x = x[:-1]
	l = [[int(x) for x in i.split()] for i in x]
	lineset = []
	for i in range(1,len(l)):
		line = []
		line.append(l[i-1])
		line.append(l[i])
		lineset.append(line)
	lineset.append([l[len(l)-1],l[0]])
	return lineset,name

file = open("../imageDatabase/line_edge_maps2.csv",'r')
f = file.read()
f = f.split('\n')

prevNm = ''
preNm = ''
accu = 0
count = 0
for i in range(len(f)-1):
	li, preNm = convert(f[i])
	x = preNm.split('-')
	x = x[0]
	y = prevNm.split('-')
	y = y[0]
	if(y != x):
		if(count):
			print("Accuracy for ", prevNm , (accu/count) * 100, end="\n\n")
		accu = 0
		count = 0
	prevNm = preNm
	fin = []
	for j in range(len(f)-1):
		if(j != i):
			newData, newNm = convert(f[j]) 
			findDist = primaryLHD(li,newData)
			fin.append([findDist, preNm, newNm])
	if(fin):
		l = min(fin)
		print(l)
		l = fin.index(l)
		if((fin[l][1].split('-'))[0] == (fin[l][2].split('-'))[0]):
			accu += 1
		count += 1