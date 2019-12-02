'''

    Nessa classe, terá as funções para compactar os textos

'''

import os, sys, math,Arquivo, re

class Compactador:

    leitura = None # conterá a classe de Arquivo para leitura
    gravacao = None # conterá a classe de Arquivo para gravar 

    # tira os itens repetidos
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

            #  se não for repetido e maior que 3, adiciona a lista final
            if repetido == False and len(quebrar[i]) > 3:
                lista.insert(0,quebrar[i])

        return lista


    # compara a lista para ver se há elementos repetidos
    def compararListas(self,origem,comparacao):
        # varre todos os elementos
        for i in range(len(origem)-1,-1,-1):
            
            # vê se não há elementos repetidos na lista
            for j in range(0,len(comparacao)):
                if origem[i] == comparacao[j] or origem[i] == ' ' or origem[i] == '':
                    del origem[i]
                    break


        return origem



    # gera o texto final para arquivos pequenos
    def textoFinal(self,texto,lista,comTexto = True):
        

        # corrige o bug da exepection
        bug = []

        # varre toda a lista, para a substituição
        for i in range(0,len(lista)):

            regex = re.compile(("(?:\\b)"+lista[i]+"(?:\\b)").encode())

            try:
                texto = re.sub(
                    regex,
                    (255).to_bytes(1,Arquivo.BYTEORDER)+(i).to_bytes(2,Arquivo.BYTEORDER),
                    texto
                )

            except:
               bug.append(i)

        # corrige o bug das impressoes
        # juro que não é gambiarra
        if len(bug) > 0:
            for i in range(0,len(bug)):
                for j in range(0,i):
                    if len(lista[bug[i]]) > len(lista[bug[j]]):
                        temp = bug[i]
                        bug[i] = bug[j]
                        bug[j] = temp

            for i in range(0,len(bug)):
                texto = texto.replace(lista[bug[i]].encode(),(255).to_bytes(1,Arquivo.BYTEORDER)+(bug[i]).to_bytes(2,Arquivo.BYTEORDER))
            


        # gera a lista em string
        listaString = ",".join(lista)

        # gera a string ginal
        final = len(lista).to_bytes(2,Arquivo.BYTEORDER) + listaString.encode() + ",".encode()
        
        # se houver texto final, concatena 
        if comTexto:
            final += texto

        final = final.replace(b"\r\n",b"\n")

        

        return final



    # gera a lista de palavras, a partir do texto
    def lista(self,texto,ordenar = True):

        # quebra a palavra 
        texto = texto.decode(Arquivo.CODIFICACAO)
        textoLista = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ]', ' ',texto)
        quebrar = textoLista.split(" ")

        if ordenar:
            return self.tirarRepeticao(quebrar)
        else:
            return quebrar


    # aponta para a ultima palavra completa do texto, e volta no seek
    def apontaUltimaPalavra(self,texto,arquivo):

        # localiza o ultimo caracter não alfa númerico
        regex = re.finditer(u'[^a-zA-Z0-9]', texto.decode(Arquivo.CODIFICACAO)) 

        # procura a ultima ocorrência
        ultimaOcorrencia = None
        for ocorrencia in regex:
            ultimaOcorrencia = (ocorrencia.span())

        # guarda a posição de seek
        posicaoLeitor = len(texto) - ultimaOcorrencia[1]

        # guarda o texto com a palavra inteira
        texto = texto[0:ultimaOcorrencia[1]]
        
        # volta a posição do ponteirod e arquivo
        if posicaoLeitor < arquivo.ponteiro():
            arquivo.seek(-posicaoLeitor,1)

        return texto


    # função de execução
    def compactar(self):
        # pega o tamanho do arquivo
        tamanhoLeitor = self.leitura.getTamanho()
        self.leitura.seek(0,0)

        # caso o arquivo tenha o tamanho menor que 2 blocos de 4k
        if tamanhoLeitor <= 2 * Arquivo.TAMANHOBUFFER:
            texto = self.leitura.leitura(tamanhoLeitor)
            lista = self.lista(texto)
            
            final = self.textoFinal(texto,lista)
            self.gravacao.gravacao(final)
        else:
            # guarda a quantidade de palavras na lista
            tamanhoLista = 0

            #inicializa o arquivo gravando "0" no cabeçalho
            self.gravacao.gravacao((0).to_bytes(2,Arquivo.BYTEORDER))


            # enquanto não leu todo o arquivo
            while tamanhoLeitor - self.leitura.ponteiro() > 0:

                # lê e aponta para a ultima palavra
                textoLeitor = self.leitura.leitura(Arquivo.TAMANHOBUFFER)
                textoLeitor = self.apontaUltimaPalavra(textoLeitor,self.leitura)

                #gera a lista
                lista = (self.lista(textoLeitor))

                #aponta para depois do cabeçalho
                self.gravacao.seek(2,0)

                # varre a lista para tirar as repetições
                while self.gravacao.getTamanho() - self.gravacao.ponteiro() > 0:
                    textoGravador = self.gravacao.leitura(Arquivo.TAMANHOBUFFER)
                    textoGravador = self.apontaUltimaPalavra(textoGravador,self.gravacao)
                    lista = self.compararListas(lista,self.lista(textoGravador))
                    


                # acresce no tamanho da lista
                tamanhoLista += len(lista)


                # grava apos tirar a repetição
                if len(lista) > 0:
                    self.gravacao.seek(self.gravacao.getTamanho(),0)
                    self.gravacao.gravacao((",".join(lista) + ",").encode())

            
            # aponta e salva o novo tamanho no cabeçalho
            self.gravacao.seek(0,0)
            self.gravacao.gravacao((tamanhoLista).to_bytes(2,Arquivo.BYTEORDER))

            #guarda o endereço da ultima palavra da lista e rebobina o leitor
            enderecoUltimoRrn = self.gravacao.getTamanho()
            self.leitura.seek(0,0)

            # varre novamente o leitor para substituir no texto
            while tamanhoLeitor - self.leitura.ponteiro() > 0:
                
                # lê o texto e aponta para ultima palavra
                textoLeitor = self.leitura.leitura(Arquivo.TAMANHOBUFFER)
                textoLeitor = self.apontaUltimaPalavra(textoLeitor,self.leitura)
                
                # aponta para o inicio da lista
                self.gravacao.seek(2,0)

                # enquanto estiver varrendo a lista
                while enderecoUltimoRrn - self.gravacao.ponteiro() > 0:

                    # pega o valor de leitura
                    tBuffer = Arquivo.TAMANHOBUFFER
                    if enderecoUltimoRrn - tBuffer < tBuffer:
                        tBuffer = enderecoUltimoRrn - self.gravacao.ponteiro()

                    # lê, aponta para ultima palavra da lista, gera a lista
                    textoGravador = self.gravacao.leitura(tBuffer)
                    textoGravador = self.apontaUltimaPalavra(textoGravador,self.gravacao)
                    lista = self.lista(textoGravador)          
         
                    
                    # conta quanto da lista já foi feito
                    rrn = 0

                    # faz a substituição direta no texto
                    for i in range(0,len(lista)):


                        regex = re.compile((r"(?:\b)"+lista[i]+r"(?:\b)").encode())

                        
                        try:
                            textoLeitor = re.sub(
                                regex,
                                (255).to_bytes(1,Arquivo.BYTEORDER)+(rrn).to_bytes(2,Arquivo.BYTEORDER),
                                textoLeitor
                            )
                        except:
                            pass

                        
                        rrn += 1
                    
                textoLeitor = textoLeitor.replace(b"\r\n",b"\n")

                # aponta para final do gravador e grava o texto
                self.gravacao.seek(0,2)
                self.gravacao.gravacao(textoLeitor)
                

                    

                    

    def __init__(self,leitor,gravador):

        # inicia a manipulação dos arquivos
        self.leitura = leitor        
        self.gravacao = gravador
