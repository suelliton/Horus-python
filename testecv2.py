
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
nomeFoto = "imagens/alface0205 (2).jpg"
img = cv2.imread(nomeFoto)

r = img[:,:,2]
g = img[:,:,1]
b = img[:,:,0]

imT = ((g) + (455-(b)))/4
blur = cv2.blur(imT,(3,3))
blur = cv2.blur(blur,(3,3))
cv2.imwrite("blur.jpg",blur)
blur = np.uint8(cv2.imread("blur.jpg"))


height, width = blur.shape[:2]
imResize = cv2.resize(blur,(412,310), interpolation = cv2.INTER_AREA)
cv2.imwrite("imResize_.jpg",imResize)
plt.imshow(imResize,'gray')
plt.show()


hist = cv2.calcHist([blur],[0],None,[256],[0,256])
plt.plot(hist)
plt.show()


##limiar, imgLimiar = cv2.threshold(g,127,255,cv2.THRESH_BINARY)
##plt.imshow(imgLimiar,'gray')
##plt.show()

imsaida = np.ones((len(imResize),len(imResize[0])),dtype=np.uint8)
cont = 0
for i in range(0,len(imResize)):
	for j in range(0,len(imResize[0])):
		if imResize[i][j][1] > 121 :
			imsaida[i][j] = 255
			cont +=1
		else:
			imsaida[i][j] = 0
print("taxa:"+str(cont))
cv2.imwrite("saida_"+nomeFoto+".jpg",imsaida)
plt.imshow(imsaida,'gray')
plt.show()
