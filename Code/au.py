

    def parser(self,num,px2):
        carga2 = 0
        pos = -1
        print("Vamos definir o carregamento", num, "(cargas em N/m e tamanho da barra em m):")
        print("tamanho da barra = 0 - define carga pontual entre carregamentos")
        x1 = px2

        tam = input("Tamanho da barra = ")
        while not eh_numero(tam,True):
            tam = input("Tamanho da barra =  ")
        tam = float(tam)
        x2=x1+tam

        opcao = input("1 - Carregamento distribuido\n2 - Carga pontual: ")
        while not eh_12(opcao):
            opcao = input("1 - Carregamento distribuido\n2 - Carga pontual: ")
        opcao = int(opcao)

        if opcao == 1:
            carga1 = input("Carga 1 = ")
            while not eh_numero(carga1,True):
                carga1 = input("Carga 1 =   ")
            carga1 = float(carga1)

            carga2 = input("Carga 2 =  ")
            while not eh_numero(carga2,True):
                carga2 = input("Carga 2 =  ")
            carga2 = float(carga2)
        else:
            carga1 = input("Carga = ")
            while not eh_numero(carga1):
                carga1 = input("Carga =  ")
            carga1 = float(carga1)

            if tam != 0:
                pos = input("Posição da carga = ")
                while not eh_numero(pos,True):
                    pos = input("Posição da carga =  ")
            else:
                pos = 0


        self.__instanciar(x1,x2,carga1,carga2,pos)

        return x2