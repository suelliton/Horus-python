# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
nomeFoto = "azul3.jpg"
img = cv2.imread(nomeFoto)
imBlur = cv2.blur(img,(5,5))


r = imBlur[:,:,2]
g = imBlur[:,:,1]
b = imBlur[:,:,0]


imR = ((g) + (455-(b)))/4
imT = (b) + (255 -r)
imTemp = b - imR - r

minimo = min(imTemp[0])
print(str(minimo))
maximo = max(imTemp[0])
print(str(maximo))
imTemp = imTemp + abs(minimo)
for i in range(0,len(img)):
	for j in range(0,len(img[0])):
		if(imTemp[i][j] < 0):
			imTemp[i][j] = 0

imTemp = np.uint8(imTemp)
"""

hist = cv2.calcHist(b,[0],None,[256],[0,256])
plt.plot(hist)
plt.show()
plt.imshow(imTemp,'gray')
plt.show()
plt.imshow(r,'gray')
plt.show()
plt.imshow(g,'gray')
plt.show()
plt.imshow(b,'gray')
plt.show()"""


"""


limiar, imgLimiar = cv2.threshold(imTemp,0,255,cv2.THRESH_BINARY)
plt.imshow(imgLimiar,'gray')
plt.show()"""


imsaida = np.ones((len(img),len(img[0])),dtype=np.uint8)
cont = 0
for i in range(0,len(img)):
	for j in range(0,len(img[0])):
		if imTemp[i][j] > 80 :
			imsaida[i][j] = 255
			cont +=1
		else:
			imsaida[i][j] = 0
print("taxa:"+str(cont))
print("tamanho : "+str(len(imsaida)))
cv2.imwrite("saida.jpg",imsaida)
plt.imshow(imsaida,'gray')
plt.show()
