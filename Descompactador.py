import os, sys, math,Arquivo, re

class Descompactador:
    
    tamanhoLista = -1 # guarda o tamanho da lista
    tamanhoRrn = 0 # guarda a quantidade de palavras para substituição

    leitura = None # guarda o ponteiro do arquivo de leitura
    gravacao = None # guarda o ponteiro do arquivo de gravação

    
    # retorna o tamanho da lista
    def getTamanhoLista(self):
        return self.tamanhoLista


    # faz a leitura do arquivo
    def setTamanhoLista(self,texto):
        self.tamanhoLista = int.from_bytes(texto,Arquivo.BYTEORDER)
        return self.tamanhoLista


    # gera a lista
    def lista(self,texto):

        # pega o tamanho da lista
        tamanho = self.getTamanhoLista()

        virgulas = 0
        posicaoFinal = 0

        # 
        for i in range(0,len(texto)):
            
            if texto[i].to_bytes(1,Arquivo.BYTEORDER).decode(Arquivo.CODIFICACAO) == ",": 
                virgulas += 1   
                
                if(virgulas == tamanho):
                    posicaoFinal = i
                    break
                
            
        self.tamanhoRrn = posicaoFinal

        lista = texto[0:posicaoFinal].decode(Arquivo.CODIFICACAO).split(",")
        return lista


    # gera o texto final        
    def textoFinal(self,texto,lista):

        for i in range(0,len(lista)):

            texto = texto.replace(
                (255).to_bytes(1,Arquivo.BYTEORDER)+(i).to_bytes(2,Arquivo.BYTEORDER),
                lista[i].encode(),
                
            )
        
        return texto

    # descompacta o arquivo
    def descompactar(self):

        #lê o texto e o processa
        texto = self.leitura.leitura(self.leitura.getTamanho())
        self.setTamanhoLista(texto[0:2])
        lista = self.lista(texto[2:len(texto)])
        
        tamanho = self.tamanhoRrn + 3
        texto = self.textoFinal(texto[tamanho:len(texto)],lista)

        # grava
        self.gravacao.gravacao(texto)




    def __init__(self,leitura,gravacao):
        self.gravacao = gravacao
        self.leitura = leitura