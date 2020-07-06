class C3E(object):
    def __init__(self, place='', code=''):
        self.place = place
        self.code = code
    def __repr__(self):
        return f'place: {self.place}, code: {self.code}'

class Variable(object):
    def __init__(self, lexeme = '', type = '', scope = ''):
        self.lexeme = lexeme
        self.type = type
        self.scope = scope
        self.isGlobal = lambda: True if self.scope == 'Global' else False
    def __repr__(self):
        return f'lexeme: {self.lexeme}, type: {self.type}, scope: {self.scope}, isGlobal: {self.isGlobal}'

class Syntatic(object):
    def __init__(self, tokenList):
        self.tokenList = tokenList

    def __repr__(self):
        return f'tokenList: {self.tokenList}'

    index = -1
    currentToken = ''

    tempCont = -1
    labelCont = -1

    currentScope = 'Global'
    symbolTable = []

    tempFim = ''
    tempContinue = ''
    resultCode = C3E()

    def erroToken(self):
        return self.tokenList[self.index]
        
    def nextToken(self):
        self.index = self.index + 1
        if(self.index < len(self.tokenList)):
            self.currentToken = self.tokenList[self.index].token
        else:
            self.currentToken = None
        
    def currentLine(self):
        return self.tokenList[self.index].row

    def currentColumn(self):
        return self.tokenList[self.index].col
    
    def currentLexeme(self): 
        return self.tokenList[self.index].lexeme
    
    def analyser(self):
        ld = C3E()
        if (self.LD(ld)):
            self.resultCode.code += ld.code
            if (self.currentToken == 'TK_EOF'):
                return True
        return False

    def LD(self, ld):
        dec = C3E()
        if (self.DEC(dec)):
            ld.code += dec.code
            rld = C3E()
            if (self.RLD(rld)):
                ld.Code += rld.code
                return True
            else: return False
        else: return False

    def RLD(self, rld):
        ld = C3E()
        if (self.LD(ld)):
            rld.code += ld.code
            return True
        else: return True

    def DEC(self, dec):
        myVar = Variable()
        if (self.Type(myVar)):
            self.nextToken()
            if (self.currentToken == "TK_ID"):
                if (not self.AddToSymbolTable(myVar)):
                    print("Variável %s já está em uso.", myVar.lexeme)
                    return False
                self.nextToken()
                if (self.RDEC(dec, myVar)):
                        return True
                else:
                    return False
            else:
                print("Erro: esperava token 'id' na linha %d coluna %d.", self.currentLine(),self.currentColumn())
                return False           
        else: return False
        
        #Parei aqui Continuar RDEC Começar a pensar em UI 
    def RDEC(self, dec, var):
        if self.currentToken == "TK_COMMA":
            self.nextToken()
            if(self.DV(var.type)):
                return True
            else:
                return False
        elif self.currentToken == "TK_LEFTPAR":
            self.currentScope = var.lexeme
            self.nextToken()
            df = C3E()
            if(self.DF(df)):
                dec.code += df.code
                return True
            else:
                return False
        elif self.currentToken == "TK_SEMICOLON":
            self.nextToken()
            return True
        elif self.currentToken == "TK_EQUAL":
            self.nextToken()
            constant = self.currentLexeme()
            aux = self.createTemp()
            if(var.type == 'int'):
                if self.currentToken == "TK_CONST_INT":
                    self.nextToken()
                    if(self.currentToken == "TK_SEMICOLON"):
                        dec.code += f"{aux} = {constant}\n {var.lexeme} = {aux}"
                        self.nextToken()
                        return True
                    else:
                        ##TODO CRIAR ALERTAS
                        print(f'Erro: esperava o token "const_int" na linha {self.currentLine()} coluna ${self.currentColumn()}.')
                        return False
                else:
                    #TODO CRIAR ALERTAS
                    print(f'Erro: esperava o token ";" na linha {self.currentLine()} coluna ${self.currentColumn()}.')

                    return False
            if(var.type == 'float'):
                if self.currentToken == "TK_CONST_REAL":
                    self.nextToken()
                    if(self.currentToken == "TK_SEMICOLON"):
                        dec.code += f"{aux} = {constant}\n {var.lexeme} = {aux}"
                        self.nextToken()
                        return True
                    else:
                        ##TODO CRIAR ALERTAS
                        return False
                else:
                    #TODO CRIAR ALERTAS
                    return False
        else:
        

    def Type(self, var):
        if self.currentToken == "TK_INT" :
            var.type = "int" 
            return True
        elif self.currentToken == "TK_FLOAT":
            var.type = "float"
            return True
        elif self.currentToken == "TK_CHAR": 
            var.type = "char" 
            return True
        elif self.currentToken == "TK_DOUBLE": 
            var.type = "double" 
            return True
        elif self.currentToken == "TK_VOID": 
            var.type = "void" 
            return True
        else: 
            return False

