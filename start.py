# -*- coding: utf-8 -*-
import time
from autentica import Autentica
from pdi import Pdi



def main():
    autenticar = Autentica("AIzaSyA17s6IPxoZ_hfPcJj6Ejh7xmzQcIv1zN4","horus110886.firebaseapp.com","https://horus110886.firebaseio.com/","horus110886.appspot.com","horus110886-firebase.json","tonmelodicmetal@gmail.com","suelliton")
    database,storage = autenticar.logar()
    if database and storage:
        print("Usuario logado, banco e storage disponiveis")
    else:
        print("Erro no login")
    pdiOb = Pdi(database,storage)
    monitorar(database,storage,pdiOb)

def monitorar(database,storage,pdiOb):
	print("Monitorando...")
	while True:
         #pega referencia do firebase
         data = database.child().get()
        # print(str(data.val()))
         for nomeExperimento in data.val():
             experimento = database.child(nomeExperimento).get()
             print(str(experimento.val()))
             print(str(experimento.val()['count'])) # printa valor da chave
             count = experimento.val()['count']#pega contador atual
             existeNova = experimento.val()['novaFoto']#boobleano de controle
             if existeNova:
                 #getFoto(count,experimento.val()["nome"])
                 database.child(experimento.val()["nome"]).update({"novaFoto":False})
                 pdiOb.getTaxa(experimento.val()["nome"])
         time.sleep(5)







if __name__ == '__main__':
    main()
