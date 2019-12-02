'''

    Esse arquivo, irá ter a função similar do int main()

'''

import os, sys, Compactador, Descompactador,Arquivo

# pega os argumentos
if len(sys.argv) < 3:
    print("Número de argumentos inválido")
else:

    caminho = sys.argv[2]
    

    # faz o compactador
    if sys.argv[1] == '-c':
        leitor = Arquivo.Arquivo(caminho,"rb")
        gravador = Arquivo.Arquivo(caminho+".cmp","w+b")

        Compactador.Compactador(leitor,gravador).compactar()

        print("Compactado com sucesso!")
        
    elif sys.argv[1] == '-d':
        leitor = Arquivo.Arquivo(caminho,"rb")
        gravador = Arquivo.Arquivo(caminho[0:len(caminho)-4],"w")

        Descompactador.Descompactador(leitor,gravador).descompactar()

        print("Descompactado com sucesso!")
    else:
        print("parâmetro inválido!")
        sys.exit(1)
