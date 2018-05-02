# -*- coding: utf-8 -*-
import pyrebase
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt

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

def getFoto(numero,nomeExperimento):
    print("Baixando foto")
    time.sleep(80)
    try:
        print(nomeExperimento)
        print(str(numero))
        storage.child("/"+nomeExperimento+"/"+nomeExperimento+str(numero-1)+".jpg").download("down_imagem.jpg")
    except :
        print("Deu erro!!")




def monitorar():
	print("Monitorando...")
	#data = db.child("/lisa").get()#pega referencia do firebase
	#print(str(data.val()['novaFoto'])) # printa valor da chave
	#count = data.val()['count']#pega contador atual
	#anterior = data.val()['count']#pega contador
	while True:
         #pega referencia do firebase
         data = db.child().get()
        # print(str(data.val()))
         for nomeExperimento in data.val():
             experimento = db.child(nomeExperimento).get()
             print(str(experimento.val()))
             print(str(experimento.val()['count'])) # printa valor da chave
             count = experimento.val()['count']#pega contador atual
             existeNova = experimento.val()['novaFoto']#boobleano de controle
             if existeNova:
                 getFoto(count,experimento.val()["nome"])
                 db.child(experimento.val()["nome"]).update({"novaFoto":False})
                 getTaxa(experimento.val()["nome"])
         time.sleep(5)

"""
data = db.child().get()#pega referencia do firebase
#print(str(data.val())) # printa valor da chave
for child in data.val():
	print(data.val()[child]['count'])#pega o numero do coutn uma por uma do firebase
"""
def getTaxa(nomeExperimento):
    print("calculando taxa de crescimento para o experimento "+nomeExperimento +"...")
    img = cv2.imread('down_imagem.jpg')

    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]
    imT = ((g) + (455-(b)))/4
    blur = cv2.blur(imT,(3,3))
    blur = cv2.blur(blur,(3,3))
    cv2.imwrite("blur.jpg",blur)
    blur = np.uint8(cv2.imread("blur.jpg"))
    imsaida = np.ones((len(img),len(img[0])),dtype=np.uint8)#inicializa uma nova imagem com numeros 1
    cont = 0#armazena quantidade de pixels da foto atual
    for i in range(0,len(img)):
        for j in range(0,len(img[0])):
            if blur[i][j][1] > 121 :
                imsaida[i][j] = 255
                cont +=1
            else:
                imsaida[i][j] = 0

    cv2.imwrite("imsaida.jpg",imsaida)
    print("taxa de crescimento em pixels:"+str(cont))
    print("Calculando taxa de crescimento em percentual...")
    print("Fazendo requisição get para experimento "+nomeExperimento+"...")
    try:
        data = db.child(nomeExperimento).get()
        print("Requisição feita com sucesso!...")
        anterior = data.val()['crescimento']['pixelsAnterior']
        print("Pixels anterior "+str(anterior))
        if anterior == 0:#for a primeira foto, nao tem com que comparar entao soarmazena a qtd pixels
            db.child(nomeExperimento).child("crescimento").update({"pixelsAnterior":cont})
        else:#calcula opercentual de crescimento em relacao a foto anterios
            taxaPercentual = (cont * 100)/anterior
            print("Taxa de crescimento em percentual é "+str(taxaPercentual))
            lista = data.val()['crescimento']['taxaCrescimento']
            lista.append(round(taxaPercentual,2))#use rounf(numero,2) pra limitar casas
            db.child(nomeExperimento).child("crescimento").child("taxaCrescimento").set(lista)#adiciona no firebase uma nova porcentagem
            db.child(nomeExperimento).child("crescimento").update({"pixelsAnterior":cont})#o valor anterior passa a ser o atual
    except Exception as e:
        print("Erro na requisição GET do experimento :(..")
        raise

monitorar()
