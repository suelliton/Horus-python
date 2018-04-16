# -*- coding: utf-8 -*-
import pyrebase
import time
import cv2
import numpy as np   
from matplotlib import pyplot as plt
from firebase import firebase
fire = firebase.FirebaseApplication('https://horus110886.firebaseio.com/')
config = {
 "apiKey": "AIzaSyA17s6IPxoZ_hfPcJj6Ejh7xmzQcIv1zN4",
  "authDomain": "horus110886.firebaseapp.com",
  "databaseURL": "https://horus110886.firebaseio.com/",
  "storageBucket": "horus110886.appspot.com",
   "serviceAccount":"horus110886-firebase.json"
  
}

firebase = pyrebase.initialize_app(config)

#pegar a referencia para autenticar o servico
auth = firebase.auth()

#logar o usuario pelo email e senha previamente fornecido
user = auth.sign_in_with_email_and_password('tonmelodicmetal@gmail.com', "suelliton")

#pegar a referencia para o banco de dados no firebase
db = firebase.database()
storage = firebase.storage()




def getFoto(numero):	
	print("Baixando foto")
	time.sleep(60)
	try:
		print()
		storage.child("/lisa/lisa"+str(numero-1)+".jpg").download("down_imagem.jpg")			
	except :
		print("Deu erro!!")




def monitorar():
	print("Monitorando...")
	data = db.child("/lisa").get()#pega referencia do firebase
	print(str(data.val()['novaFoto'])) # printa valor da chave 
	count = data.val()['count']#pega contador atual
	#anterior = data.val()['count']#pega contador atual
	


	while True:	
		data = db.child("/lisa").get()#pega referencia do firebase
		print(str(data.val()['count'])) # printa valor da chave 
		count = data.val()['count']#pega contador atual
		existeNova = data.val()['novaFoto']#boobleano de controle	
		if existeNova:
			getFoto(count)
			db.child("/lisa").update({"novaFoto":False})
			getTaxa()

		time.sleep(5)

"""
data = db.child().get()#pega referencia do firebase
#print(str(data.val())) # printa valor da chave 
for child in data.val():
	print(data.val()[child]['count'])#pega o numero do coutn uma por uma do firebase
"""
def getTaxa():

	img = cv2.imread('down_imagem.jpg')
	r = img[:,:,2]
	g = img[:,:,1]
	b = img[:,:,0]
	imT = (g + (455-b))/2
	#print(str(len(img)))
	#print(str(len(img[0]))+ "-x-")
	print("g " +str(g[20][15]))
	print("g " +str(g[2000][1500]))
	print(str(imT[20][15]))
	print(str(imT[2000][1500]))
	#hist = cv2.calcHist([r],[0],None,[256],[0,256])
	#plt.plot(hist)
	#hist = cv2.calcHist([g],[0],None,[256],[0,256])
	#plt.plot(hist)
	#hist = cv2.calcHist([b],[0],None,[256],[0,256])
	#plt.plot(hist)
	plt.show()
	imsaida = np.ones((len(img),len(img[0])),dtype=np.uint8)
	cont = 0#armazena quantidade de pixels da foto atual
	for i in range(0,len(img)):
		for j in range(0,len(img[0])):
			if imT[i][j] > 255 :
				imsaida[i][j] = 255
				cont +=1
			else:
				imsaida[i][j] = 0	
	print("taxa:"+str(cont))

	data = db.child("/lisa").get()
	anterior = data.val()['pixelsAnterior']
	if anterior == 0:#for a primeira foto, nao tem com que comparar entao soarmazena a qtd pixels
		db.child('/lisa').update({"pixelsAnterior":cont})
	else:#calcula opercentual de crescimento em relacao a foto anterios
		taxaPercentual =(cont * 100)/anterior 		
		lista = data.val()['crescimento']['taxaCrescimento']
		lista.append(taxaPercentual)#use rounf(numero,2) pra limitar casas
		db.child("/lisa").child("crescimento").child("taxaCrescimento").set(lista)#adiciona no firebase uma nova porcentagem  
		
		db.child('/lisa').update({"pixelsAnterior":cont})#o valor anterior passa a ser o atual

monitorar()




