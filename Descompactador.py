import os, sys, math,Arquivo, re

class Descompactador:
    
    tamanhoLista = -1
    tamanhoRrn = 0

    leitura = None
    gravacao = None

    

    def getTamanhoLista(self):
        return self.tamanhoLista


    def setTamanhoLista(self,texto):
        self.tamanhoLista = int.from_bytes(texto,Arquivo.BYTEORDER)
        return self.tamanhoLista


    def lista(self,texto):
        tamanho = self.getTamanhoLista()

        virgulas = 0
        posicaoFinal = 0

        #print(texto)

        for i in range(0,len(texto)):
            
            if texto[i].to_bytes(1,'big').decode('ascii') == ",": 
                virgulas += 1   
                
                if(virgulas == tamanho):
                    posicaoFinal = i
                    break
                
            
        self.tamanhoRrn = posicaoFinal

        lista = texto[0:posicaoFinal].decode('ascii').split(",")
        return lista

        
    def textoFinal(self,texto,lista):

        for i in range(0,len(lista)):

            texto = texto.replace(
                (255).to_bytes(1,'big')+(i).to_bytes(2,'big'),
                lista[i].encode(),
                
            )
        
        return texto

    def descompactar(self):
        texto = self.leitura.leitura(self.leitura.getTamanho())
        self.setTamanhoLista(texto[0:2])
        lista = self.lista(texto[2:len(texto)])
        
        tamanho = self.tamanhoRrn + 3
        texto = self.textoFinal(texto[tamanho:len(texto)],lista)

        self.gravacao.gravacao(texto)




    def __init__(self,leitura,gravacao):
        self.gravacao = gravacao
        self.leitura = leitura


caminho = 'testGrande.txt.cmp'
Descompactador(Arquivo.Arquivo(caminho,"rb"),Arquivo.Arquivo(caminho+".txt.old","wb")).descompactar()

