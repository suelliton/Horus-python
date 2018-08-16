

import cv2
import numpy as np
import os
import random
import time
#from matplotlib import pyplot as plt




class Pdi(object):
    def __init__(self,database,storage):
        super(Pdi, self).__init__()
        self._database = database
        self._storage = storage


    def getDados(self,experimento):
        print("calculando taxa de crescimento para o experimento "+experimento['nome'] +"...")
        path = experimento['nome']+str(experimento['count']-1)+".jpg"
        img = cv2.imread(path)#leitura de foto que foi baixada
        img = cv2.resize(img,(int(len(img[0])/4),int(len(img)/4)))

        #inclui blur nas imagens
        blurRed, blurGreen = preProcessamento(img,experimento['nome'],experimento['count'])
        limiarRed = calculaLimiar(blurRed,150,"red")
        limiarGreen = calculaLimiar(blurGreen,1000,"green")
        #faz a contagem de pixels das areas de interesse
        redPixels, greenPixels  = calculaPixels(blurRed,blurGreen,limiarRed,limiarGreen,experimento['nome'],experimento['count'])
        geraImagemSaida(experimento)
        #redPixels = random.randint(0,100);
        #greenPixels=random.randint(0,1000);
        print("Fazendo requisição get para experimento "+experimento['nome']+"...")
        try:#calcula taxa de crescimento e area
            experimento = calculaTaxaCrescimento(redPixels, greenPixels,experimento)
            experimento['novaFoto'] = False#avisa que deu certo dizendo ue nao a foto nova
            #faz a remocao de todas as fotos geradas durante o processo para evitar desperdicio de disco
            os.remove(experimento['nome']+str(experimento['count']-1)+".jpg")
            os.remove("blurRed_"+experimento['nome']+str(experimento['count']-1)+"_.jpg")
            os.remove("blurGreen_"+experimento['nome']+str(experimento['count']-1)+"_.jpg")
            os.remove("imsaidaRed_"+experimento['nome']+str(experimento['count']-1)+"_.jpg")
            os.remove("imsaidaGreen_"+experimento['nome']+str(experimento['count']-1)+"_.jpg")
            return experimento#retorna o experimento j´´aatualizado para a classe start

        except Exception as e:
            print("Erro na requisição GET do experimento :(..")
            experimento['novaFoto'] = False
            return experimento


            raise



def geraImagemSaida(experimento):
    time.sleep(2)
    red = cv2.cvtColor(cv2.imread("imsaidaRed_"+experimento['nome']+str(experimento['count']-1)+"_.jpg"), cv2.COLOR_BGR2GRAY)
    green = cv2.cvtColor(cv2.imread("imsaidaGreen_"+experimento['nome']+str(experimento['count']-1)+"_.jpg"), cv2.COLOR_BGR2GRAY)
    imsaidaColorida = np.ones((len(red),len(red[0]),3),dtype=np.uint8)
    for i in range(0,len(red)):
        for j in range(0,len(red[0])):
            if red[i][j] == 255:
                imsaidaColorida[i][j][0] = 0
                imsaidaColorida[i][j][1] = 0
                imsaidaColorida[i][j][2] = 255
            if green[i][j] == 255:
                imsaidaColorida[i][j][0] = 0
                imsaidaColorida[i][j][1] = 255
                imsaidaColorida[i][j][2] = 0
    cv2.imwrite("imsaidaColorida.jpg",imsaidaColorida)


def calculaLimiar(img,pixelsVale,cor):
    hist = cv2.calcHist([np.uint8(img)],[0],None,[256],[0,256])
    maximo = max(hist)
    indice = 0
    for i in range(len(hist)):
    	if hist[i] == maximo:
            indice = i
            break
    corte = 0
    for i in range(indice,len(hist)):
    	if hist[i] < pixelsVale:
    		corte = i
    		break
    if cor == "red":
        print("corte red "+str(corte))
    elif cor =="green":
        print("corte green "+str(corte))
    return corte

def calculaPixels(blurRed, blurGreen,limiarRed,limiarGreen,nomeExperimento, numero):

    imsaidaRed = np.ones((len(blurRed),len(blurRed[0])),dtype=np.uint8)#instancia uma matriz numpy
    redPixels = 0#contador
    for i in range(0,len(blurRed)):
    	for j in range(0,len(blurRed[0])):
    		if blurRed[i][j] > limiarRed :
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
    		if blurGreen[i][j] > limiarGreen :
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

def calculaTaxaCrescimento(redPixels, greenPixels,experimento):

    areaInicial = experimento['crescimento']['areaInicial']

    if redPixels == 0 :
        redPixels = (greenPixels * 4)+1;

    if areaInicial == 0:#for a primeira foto, nao tem com que comparar entao soarmazena a qtd pixels
        areaGreen = (4 * greenPixels) / redPixels#calculo area verde
        print("Area verde total	"+ str(areaGreen))
        experimento['crescimento']['areaInicial'] = round(areaGreen,2)

        lista = []
        lista.append({"dataCaptura":experimento['ultimaCaptura'],"percentualCrescimento":round(0,2),"areaVerde":round(areaGreen,2)})#use rounf(numero,2) pra limitar casas
        experimento['crescimento']['capturas'] = lista

    else:#calcula opercentual de crescimento em relacao a foto anterios
        lista = experimento['crescimento']['capturas']#pega a lista de capturas
        areaGreen = (4 * greenPixels) / redPixels#calcula area verde
        print("Area verde total	"+ str(areaGreen))
        percentualCrescimento = ((areaGreen-areaInicial) * 100)/areaInicial
        print("Taxa de crescimento em percentual é "+str(percentualCrescimento))

        #dataCaptura = data.val()["ultimaCaptura"]#recebe ultima data de captura
        #dataCaptura,horaCaptura = dataCaptura.split("\n")#separa a data da hora
        lista.append({"dataCaptura":experimento['ultimaCaptura'],"percentualCrescimento":round(percentualCrescimento,2),"areaVerde":round(areaGreen,2)})#use rounf(numero,2) pra limitar casas
        experimento['crescimento']['capturas'] = lista
                #database.child(nomeExperimento).child("crescimento").child("capturas").set(lista)#adiciona no firebase uma nova porcentagem

    return experimento
