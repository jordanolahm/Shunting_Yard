import time
import sys
 
    #classe que define a árvore
class No:
    def __init__(self, Conteudo = None, PtrEsq = None, PtrDir = None):
        self.Conteudo = Conteudo
        self.PtrEsq = PtrEsq
        self.PtrDir = PtrDir
        
def CaminhaPreFixo(No):
    print(No.Conteudo)
    if No.PtrEsq is not None:
        CaminhaPosFixo(No.PtrEsq)
    if No.PtrDir is not None:
        CaminhaPosFixo(No.PtrDir)

def CaminhaPosFixo(No):
    if No.PtrEsq is not None:
        CaminhaPosFixo(No.PtrEsq)
    if No.PtrDir is not None:
        CaminhaPosFixo(No.PtrDir)
    print(No.Conteudo)
    
def CaminhaInFixo(No):
    if No.PtrEsq is not None:
        CaminhaPosFixo(No.PtrEsq)
    print(No.Conteudo)
    if No.PtrDir is not None:
        CaminhaPosFixo(No.PtrDir)

def AlturaArvore(No):
    if No == None:
        return 1
    AltEsq = AlturaArvore(No.PtrEsq)
    AltDir = AlturaArvore(No.PtrDir)
    if AltEsq >= AltDir:
        return 1 + AltEsq
    else:
        return 1 + AltDir

def CaminhaAltitude(No, SaidaArqNome): #rotina que caminha na árvore e retorna altura, melhor para verificacao da arvore de tokens
    ArqSaida = open(SaidaArqNome, 'a+')
    
    AltArvore = AlturaArvore(No)
    Cont = 0
    Expoente = 0
    ExpoenteLimite = 1
    Saida = [No] #lista de nós, com ínicio do no raiz
    while Expoente < AltArvore:
        while Cont < ExpoenteLimite: #2^n, n = 0
            if (Saida[Cont] == None):
                Saida.append(None) #printar none, com nós sem valor
                Saida.append(None) #printar none, com nós sem valor
                ArqSaida.write('None ')
            else:
                Saida.append(Saida[Cont].PtrEsq)
                Saida.append(Saida[Cont].PtrDir)
                ArqSaida.write(str(Saida[Cont].Conteudo) + ' ')
            Cont += 1
        ArqSaida.write('\n')
        Expoente += 1
        ExpoenteLimite += 2**(Expoente)
    ArqSaida.write('\n')
    ArqSaida.close()    
    return Saida

#Modulo 1: Definição da estrutura da análise Lexica.
class Estado():
    def __init__(self, nome, final = 0):
        self.nome = nome
        self.final = final
        if (final == 0):
            self.mensagem = ''

    def set_regra(self, regra):
        self.regras = regra

    def retorna_nome(self):
        return self.nome

    def retorna_est_final(self):
        if (self.final == 1):
            print('Final')
        else:
            print('Nao final')

    def printa_regras(self):
        for i in self.regras:
            print('le '+ i + ', vai para '+ self.regras[i])


