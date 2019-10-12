import os, sys, math

TAMANHOBUFFER = 4096
BYTEORDER = 'big'

class Arquivo:

    apontador = 0
    arquivo = None
    caminho = ''
    tamanho = 0
    posicao = 0
    

    # retorna o tamanho do arquivo
    def getTamanho(self):
        self.tamanho = os.path.getsize(self.caminho)
        return self.tamanho

    def ponteiro(self):
        self.posicao = self.arquivo.tell()
        return self.posicao

    # Trata a leitura do arquivo
    def leitura(self,tamanho):
        
        if os.path.isfile(self.caminho):

            dados = self.arquivo.read(tamanho)
            
            return dados
        else:
            return None


    # Realiza a gravação de um arquivo
    def gravacao(self,dados):
        self.arquivo.write(dados)
        
    def seek(self,posicao,tipo):
        self.arquivo.seek(posicao,tipo)

    def close(self):
        self.arquivo.close()
        

    def __init__(self,caminho,modo):
        self.caminho = caminho
        self.modo = modo

        self.arquivo = open(self.caminho, modo)
        