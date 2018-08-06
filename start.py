# -*- coding: utf-8 -*-
import time
from autentica import Autentica
from pdi import Pdi
import threading




def main():
    autenticar = Autentica("AIzaSyA17s6IPxoZ_hfPcJj6Ejh7xmzQcIv1zN4","horus110886.firebaseapp.com","https://horus110886.firebaseio.com/","horus110886.appspot.com","horus110886-firebase.json","tonmelodicmetal@gmail.com","suelliton")
    database,storage = autenticar.logar()
    if database and storage:
        print("Usuario logado, banco e storage disponiveis")
    else:
        print("Erro no login")
    pdiOb = Pdi(database,storage)
    monitorar(database,storage,pdiOb)



def getFoto(numero,nomeExperimento,storage):
    print("Baixando foto")
    #time.sleep(80)
    try:
        print(nomeExperimento)
        print(str(numero))
        storage.child("/"+nomeExperimento+"/"+nomeExperimento+str(numero-1)+".jpg").download(nomeExperimento+str(numero-1)+".jpg")
    except :
        print("Deu erro!!")


def monitorar(database,storage,pdiOb):

    while True:
        print("Monitorando...")
         #pega referencia do firebase
        data = database.child().get()
        # print(str(data.val()))
        if data.val() != None :
            for nomeExperimento in data.val():
                 experimento = database.child(nomeExperimento).get()
                 #print(str(experimento.val()))
                 #print(str(experimento.val()['count'])) # printa valor da chave
                 count = experimento.val()['count']#pega contador atual
                 existeNova = experimento.val()['novaFoto']#boobleano de controle
                 if existeNova:
                     rotina(experimento.val()["nome"],count,database,storage,pdiOb)
        time.sleep(25)

def rotina(nomeExperimento,count,database,storage,pdiOb):
    print("Thread "+ nomeExperimento+" iniciada")
    getFoto(count,nomeExperimento,storage)
    #database.child(nomeExperimento).update({"novaFoto":False})
    pdiOb.getDados(nomeExperimento,count)
    print("Thread "+ nomeExperimento+" morreu")





if __name__ == '__main__':
    main()