class Automato():
    def __init__(self):
        self.vet_estados = []
        self.dic_regras = {}

    def printa_dic_regras(self):
        print(self.dic_regras)

    def adiciona_estado(self, nome, regra, final = 0):
        estado = Estado(nome, final)
        estado.set_regra(regra)
        self.dic_regras.update({nome : len(self.vet_estados)})
        self.vet_estados.append(estado)

    def lex_corretude(self, entrada, result_tok, result_nome):
        result = ''

        entrada = entrada.replace(' ','')

        i = 0
        while i < len(entrada):
            if ord(entrada[i]) > 127:
                entrada = entrada[0:i] + entrada[i:]
            i = i+1
        est_atual = 0
        i = 0
        token = ''

        while i < len(entrada):       #varrendo a entrada
            if (entrada[i] == '\n'):
                break
            try:
                est_atual = self.vet_estados[est_atual].regras[entrada[i]]
                #print(est_atual)
                token = token + entrada[i]
                i = i+1

            except:
                if (self.vet_estados[est_atual].final == 1):

                    result_tok.append(token)
                    result_nome.append(self.vet_estados[est_atual].nome)
                    est_atual = 0

                else:
                    if (est_atual == 0):
                        token = entrada[i]
                        i=i+1
                    result = result + ('Token: "'+token+'" invalido, posição: '+str(i-len(token))+'.' + self.vet_estados[est_atual].mensagem + '\n')
                    est_atual = 0
                token = ''

        if (self.vet_estados[est_atual].final == 1):
            result_tok.append(token)
            result_nome.append(self.vet_estados[est_atual].nome)
            est_atual = 0

        else:
            result = result + ('Token: "'+token+'" invalido, posição: '+str(i-len(token))+'.' + self.vet_estados[est_atual].mensagem + '\n')
            est_atual = 0

        return result

    #Modulo 2: Definicao das rotinas de tratamento.
    def retorna_est_final(self, nome):
        for i in self.vet_estados:
            if (i.nome == nome):
                if (i.final == 1):
                    print('Final')
                else:
                    print('Nao final')

    def adiciona_mensagem(self, nome, mensagem):
        a = self.dic_regras[nome]
        self.vet_estados[a].mensagem = mensagem

    def lexf(self, entrada):

        self.pre_processamento(entrada)

        est_atual = 0
        i = 0
        token = ''
        result = ''

        while i < len(entrada):
            if (entrada[i] == '\n'):
                break
            try:
                est_atual = self.vet_estados[est_atual].regras[entrada[i]]
                token = token + entrada[i]
                i = i+1

            except:
                if (self.vet_estados[est_atual].final == 1):
                    result = result + ('Token: "'+token+'" valido, nome: '+self.vet_estados[est_atual].nome+ ', posição: '+str(i-len(token)) + '\n')
                    est_atual = 0

                else:
                    if (est_atual == 0):
                        token = entrada[i]
                        i=i+1
                    #result = result + ('Token: "'+token+'" invalido, posição: '+str(i-len(token))+'.' + self.vet_estados[est_atual].mensagem + '\n')
                    est_atual = 0

                token = ''

        if (self.vet_estados[est_atual].final == 1):
            #result = result + ('Token: "'+token+'" valido, nome: '+self.vet_estados[est_atual].nome+ ', posição: '+str(i-len(token)) + '\n')
            est_atual = 0

        else:
            result = result + ('Token: "'+token+'" invalido, posição: '+str(i-len(token))+'.' + self.vet_estados[est_atual].mensagem + '\n')
            est_atual = 0

        return result

        #Modulo 3 - Início da análise sintática.

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

aut = Automato()
aut.adiciona_estado('q0', {"(":1,
                        ")":11,
                        "~":2,
                        "0":3,
                        "1":3,
                        "a":4,"b":4,"c":4,"d":4,"e":4,"f":4,"g":4,"h":4,"i":4,"j":4,"k":4,"l":4,"m":4,"n":4,"o":4,"p":4,"q":4,"r":4,"s":4,"t":4,"u":4,"v":4,"w":4,"x":4,"y":4,"z":4,
                        "A":4,"B":4,"C":4,"D":4,"E":4,"F":4,"G":4,"H":4,"I":4,"J":4,"K":4,"L":4,"M":4,"N":4,"O":4,"P":4,"Q":4,"R":4,"S":4,"T":4,"U":4,"V":4,"W":4,"X":4,"Y":4,"Z":4,
                        "\\":5,
                        "/":7,
                        ">":9,
                        "=":10})
aut.adiciona_mensagem('q0',' Você esta no estado inicial, insira algum token válido a partir daqui.')

aut.adiciona_estado("LPAREN",   {}, 1)
aut.adiciona_estado("NOT", {}, 1)
aut.adiciona_estado("BINARY",   {}, 1)
aut.adiciona_estado("VAR", {"a":4,"b":4,"c":4,"d":4,"e":4,"f":4,"g":4,"h":4,"i":4,"j":4,"k":4,"l":4,"m":4,"n":4,"o":4,"p":4,"q":4,"r":4,"s":4,"t":4,"u":4,"v":4,"w":4,"x":4,"y":4,"z":4,
                            "A":4,"B":4,"C":4,"D":4,"E":4,"F":4,"G":4,"H":4,"I":4,"J":4,"K":4,"L":4,"M":4,"N":4,"O":4,"P":4,"Q":4,"R":4,"S":4,"T":4,"U":4,"V":4,"W":4,"X":4,"Y":4,"Z":4,
                            "0":4,"1":4,"2":4,"3":4,"4":4,"5":4,"6":4,"7":4,"8":4,"9":4,}, 1)
aut.adiciona_estado('q5',        {"/":6})
aut.adiciona_mensagem('q5',' Está faltando fechar a barra da disjunção.')
aut.adiciona_estado("DISJ", {}, 1)
aut.adiciona_estado('q7',        {"\\":8})
aut.adiciona_mensagem('q7',' Está faltando fechar a barra da conjunção.')
aut.adiciona_estado("CONJ", {}, 1)
aut.adiciona_estado("COND", {}, 1)
aut.adiciona_estado("BCOND", {}, 1)
aut.adiciona_estado("RPAREN", {}, 1)

    #Modulo 7 - Manipulação de arquivo de teste.

'''
ArquivoEntrada = open('Expressoes.txt', 'r')
Aux = ArquivoEntrada.read().splitlines()
Entradas = []
ArquivoEntrada.close()
ArquivoSaida = open('Saidas.txt', 'w+')
'''

     #Modulo 8 - Dicionario de transicao dos estados

