

import cv2
import numpy as np
import os
#from matplotlib import pyplot as plt




class Pdi(object):
    def __init__(self,database,storage):
        super(Pdi, self).__init__()
        self._database = database
        self._storage = storage





    def getDados(self,nomeExperimento,numero):
        print("calculando taxa de crescimento para o experimento "+nomeExperimento +"...")

        img = cv2.imread(nomeExperimento+str(numero-1)+".jpg")

        blurRed, blurGreen = preProcessamento(img,nomeExperimento,numero)

        redPixels, greenPixels  = calculaPixels(blurRed,blurGreen,nomeExperimento,numero)

        print("Fazendo requisição get para experimento "+nomeExperimento+"...")
        try:
            calculaTaxaCrescimento(redPixels, greenPixels,self._database,nomeExperimento)
            self._database.child(nomeExperimento).update({"novaFoto":False})

        except Exception as e:
            print("Erro na requisição GET do experimento :(..")
            self._database.child(nomeExperimento).update({"novaFoto":True})#se nao der certo ele deixa como esta
            raise
        os.remove(nomeExperimento+str(numero-1)+".jpg")
        os.remove("blurRed_"+nomeExperimento+str(numero-1)+"_.jpg")
        os.remove("blurGreen_"+nomeExperimento+str(numero-1)+"_.jpg")
        os.remove("imsaidaRed_"+nomeExperimento+str(numero-1)+"_.jpg")
        os.remove("imsaidaGreen_"+nomeExperimento+str(numero-1)+"_.jpg")


def calculaPixels(blurRed, blurGreen, nomeExperimento, numero):

    imsaidaRed = np.ones((len(blurRed),len(blurRed[0])),dtype=np.uint8)
    redPixels = 0
    for i in range(0,len(blurRed)):
    	for j in range(0,len(blurRed[0])):
    		if blurRed[i][j] > 130 :
    			imsaidaRed[i][j] = 255
    			redPixels +=1
    		else:
    			imsaidaRed[i][j] = 0
    print("Pixels Red:"+str(redPixels))
    cv2.imwrite("imsaidaRed_"+nomeExperimento+str(numero-1)+"_.jpg",imsaidaRed)

    ######
    imsaidaGreen = np.ones((len(blurGreen),len(blurGreen[0])),dtype=np.uint8)
    greenPixels = 0
    for i in range(0,len(blurGreen)):
    	for j in range(0,len(blurGreen[0])):
    		if blurGreen[i][j] > 120 :
    			imsaidaGreen[i][j] = 255
    			greenPixels +=1
    		else:
    			imsaidaGreen[i][j] = 0
    print("Pixels Green:"+str(greenPixels))
    cv2.imwrite("imsaidaGreen_"+nomeExperimento+str(numero-1)+"_.jpg",imsaidaGreen)

    return redPixels, greenPixels



def preProcessamento(img,nomeExperimento,numero):
    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]

#####
    imCinzaRed =  ((r) + (455-(g)))/4
    #imCinzaRed =  ((2*r) - (b) - (g))/2
    blurRed = cv2.blur(imCinzaRed,(3,3))
    blurRed = cv2.blur(blurRed,(3,3))
    cv2.imwrite("blurRed.jpg",blurRed)
    blurRed = cv2.cvtColor(cv2.imread("blurRed.jpg"), cv2.COLOR_BGR2GRAY)

    imCinzaGreen =  (g + (455 - (b))) /4
    blurGreen = cv2.blur(imCinzaGreen,(3,3))
    blurGreen = cv2.blur(blurGreen,(3,3))
    cv2.imwrite("blurGreen.jpg",blurGreen)
    blurGreen = cv2.cvtColor(cv2.imread("blurGreen.jpg"), cv2.COLOR_BGR2GRAY)

#####

    cv2.imwrite("blurRed_"+nomeExperimento+str(numero-1)+"_.jpg",blurRed)
    cv2.imwrite("blurGreen_"+nomeExperimento+str(numero-1)+"_.jpg",blurGreen)
    #blur = np.uint8(cv2.imread("blur_"+nomeExperimento+str(numero-1)+"_.jpg"))
    return blurRed, blurGreen

def calculaTaxaCrescimento(redPixels, greenPixels, database, nomeExperimento):
    data = database.child(nomeExperimento).get()
    print("Requisição feita com sucesso!...")
    areaInicial = data.val()['crescimento']['areaInicial']
    #print("Pixels primeira foto "+str(pixelsFotoInicial))
    if redPixels == 0 :
        redPixels = greenPixels * 4;

    if areaInicial == 0:#for a primeira foto, nao tem com que comparar entao soarmazena a qtd pixels
        lista = []#pega a lista de capturas
        areaGreen = (4 * greenPixels) / redPixels#calculo area verde
        database.child(nomeExperimento).child("crescimento").update({"areaInicial":round(areaGreen,2)})
        print("Area verde total	"+ str(areaGreen))
        dataCaptura = data.val()["ultimaCaptura"]#recebe ultima data de captura
        dataCaptura,horaCaptura = dataCaptura.split("\n")#separa a data da hora
        lista.append({"dataCaptura":dataCaptura,"percentualCrescimento":round(0,2),"areaVerde":round(areaGreen,2)})#use rounf(numero,2) pra limitar casas
        database.child(nomeExperimento).child("crescimento").child("capturas").set(lista)#adiciona no firebase uma nova porcentagem

    else:#calcula opercentual de crescimento em relacao a foto anterios
        lista = data.val()['crescimento']['capturas']#pega a lista de capturas
        areaGreen = (4 * greenPixels) / redPixels#calcula area verde
        print("Area verde total	"+ str(areaGreen))
        percentualCrescimento = ((areaGreen-areaInicial) * 100)/areaInicial
        print("Taxa de crescimento em percentual é "+str(percentualCrescimento))

        dataCaptura = data.val()["ultimaCaptura"]#recebe ultima data de captura
        dataCaptura,horaCaptura = dataCaptura.split("\n")#separa a data da hora
        lista.append({"dataCaptura":dataCaptura,"percentualCrescimento":round(percentualCrescimento,2),"areaVerde":round(areaGreen,2)})#use rounf(numero,2) pra limitar casas
        database.child(nomeExperimento).child("crescimento").child("capturas").set(lista)#adiciona no firebase uma nova porcentagem

        #db.child(nomeExperimento).child("crescimento").update({"pixelsAnterior":cont})#o valor anterior passa a ser o atual

    #calculo e envio de areaVerde
