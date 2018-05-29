

import cv2
import numpy as np
import os
#from matplotlib import pyplot as plt




class Pdi(object):
    def __init__(self,database,storage):
        super(Pdi, self).__init__()
        self._database = database
        self._storage = storage
        




    def getTaxa(self,nomeExperimento,numero):
        print("calculando taxa de crescimento para o experimento "+nomeExperimento +"...")

        img = cv2.imread(nomeExperimento+str(numero-1)+".jpg")

        imBlur = preProcessamento(img,nomeExperimento,numero)

        totalPixels = calculaPixels(imBlur,nomeExperimento,numero)

        print("taxa de crescimento em pixels:"+str(totalPixels))
        print("Calculando taxa de crescimento em percentual...")
        print("Fazendo requisição get para experimento "+nomeExperimento+"...")
        try:
            calculaTaxaCrescimento(totalPixels,self._database,nomeExperimento)
        except Exception as e:
            print("Erro na requisição GET do experimento :(..")
            raise
        os.remove(nomeExperimento+str(numero-1)+".jpg")
        os.remove("blur_"+nomeExperimento+str(numero-1)+"_.jpg")
        os.remove("imsaida_"+nomeExperimento+str(numero-1)+"_.jpg")


def calculaPixels(imBlur,nomeExperimento,numero):
    imsaida = np.ones((len(imBlur),len(imBlur[0])),dtype=np.uint8)#inicializa uma nova imagem com numeros 1
    cont = 0#armazena quantidade de pixels da foto atual
    for i in range(0,len(imBlur)):
        for j in range(0,len(imBlur[0])):
            if imBlur[i][j][1] > 121 :
                imsaida[i][j] = 255
                cont +=1
            else:
                imsaida[i][j] = 0
    cv2.imwrite("imsaida_"+nomeExperimento+str(numero-1)+"_.jpg",imsaida)
    return cont
def preProcessamento(img,nomeExperimento,numero):
    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]
    imTemp = ((g) + (455-(b)))/4
    blur = cv2.blur(imTemp,(3,3))
    blur = cv2.blur(blur,(3,3))
    cv2.imwrite("blur_"+nomeExperimento+str(numero-1)+"_.jpg",blur)
    blur = np.uint8(cv2.imread("blur_"+nomeExperimento+str(numero-1)+"_.jpg"))
    return blur

def calculaTaxaCrescimento(totalPixels,database,nomeExperimento):
    data = database.child(nomeExperimento).get()
    print("Requisição feita com sucesso!...")
    pixelsFotoInicial = data.val()['crescimento']['pixelsFotoInicial']
    print("Pixels primeira foto "+str(pixelsFotoInicial))
    if pixelsFotoInicial == 0:#for a primeira foto, nao tem com que comparar entao soarmazena a qtd pixels
        database.child(nomeExperimento).child("crescimento").update({"pixelsFotoInicial":totalPixels})
    else:#calcula opercentual de crescimento em relacao a foto anterios
        taxaPercentual = ((totalPixels-pixelsFotoInicial) * 100)/pixelsFotoInicial
        print("Taxa de crescimento em percentual é "+str(taxaPercentual))
        lista = data.val()['crescimento']['capturas']#pega a lista de capturas
        dataCaptura = data.val()["ultimaCaptura"]#recebe ultima data de captura
        dataCaptura,horaCaptura = dataCaptura.split("\n")#separa a data da hora
        lista.append({"dataCaptura":dataCaptura,"taxaCrescimento":round(taxaPercentual,2)})#use rounf(numero,2) pra limitar casas
        database.child(nomeExperimento).child("crescimento").child("capturas").set(lista)#adiciona no firebase uma nova porcentagem
        #db.child(nomeExperimento).child("crescimento").update({"pixelsAnterior":cont})#o valor anterior passa a ser o atual