EstadosAutomato = []
EstadosFinais = [6]

EstadoTransicao0 = {
    'VAR': 1,
    'LPAREN': 4,
    'NOT': 3,
    'BINARY': 1
}

EstadoInsere0 = {
    'LPAREN': 'X'
}

EstadoConsome0 = {
}

EstadosAutomato.append(State(EstadoTransicao0, EstadoInsere0, EstadoConsome0))

EstadoTransicao1 = {
    'CONJ': 2,
    'DISJ': 2,
    'COND': 2,
    'BCOND': 2,
    'RPAREN': 5,
    'empty': 6
}

EstadoInsere1 = {
}

EstadoConsome1 = {
    'RPAREN': 'X',
    'empty': 'empty'
}

EstadosAutomato.append(State(EstadoTransicao1, EstadoInsere1, EstadoConsome1))

EstadoTransicao2 = {
    'VAR': 1,
    'BINARY': 1,
    'LPAREN': 4,
    'NOT': 3
}

EstadoInsere2 = {
    'LPAREN': 'X'
}

EstadoConsome2 = {
}

EstadosAutomato.append(State(EstadoTransicao2, EstadoInsere2, EstadoConsome2))

EstadoTransicao3 = {
    'NOT': 3,
    'LPAREN': 4,
    'VAR': 1,
    'BINARY': 1
}

EstadoInsere3 = {
    'LPAREN': 'X'
}

EstadoConsome3 = {
}

EstadosAutomato.append(State(EstadoTransicao3, EstadoInsere3, EstadoConsome3))

EstadoTransicao4 = {
    'VAR': 1,
    'BINARY': 1,
    'LPAREN': 4,
    'NOT': 3
}

EstadoInsere4 = {
    'LPAREN': 'X'
}

EstadoConsome4 = {
}

EstadosAutomato.append(State(EstadoTransicao4, EstadoInsere4, EstadoConsome4))

EstadoTransicao5 = {
    'RPAREN': 5,
    'CONJ': 2,
    'DISJ': 2,
    'COND': 2,
    'BCOND': 2,
    'empty': 6
}

EstadoInsere5 = {
}

EstadoConsome5 = {
    'RPAREN': 'X',
    'empty': 'empty'
}

EstadosAutomato.append(State(EstadoTransicao5, EstadoInsere5, EstadoConsome5))

EstadoTransicao6 = {
}

EstadoInsere6 = {
}

EstadoConsome6 = {
}

    #Modulo 9 - Declaracao de regras do Shutting -> peso de operadores
'''
Precedencia = {
    'CONJ': 0,
    'DISJ': 1,
    'COND': 2,
    'BCOND': 3,
    'NOT': 4
}

Associatividade = {
    'CONJ': 'left',
    'DISJ': 'left',
    'COND': 'left',
    'BCOND': 'left',
    'NOT': 'left'
 }

NumOperandos = {
    'CONJ': 2,
    'DISJ': 2,
    'COND': 2,
    'BCOND': 2,
    'NOT': 1
}


    #Modulo 10 - Tratamento final, chamada de rotinas da analise Sintatica, verificacao da corretude para operacao.

cont = 0
while cont < len(Aux):
    tok_nomes = []
    tok_valores = []
    #print(Aux[cont])

    E_lexico = aut.lex_corretude(Aux[cont], tok_nomes, tok_valores)

    EstadosAutomato.append(State(EstadoTransicao6, EstadoInsere6, EstadoConsome6))
    AnalisadorSintatico = PushdownAutomaton(EstadosFinais, EstadosAutomato)

    Saida1 = ExpToken()
    Saida1.ListaTokensTipo = tok_valores
    Saida1.ListaTokensValor = tok_nomes

    Corretude = AnalisadorSintatico.AnaliseSintatica(Saida1.ListaTokensTipo.copy()) #algoritmo léxico cópia 

    if (Corretude == 1) and (len(E_lexico) == 0): #continuação sem erro da léxica, para começar a sintática
        Parsing = ShuntingYard(Precedencia, Associatividade, NumOperandos)
        Saida2 = Parsing.GeraSaida(Saida1.ListaTokensTipo, Saida1.ListaTokensValor)
        #print('Shunting: ' + str(Saida2))
        Saida2Arv = Parsing.ConverterParaArvore(Saida2)
        CaminhaAltitude(Saida2Arv, 'SaidaEmArvore.txt')
        for elem in Saida2:
            ArquivoSaida.write(elem+' ')

        ArquivoSaida.write('\n')
    else:
        ArquivoSaida.write('Erro')
        ArquivoSaida.write('\n')
    cont += 1
ArquivoSaida.close()
'''


print("\n\nAnalise concluida com sucesso!")
print("Confira o arquivo de saida.")
time.sleep(5)
sys.exit()