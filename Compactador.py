import os, sys, math,Arquivo, re

class Compactador:

    leitura = None
    gravacao = None


    rrn = []
    
    tamanho = 0

    def ordenacaoLista(self,lista):
        # faz a ordenação decrescente

        for i in range(0,len(lista)):
            for j in range(0,i):
                if len(lista[i]) > len(lista[j]):
                    temp = lista[i]
                    lista[i] = lista[j]
                    lista[j] = temp

        return lista

    def tirarRepeticao(self,quebrar):
        lista = []

        # varre todos os elementos
        for i in range(len(quebrar)-1,-1,-1):

            repetido = False

            # vê se não há elementos repetidos na lista
            for j in range(0,i):
                if quebrar[i] == quebrar[j] or quebrar[i] == ' ' or quebrar[i] == '':
                    repetido = True
                    del quebrar[i]
                    break

            if repetido == False and len(quebrar[i]) > 3:
                lista.insert(0,quebrar[i])

        return lista


    def compararListas(self,origem,comparacao):
        # varre todos os elementos
        for i in range(len(origem)-1,-1,-1):
            
            # vê se não há elementos repetidos na lista
            for j in range(0,len(comparacao)):
                if origem[i] == comparacao[j] or origem[i] == ' ' or origem[i] == '':
                    del origem[i]
                    break


        return origem


    def textoFinal(self,texto,lista,comTexto = True):
        for i in range(0,len(lista)):
            texto = texto.replace(
                lista[i].encode(),
                (255).to_bytes(1,'big')+(i).to_bytes(2,'big')
            )

        listaString = ",".join(lista)

        final = len(lista).to_bytes(2,'big') + listaString.encode() + ",".encode()
        
        if comTexto:
            final += texto

        return final 



    def lista(self,texto,ordenar = True):
        texto = texto.decode('ascii')
        textoLista = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ:]', ' ',texto)
        quebrar = textoLista.split(" ")

        if ordenar:
            return self.tirarRepeticao(quebrar)
        else:
            return quebrar


    def apontaUltimaPalavra(self,texto,arquivo):

        regex = re.finditer(u'[^a-zA-Z0-9:]', texto.decode('ascii')) 

        ultimaOcorrencia = None
        for ocorrencia in regex:
            ultimaOcorrencia = (ocorrencia.span())


        posicaoLeitor = len(texto) - ultimaOcorrencia[1]

        texto = texto[0:ultimaOcorrencia[1]]

        
        if posicaoLeitor < arquivo.ponteiro():
            arquivo.seek(-posicaoLeitor,1)

        return texto


    def compactar(self):

        tamanhoLeitor = self.leitura.getTamanho()
        self.leitura.seek(0,0)

        if tamanhoLeitor <= 2 * Arquivo.TAMANHOBUFFER:
            texto = self.leitura.leitura(tamanhoLeitor)
            lista = self.ordenacaoLista(self.lista(texto))
            
            final = self.textoFinal(texto,lista)
            self.gravacao.gravacao(final)
        else:
            tamanhoLista = 0
            self.gravacao.gravacao((0).to_bytes(2,Arquivo.BYTEORDER))

            while tamanhoLeitor - self.leitura.ponteiro() > 0:

                textoLeitor = self.leitura.leitura(Arquivo.TAMANHOBUFFER)
                textoLeitor = self.apontaUltimaPalavra(textoLeitor,self.leitura)

                #self.gravacao.gravacao(textoLeitor)

                lista = (self.lista(textoLeitor))

                self.gravacao.seek(2,0)
                while self.gravacao.getTamanho() - self.gravacao.ponteiro() > 0:
                    textoGravador = self.gravacao.leitura(Arquivo.TAMANHOBUFFER)
                    textoGravador = self.apontaUltimaPalavra(textoGravador,self.gravacao)
                    lista = self.compararListas(lista,self.lista(textoGravador))
                    

                tamanhoLista += len(lista)


                if len(lista) > 0:
                    self.gravacao.seek(self.gravacao.getTamanho(),0)
                    self.gravacao.gravacao((",".join(lista) + ",").encode())

            
            #print(tamanhoLista)
            self.gravacao.seek(0,0)
            self.gravacao.gravacao((tamanhoLista).to_bytes(2,Arquivo.BYTEORDER))

            vezes = math.ceil(self.gravacao.getTamanho()/Arquivo.TAMANHOBUFFER)

            for i in range(0,vezes):
                self.gravacao.seek(2,0)

                while self.gravacao.getTamanho() - self.gravacao.ponteiro() > 0:
                    textoGravador = self.gravacao.leitura(Arquivo.TAMANHOBUFFER*2)
                    
                    textoGravador = self.apontaUltimaPalavra(textoGravador,self.gravacao)
                    lista = self.ordenacaoLista(self.lista(textoGravador))
                    
                    
                    if self.gravacao.ponteiro() > Arquivo.TAMANHOBUFFER*2+2:
                        self.gravacao.seek(-Arquivo.TAMANHOBUFFER*2,1)
                    else:
                        self.gravacao.seek(2,0)


                    self.gravacao.gravacao((",".join(lista) + ",").encode())
                
                if(self.gravacao.getTamanho() - self.gravacao.ponteiro() > 0 or self.gravacao.ponteiro() < Arquivo.TAMANHOBUFFER*2+2):
                    self.gravacao.seek(2,0)
                else:
                    self.gravacao.seek(-Arquivo.TAMANHOBUFFER,1)

            enderecoUltimoRrn = self.gravacao.getTamanho()
            self.leitura.seek(0,0)

            while tamanhoLeitor - self.leitura.ponteiro() > 0:

                textoLeitor = self.leitura.leitura(Arquivo.TAMANHOBUFFER)
                textoLeitor = self.apontaUltimaPalavra(textoLeitor,self.leitura)
                
                self.gravacao.seek(2,0)
                while enderecoUltimoRrn - self.gravacao.ponteiro() > 0:

                    tBuffer = Arquivo.TAMANHOBUFFER
                    if enderecoUltimoRrn - tBuffer < tBuffer:
                        tBuffer = enderecoUltimoRrn - self.gravacao.ponteiro()

                    textoGravador = self.gravacao.leitura(tBuffer)
                    textoGravador = self.apontaUltimaPalavra(textoGravador,self.gravacao)
                    lista = self.lista(textoGravador)
                    print(lista)
                    
                    
                    rrn = 0
                    for i in range(0,len(lista)):

                        textoLeitor = textoLeitor.replace(
                            lista[i].encode(),
                            (255).to_bytes(1,'big')+(rrn).to_bytes(2,'big')
                        )

                        rrn += 1
                    
  
                self.gravacao.seek(0,2)
                self.gravacao.gravacao(textoLeitor)
                

                    

                    

    def __init__(self,leitor,gravador):

        # inicia a manipulação dos arquivos
        self.leitura = leitor        
        self.gravacao = gravador



caminho = "testGrande.txt"
Compactador(Arquivo.Arquivo(caminho,"rb"),Arquivo.Arquivo(caminho+".cmp","w+b")).compactar()

#txt = b"dda sdasdasd".replace()
#print(txt)