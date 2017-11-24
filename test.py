import cv2
import numpy as np

img = cv2.imread('images/Test/Hari.jpg',cv2.IMREAD_UNCHANGED)
print(np.shape(img))

# for i in img:
# 	for j in i:
# 		R,G,B = j
# 		if(not(R>95 and G>40 and B > 20 and R > G and R > B and abs(R - G) > 15)):
# 			j=[0,0,0]

for i in img[0]:
	print(i)
# 		print(j)
# 	print("AAHAHAHAHA")
# print(img[0][0])
# for i in img[0]:
# 	print(i)

# R > 95 and G > 40 and B > 20 and R > G and R > B
# and | R - G | > 15 and A > 15 and Cr > 135 and
# Cb > 85 and Y > 80 and Cr <= (1.5862*Cb)+20 and
# Cr>=(0.3448*Cb)+76.2069 and
# Cr >= (-4.5652*Cb)+234.5652 and
# Cr <= (-1.15*Cb)+301.75 and
# Cr <= (-2.2857*Cb)+432.85