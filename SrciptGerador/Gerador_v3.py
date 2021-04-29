import random
from random import randint
import string
import Parsing

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

saida1 = Parsing.ShuntingYard(Precedencia, Associatividade, NumOperandos)

class ExpToken:
    def __init__(self):
        self.ListaTokensTipo = []
        self.ListaTokensValor = []

def GeraParsingEsq(NumPassos):
    OperadoresTokens = ['CONJ', 'DISJ', 'COND', 'BCOND', 'NOT']
    OperadoresSimbolos = ['\\/', '/\\', '>', '=', '~']   
    
    Entrada = ExpToken()
    Saida = []
    OperandoEsq = ''
    OperandoDir = ''
    #Aleatoriza operando da esquerda
    OperandoEsq = randint(0, 1)
    #Aleatoriza operando da direita
    OperandoDir = randint(0, 1)
    #Aleatoriza operador    
    OpNum = randint(0, 4)
    
    #Operador binario
    if OpNum >= 0 and OpNum <= 3:
        #Operando da esquerda
        Entrada.ListaTokensValor.append(OperandoEsq)
        Entrada.ListaTokensTipo.append('BOOL')
        
        #Operador    
        Entrada.ListaTokensValor.append(OperadoresSimbolos[OpNum])
        Entrada.ListaTokensTipo.append(OperadoresTokens[OpNum])
        
        #Operando da direita
        Entrada.ListaTokensValor.append(OperandoDir)
        Entrada.ListaTokensTipo.append('BOOL')        
            
        #Monta a saida
        Saida.append(OperandoEsq)
        Saida.append(OperandoDir)
        Saida.append(OperadoresTokens[OpNum])
        
    #Operador unario
    else:
        #Operador    
        Entrada.ListaTokensValor.append(OperadoresSimbolos[OpNum])
        Entrada.ListaTokensTipo.append(OperadoresTokens[OpNum])
        
        #Operando da direita
        Entrada.ListaTokensValor.append(OperandoDir)
        Entrada.ListaTokensTipo.append('BOOL')

        #Monta a saida
        Saida.append(OperandoDir)
        Saida.append(OperadoresTokens[OpNum])              
    
    Cont = 1
    while Cont < NumPassos:
        #Aleatoriza operador    
        OpNum = randint(0, 4)
        #Aleatoriza operando da direita
        if OpNum < 3:
            OperandoDir = randint(0, 1)   
        
        #Insercao dos parenteses laterais
        Entrada.ListaTokensTipo.insert(0, 'LPAREN')
        Entrada.ListaTokensValor.insert(0, '(')
        Entrada.ListaTokensTipo.append('RPAREN')
        Entrada.ListaTokensValor.append(')')        
        #Operador binario
        if OpNum >= 0 and OpNum <= 3:
            #Operador    
            Entrada.ListaTokensValor.append(OperadoresSimbolos[OpNum])
            Entrada.ListaTokensTipo.append(OperadoresTokens[OpNum])
            
            #Operando da direita
            Entrada.ListaTokensValor.append(OperandoDir)
            Entrada.ListaTokensTipo.append('BOOL')     
                
            #Monta a saida
            Saida.append(OperandoDir)
            Saida.append(OperadoresTokens[OpNum])
            
        #Operador unario
        else:
            #Operador    
            Entrada.ListaTokensValor.insert(0, OperadoresSimbolos[OpNum])
            Entrada.ListaTokensTipo.insert(0, OperadoresTokens[OpNum])
                
            #Monta a saida
            Saida.append(OperadoresTokens[OpNum])         
        
        Cont += 1
        
    return [Entrada, Saida]

ArquivoTeste = open('Expressoes.txt', 'w+')
ArquivoTesteResultado = open('Final.txt', 'w+')

NumTeste = 10000
Contador = 0

while Contador < NumTeste:
    Aux = GeraParsingEsq(10)#Numero de TODOS os operadores
    ArquivoTeste.write(str(Aux[0].ListaTokensTipo) + '\n')
    ArquivoTeste.write(str(Aux[0].ListaTokensValor) + '\n')
    ArquivoTeste.write(str(Aux[1]) + '\n')
    
    Resultado = saida1.GeraSaida(Aux[0].ListaTokensTipo, Aux[0].ListaTokensValor)
    if Resultado == Aux[1]:
        ArquivoTesteResultado.write('True\n')
    else:
        ArquivoTesteResultado.write('False\n')
    
        
    print(Aux[1])
    print('\n')
    print(Resultado)
    print('\n')
    Contador += 1
    
ArquivoTeste.close()
ArquivoTesteResultado.close()