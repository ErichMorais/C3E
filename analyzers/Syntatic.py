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

    def   createTemp(self):
        self.tempCont += 1
        return f'T{self.tempCont}'
    
    def createLabel(self):
        self.labelCont += 1
        return f'L{self.labelCont}'
    
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
        var = Variable()
        if (self.Type(var)):
            self.nextToken()
            if (self.currentToken == "TK_ID"):
                if (not self.AddToSymbolTable(var)):
                    print(f"Variável {var.lexeme} já está em uso.", )
                    return False
                self.nextToken()
                if (self.RDEC(dec, var)):
                        return True
                else:
                    return False
            else:
                print(f"Erro: esperava token 'id' na linha {self.currentLine()} coluna {self.currentColumn()}.")
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
                        print(f'Erro: esperava o token ";" na linha {self.currentLine()} coluna ${self.currentColumn()}.')
                        return False
                else:
                    #TODO CRIAR ALERTAS
                    print(f'Erro: esperava o token "const_int" na linha {self.currentLine()} coluna ${self.currentColumn()}.')

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
                        print(f'Erro: esperava o token ";" na linha {self.currentLine()} coluna ${self.currentColumn()}.')                        
                        return False
                else:
                    #TODO CRIAR ALERTAS
                    print(f'Erro: esperava o token "const_real" na linha {self.currentLine()} coluna ${self.currentColumn()}.')
                    return False
            else:
                print(f'Erro: esperava o o tipo int ou float na linha {self.currentLine()} coluna ${self.currentColumn()}.')
                return False
        else:
                print(f'Erro: esperava o  ;, ) ou , na linha {self.currentLine()} coluna ${self.currentColumn()}.')
                return False

    def DV(self, rcvtype):
        var = Variable()
        var.type = rcvtype
        if (self.currentToken == 'TK_ID'):
            if (not self.AddToSymbolTable(var)):
                return False
            self.nextToken()
            if( self.RDV(rcvtype)):
                return True
            else:
                return False
        else:
            print(f"Erro: esperava token 'id' na linha {self.currentLine()} coluna {self.currentColumn()}.")
            return False

    def RDV(self, rcvtype):
        if (self.currentToken == "TK_COMMA"):
            self.nextToken()
            if (self.DV(rcvtype)):
                return True
            else:
                return False
        elif (self.currentToken == "TK_SEMICOLON"): 
            self.nextToken()
            return True
        else:
            print(f"Erro: esperava token , ou ; na linha {self.currentLine()} coluna {self.currentColumn()}.")
            return False

    def DF(self, df):
        if(self.LP()):
            if (self.currentToken == 'TK_RIGHTPAR'):
                self.nextToken()
                c3eBlock = C3E()
                if (self.blockCode(c3eBlock)):
                    df.code += c3eBlock.code
                    return True
                elif(self.currentToken == 'TK_SEMICOLON'):
                    self.currentScope = 'Global'
                    self.nextToken()
                    return True
                else:
                    print(f"Erro: esperava token "+ '{' + f"ou ; na linha {self.currentLine()} coluna {self.currentColumn()}.")
                    return False
            else:
                    print(f"Erro: esperava token "+ ')' + f"ou ; na linha {self.currentLine()} coluna {self.currentColumn()}.")
                    return False
        else:
            return False

    def LP(self):
        var = Variable()
        if (self.Type(var)):
            self.nextToken()
            if self.currentToken == 'TK_ID':
                if (not self.AddToSymbolTable(var)):
                    return False
                self.nextToken()
                if (self.RLP()):
                    return True
                else:
                    return False
            else:
                print(f"Erro: esperava token 'id' na linha {self.currentLine()} coluna {self.currentColumn()}.")
                return False
        else:
            return True

    def RLP(self):
        if(self.currentToken == 'TK_COMMA'):
            self.nextToken()
            var = Variable()
            if(self.Type(var)):
                self.nextToken()
                if(self.currentToken == 'TK_ID'):
                    if (not self.AddToSymbolTable(var)):
                        return False
                    self.nextToken()
                    if (self.RLP()):
                        return True
                    else:
                        return False
                else:
                    print(f"Erro: esperava token 'id' na linha {self.currentLine()} coluna {self.currentColumn()}.")
                    return False
            else:
                return False
        else:
            return True
    
    def blockCode(self, c3eBlock):
        if(self.currentToken == 'TK_LEFTBRAC'):
            self.nextToken()
            lcd = C3E()
            if(self.LCD(lcd)):
                c3eBlock.code += lcd.code
                if(self.currentToken == 'TK_RIGHTBRAC'):
                    self.currentScope = 'Global'
                    self.nextToken()
                    return True
                else:
                    print(f"Erro: esperava token "+ '}' + f"ou ; na linha {self.currentLine()} coluna {self.currentColumn()}.")
        return False

    def LCD(self, lcd):
        var = Variable()
        cmd = C3E()
        if(self.COM(cmd)):
            lcd.code += cmd.code
            if (self.LCD(lcd)):
                return True
            else:
                return False
        elif (self.Type(var)):
            self.nextToken()
            if(self.DV(var.type)):
                if(self.LCD(lcd)):
                    return True
                else: 
                    return False
            else:
                return True
        else:
            return True

    # TODO Implementar def de comandos da especificacao
    def COM(self, cmd):
        expression = C3E()
        var = Variable()
        #Que deus nos elimine 
        if (self.currentToken == "TK_IF"):
            self.nextToken()
            return self.IFcommand(cmd)
        elif(self.currentToken == "TK_WHILE"):
            self.nextToken()
            return self.WHILEcommand(cmd)
        elif(self.currentToken == "TK_DO"):
            self.nextToken()
            return self.DOWHILEcommand(cmd)
        elif(self.currentToken == "TK_FOR"):
            self.nextToken()
            return self.FORcommand(cmd)
        elif(self.currentToken == "TK_BREAK"):
            self.nextToken()
            if(self.currentToken == "TK_SEMICOLON"):
                self.nextToken()
                cmd.code += f'goto {self.tempFim}\n'
                self.COM(cmd)
                return True
            return False
        elif(self.currentToken == "TK_CONTINUE"):
            self.nextToken()
            if(self.currentToken == "TK_SEMICOLON"):
                self.nextToken()
                cmd.code += f'goto {self.tempContinue}\n'
                self.COM(cmd)
                return True
            return False
        elif (self.Type(var)) :
            self.nextToken()    
            if(self.currentToken == 'TK_ID'):
                if (not self.AddToSymbolTable(var)):
                    return False
                self.nextToken()  
                rdec = C3E()  
                if(self.RDEC(rdec, var)):
                    cmd.code +=rdec.code
                    return True
                else:
                    return False
            else:
                print(f"Erro: esperava token 'id' na linha {self.currentLine()} coluna {self.currentColumn()}.")
                return False
        elif(self.E(expression)):
            cmd.code += expression.code
            if(self.currentToken == "TK_SEMICOLON" ):
                self.nextToken()
                return True
            else:
                return False
        elif(self.currentToken == "TK_RETURN"):
            self.nextToken()
            if(self.currentToken == "TK_SEMICOLON"):
                self.nextToken()
                return True
            else:
                print(f"Erro: esperava token ; na linha {self.currentLine()} coluna {self.currentColumn()}.")
                return False
        else:
            return False

    def IFcommand(self, rcvCode):
        expression = c3eBlock = elseCmd =  C3E()
        if(self.currentToken == "TK_LEFTPAR"):
            self.nextToken()
            if(self.E(expression)):
                if(self.currentToken == "TK_RIGHTPAR"):
                    self.nextToken()
                    if(self.blockCode(c3eBlock)):
                        endLabel = self.createLabel()
                        sintElse = self.ELSEcommand("", endLabel, elseCmd)
                        rcvCode.code = expression.code + f'if {expression.place} = 0 goto {sintElse}\n' + c3eBlock.code +elseCmd+f'{endLabel}'
                        return True
        return False

    def ELSEcommand(self,sintElse, endLabel, elseCmd):
        c3eBlock = C3E()
        if(self.currentToken == "TK_ELSE"):
            self.nextToken()
            if(self.blockCode(c3eBlock)):
                elseLabel = self.createLabel()
                elseCmd.code = f'goto {endLabel} \n{elseLabel}:\n' + c3eBlock.code
                sintElse = elseLabel
                return sintElse
        sintElse = endLabel
        return sintElse

    def WHILEcommand(self, rcvCode):
        expression = c3eBlock = C3E()
        if(self.currentToken == "TK_LEFTPAR"):
            self.nextToken()
            if(self.E(expression)):
                if(self.currentToken == "TK_RIGHTPAR"):
                    self.nextToken()
                    self.tempContinue = iLabel = self.createLabel()
                    self.tempFim = fLabel = self.createLabel()
                    if(self.blockCode(c3eBlock)):
                        rcvCode.code = f'{iLabel}+\n {expression.code} if {expression.place} = 0 goto {fLabel}\n {c3eBlock.code} goto {iLabel}\n {fLabel}:\n'
                        return True
        return False

    def DOWHILEcommand(self,rcvCode):
        expression = c3eBlock = C3E()
        iLabel = self.createLabel()
        fLabel = self.createLabel()
        self.tempFim = fLabel
        self.tempContinue = iLabel
        if(self.blockCode(c3eBlock)):
            if(self.currentToken == "TK_WHILE"):
                self.nextToken()
                if(self.currentToken == "TK_LEFTPAR"):
                    self.nextToken()
                    if(self.E(expression)):
                        if(self.currentToken == "TK_RIGHTPAR"):
                            self.nextToken()
                            if(self.currentToken == "TK_SEMICOLON"):
                                self.nextToken()
                                rcvCode.code = f'{iLabel}+\n {c3eBlock + expression.code} if {expression.place} = 0 goto {iLabel}\n {fLabel}:\n'
                                return True
        return False

    def FORcommand(self, rcvCode):
        firstExp = secExp = trdExp = c3eBlock = C3E()
        if(self.currentToken == "TK_LEFTPAR"):
            self.nextToken()
            if(self.E(firstExp)):
                if(self.currentToken == "TK_SEMICOLON"):
                    self.nextToken()
                    if(self.E(secExp)):
                        if(self.currentToken == "TK_SEMICOLON"):
                            self.nextToken()
                            if(self.E(trdExp)):
                                if(self.currentToken == "TK_RIGHTPAR"):
                                    self.nextToken()
                                    iLabel = self.createLabel()
                                    self.tempFim = fLabel = self.createLabel()
                                    if(self.blockCode(c3eBlock)):
                                        rcvCode.code = firstExp.code + f'{iLabel}:\n {secExp.code} if {secExp.place} = 0 goto {fLabel}\n {c3eBlock.code+self.tempContinue}: \n {trdExp.code} goto {iLabel}\n {fLabel}' 
                                        return True
        return False     

    #E -> E' E1 
    def E(self, E): 
        varE1 = sintE = herdE = C3E()
        if (self.E1(varE1)):
            herdE.place = varE1.place
            herdE.code = varE1.code
            if (self.lineE(herdE, sintE)):
                E.place = sintE.place
                E.code = sintE.code
                return True
            else: 
                return False
        else: 
            return False
    
    #E' -> ,E1 E' | e
    def lineE(self, herdE, sintE):
        varE1 = sintELinha = herdELinha = C3E()
        if (self.currentToken == 'TK_COMMA'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E1(varE1)):
                herdELinha.place = self.createTemp()
                herdELinha.code = (herdE.code + varE1.code + 
                f'{herdELinha.place} = {herdE.place} {op} {varE1.place}\n')
                if (self.lineE(herdELinha, sintELinha)):
                    sintE.code = sintELinha.code
                    sintE.place = sintELinha.place
                    return True
                else:
                    return False
        sintE.place = herdE.place
        sintE.code = herdE.code
        return True

    def E1(self, varE1):
        herdE1 = C3E()
        varE3 = C3E()
        if (self.E3(varE3)):
            if (self.currentToken == 'TK_EQUAL' or self.currentToken == 'TK_STAREQUAL' or self.currentToken == 'TK_SLASHEQUAL'
                or self.currentToken == 'TK_PERCENTEQUAL' or self.currentToken == 'TK_PLUSEQUAL' or self.currentToken == 'TK_MINEQUAL'):
                op = self.currentLexeme()
                self.nextToken()
                if (self.E1(herdE1)):
                    varE1.place = herdE1.place
                    if (op == '='):
                        varE1.code = f'{herdE1.code + varE3.code + varE3.place} = {varE1.place}\n'
                    else:
                        varE1.code = f'{herdE1.code + varE3.code + varE3.place} = {varE3.place} {op.substring(0, 1)}{ varE1.place}\n'
                    return True
                else:
                    return False      
            else:
                varE1.place = varE3.place
                varE1.code = varE3.code
                return True
        else:
            return False

    # def E2(self, sintExpression, herdExpression):
    #     if (self.E3(sintExpression)):
    #         if (self.lineE2(sintExpression, herdExpression)):
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False

    # def lineE2(self, exp_s, exp_h):
    #     if (self.E2(exp_s, exp_h)):
    #         if (self.currentToken == 'TK_COLON'):
    #             self.nextToken()    
    #             if (self.E2(exp_s, exp_h)):
    #                 if (self.E2Linha(exp_s, exp_h)):
    #                     return True
    #                 else return: False
    #      else: return False
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

