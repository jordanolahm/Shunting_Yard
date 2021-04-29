
class ExpToken:
    def __init__(self):
        self.ListaTokensTipo = []
        self.ListaTokensValor = []

class State:
    def __init__(self, dic_transition, dic_insert, dic_remove):
        self.Transicao = dic_transition
        self.Insere = dic_insert
        self.Consome = dic_remove

class PushdownAutomaton:
    def __init__(self, VetorEstadosFinais, VetorEstados):
        self.Estado = VetorEstados
        self.Pilha = []
        self.EstadosFinais = VetorEstadosFinais
        self.EstadoAtual = 0


        #Modulo 4 - Rotina de validacao da analise Sintatica a partir da entrada.
    def AnaliseSintatica(self, LinhaTokensTipo):
        #Prepara o automato para processar a entrada
        LinhaTokensTipo.append('empty')                                         #Adiciona o token de "final de entrada" a fila de entrada
        self.EstadoAtual = 0                                                    #Retorna o automato ao estado inicial
        self.Pilha.clear()                                                      #Limpa a pilha
        self.Pilha.append('empty')                                              #Adiciona o token de "base da pilha" a pilha do automato

        #Processa a entrada
        while len(LinhaTokensTipo) > 0:
            Token = LinhaTokensTipo.pop(0)                                      #Toma o primeiro token da fila de entrada
            Transicao = self.Estado[self.EstadoAtual].Transicao.get(Token)      #Toma o proximo estado do automato conforme o primeiro token da fila de entrada
            Insere = self.Estado[self.EstadoAtual].Insere.get(Token)            #Toma o elemento a ser inserido na pilha conforme o primeiro token da fila de entrada
            Consome = self.Estado[self.EstadoAtual].Consome.get(Token)          #Toma o elemento a ser removido na pilha conforme o primeiro token da fila de entrada
            #print(Token)
            #print(Transicao)
            #print(Consome)
            if Transicao == None:                                               #Retorna -1 caso não exista transição relacionada ao token da fila de entrada
                #print('Erro1')
                return -1
            if Consome != None and len(self.Pilha) == 0:                        #Retorna -1 caso seja exigido o consumo de um elemento da pilha e a mesma esteja vazia
                #print('Erro2')
                return -1
            if Consome != None and Consome != self.Pilha.pop():                 #Retorna -1 caso seja exigido o consumo de um elemento da pilha e o mesmo não esteja no topo
                #print('Erro3')
                return -1

            self.EstadoAtual = Transicao                                        #Muda o estado do automato
            if Insere != None:                                                  #Caso seja exigido adiciona um elemento a pilha do automato
                self.Pilha.append(Insere)

        if self.EstadoAtual in self.EstadosFinais:
            return 1
        return -1

    #Modulo 5 -  Definicao do algoritmo do Shutting Yard

class ShuntingYard:
    def __init__(self, Precedencia, Associatividade, NumOperandos):
        self.Precedencia = Precedencia
        self.Associatividade = Associatividade
        self.NumOperandos = NumOperandos

    def GeraSaida(self, LinhaTokensTipo, LinhaTokensValor):
        Pilha = []
        Fila = []
        #print(LinhaTokensTipo)
        #print(LinhaTokensValor)
        cont = 0
        while cont < len(LinhaTokensTipo):
            #print('Pilha: ', end=' ')
            #print(Pilha)
            #print('Fila: ', end=' ')
            #print(Fila)
            if LinhaTokensTipo[cont] == "VAR" or LinhaTokensTipo[cont] == "BINARY":
                Fila.append(LinhaTokensValor[cont])
            elif LinhaTokensTipo[cont] == "LPAREN":
                Pilha.append(LinhaTokensTipo[cont])
            elif LinhaTokensTipo[cont] == "RPAREN":
                while Pilha[len(Pilha) - 1] != "LPAREN":
                    Fila.append(Pilha.pop())
                Pilha.pop()
            else:
                nivelprec = self.Precedencia.get(LinhaTokensTipo[cont])
                tipoassoc = self.Associatividade.get(LinhaTokensTipo[cont])
                if len(Pilha) == 0 or Pilha[len(Pilha) - 1] == "LPAREN":
                    Pilha.append(LinhaTokensTipo[cont])
                else:
                    proxnivelprec = self.Precedencia.get(Pilha[len(Pilha) - 1], -1)
                    if tipoassoc == 'left':
                        while len(Pilha) > 0 and Pilha[len(Pilha) - 1] != "LPAREN" and proxnivelprec >= nivelprec:
                            Fila.append(Pilha.pop())
                            if(len(Pilha) > 0):
                                  proxnivelprec = self.Precedencia.get(Pilha[len(Pilha) - 1], -1)
                    elif tipoassoc == 'right':
                        while len(Pilha) > 0 and Pilha[len(Pilha) - 1] != "LPAREN" and proxnivelprec > nivelprec:
                            Fila.append(Pilha.pop())
                            if(len(Pilha) > 0):
                                proxnivelprec = self.Precedencia.get(Pilha[len(Pilha) - 1], -1)
                    Pilha.append(LinhaTokensTipo[cont])
            cont += 1
        while len(Pilha) > 0:
            Fila.append(Pilha.pop())
        return Fila
    
    def ConverterParaArvore(self, PilhaRPN):
        return self.__ConverterParaArvore(PilhaRPN, 0, len(PilhaRPN) - 1, [])
    
    def __ConverterParaArvore(self, PilhaRPN, PosIni, PosFim, ListaNosAtrelados):
        #print(PilhaRPN[PosIni:(PosFim+1)])
        NumOperandos = self.NumOperandos.get(PilhaRPN[PosFim])
        if NumOperandos == 1:
            ListaNosAtrelados.append(PosFim)
            return No( PilhaRPN[PosFim], self.__ConverterParaArvore(PilhaRPN, PosIni, PosFim - 1, ListaNosAtrelados)  )
        elif NumOperandos == 2:
            ListaNosAtrelados.append(PosFim)
            NoSaida = No(PilhaRPN[PosFim])
            NoSaida.PtrEsq = self.__ConverterParaArvore(PilhaRPN, PosIni, PosFim - 1, ListaNosAtrelados)
            
            #Procura a posição do elemento mais a direita que não possua nó pai
            NumFinal = PosFim - 2
            while NumFinal in ListaNosAtrelados:
                NumFinal -= 1
            NoSaida.PtrDir = self.__ConverterParaArvore(PilhaRPN, PosIni, NumFinal, ListaNosAtrelados)

            
            return NoSaida
        else:
            ListaNosAtrelados.append(PosFim)
            return No(PilhaRPN[PosFim])

        #Modulo 6 - Criação do autômato, regras, estados e transicao.
