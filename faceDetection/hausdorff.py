sandeep_1 = [[51 ,84],
 [59 ,80],
 [68 ,79],
 [77 ,83],
 [68 ,87],
 [58 ,88]]

sandeep_2 = [[52 ,84],
 [60 ,78],
 [70 ,78],
 [79 ,83],
 [70 ,86],
 [60 ,87]]

sandeep_tilted = [[44 ,87],
 [52 ,82],
 [64 ,80],
 [74 ,82],
 [65 ,88],
 [54 ,91]]

sandeep_skewed = [[59 ,78],
 [63 ,74],
 [71 ,74],
 [77 ,79],
 [70 ,82],
 [63 ,82]]

other1 = [[53 ,84],
 [61 ,79],
 [71 ,78],
 [82 ,82],
 [72 ,85],
 [62 ,86]]

other2 = [[53 ,74],
 [62 ,73],
 [72 ,74],
 [80 ,79],
 [70 ,79],
 [60 ,78]]


def dist(a,b):
	return ( (a[0]-b[0])**2 + (a[1]-b[1])**2)*(1/2.0)

def hausdrauff(set_a,set_b):
	hausdrauff_dist_a = 0
	hausdrauff_pts_a=[]
	for a in set_a:
		min_d = 9999
		min_pts = []
		for b in set_b:
			distance = dist(a,b)
			if(distance<min_d):
				min_d=distance
				min_pts=a,b
		if(min_d>hausdrauff_dist_a):
			hausdrauff_dist_a=min_d
			hausdrauff_pts_a=min_pts

	hausdrauff_dist_b = 0
	hausdrauff_pts_b=[]
	for b in set_b:
		min_d = 9999
		min_pts = []
		for a in set_a:
			distance = dist(b,a)
			if(distance<min_d):
				min_d=distance
				min_pts=b,a
		if(min_d>hausdrauff_dist_b):
			hausdrauff_dist_b=min_d
			hausdrauff_pts_b=min_pts

	return  [hausdrauff_dist_a,hausdrauff_dist_b] ,  hausdrauff_pts_a,hausdrauff_pts_b 

print('sandeep_1:sandeep_2')
print(hausdrauff(sandeep_1,sandeep_2))

print()

print('sandeep_1:sandeep_tilted')
print(hausdrauff(sandeep_1,sandeep_tilted))

print()

print('sandeep_1:sandeep_skewed')
print(hausdrauff(sandeep_1,sandeep_skewed))

print()

print('sandeep_1:other1')
print(hausdrauff(sandeep_1,other1))

print()

print('sandeep_1:other2')
print(hausdrauff(sandeep_1,other2))

