def convert(s):
	s = s.split(",")
	s = [[int(x) for x in i.split()] for i in s]
	lineSet = []
	for i in range(1,len(s)):
		lineSet.append([s[i-1],s[i]])
	return lineSet

print(convert(input()))