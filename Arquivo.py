import os, sys, math

TAMANHOBUFFER = 4096
BYTEORDER = 'big'
CODIFICACAO = 'ascii'

'''

    Classe para manipulação de arquivo

'''

class Arquivo:

    apontador = 0
    arquivo = None
    caminho = ''
    tamanho = 0
    posicao = 0
    

    # retorna o tamanho do arquivo
    def getTamanho(self):
        
        # retorna do s.o o tamanho do arquivo
        self.tamanho = os.path.getsize(self.caminho)
        return self.tamanho

    # retorna a posição do ponteiro do arquivo
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

    
    # muda o ponteiro de posição        
    def seek(self,posicao,tipo):
        self.arquivo.seek(posicao,tipo)

    # fecha o arquivo
    def close(self):
        self.arquivo.close()
        
    # metodo construtor que abrirá o arquivo
    def __init__(self,caminho,modo):
        self.caminho = caminho
        self.modo = modo

        # tenta abrir o arquivo
        try:
            self.arquivo = open(self.caminho, modo)
        except:
            print("Falha ao abrir arquivo!")
            sys.exit(1)
        