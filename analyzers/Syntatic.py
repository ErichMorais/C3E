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

    def createTemp(self):
        self.tempCont += 1
        return f'T{self.tempCont}'
    
    def createLabel(self):
        self.labelCont += 1
        return f'L{self.labelCont}'
    
    def AddToSymbolTable(self, rcvVar):
        actVar = self.symbolTable.index(lambda item: item.lexeme == self.currentLexeme())
        print(self.symbolTable)
        if (actVar):
            return False
        else:
            actVar.scope = self.currentScope
            actVar.lexeme = self.currentLexeme()
            self.symbolTable.append(actVar)
            return True
    

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
            print(dec)
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
            print(ld)
            rld.code += ld.code
            return True
        else: return True

    def DEC(self, dec):
        var = Variable()
        if (self.Type(var)):
            print(var)
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
    #*************************************************************EXPRESSÕES*****************************************************************************
    #E -> lineE E1
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
    
    #lineE -> ,E1 lineE | vazio
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

    #E1 -> E2 = E1 | E2 += E1 | E2 -= E1 | E2 *= E1 | E2 ÷= E1 | E2 %= E1 E2
    def E1(self, varE1):
        herdE1 = C3E()
        varE2 = C3E()
        if (self.E2(varE2)):
            if (self.currentToken == 'TK_EQUAL' or self.currentToken == 'TK_STAREQUAL' or self.currentToken == 'TK_SLASHEQUAL'
                or self.currentToken == 'TK_PERCENTEQUAL' or self.currentToken == 'TK_PLUSEQUAL' or self.currentToken == 'TK_MINEQUAL'):
                op = self.currentLexeme()
                self.nextToken()
                if (self.E1(herdE1)):
                    varE1.place = herdE1.place
                    if (op == '='):
                        varE1.code = f'{herdE1.code + varE2.code + varE2.place} = {varE1.place}\n'
                    else:
                        varE1.code = f'{herdE1.code + varE2.code + varE2.place} = {varE2.place} {op.substring(0, 1)}{ varE1.place}\n'
                    return True
                else:
                    return False      
            else:
                varE1.place = varE2.place
                varE1.code = varE2.code
                return True
        else:
            return False

    # def E2(self, sintExpression, herdExpression):
    #     if (self.E2(sintExpression)):
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

    # E2 -> E3 lineE2
    def E2(self, varE2):
        varE3 = sintE2 = herdE2 = C3E()
        if (self.E3(varE2)):
            herdE2.place = varE3.place
            herdE2.code  = varE3.code
            if (self.lineE2(herdE2, sintE2)):
                varE2.place = sintE2.place
                varE2.code = sintE2.code
                return True
            else:
                return False
        else:
            return False


    # lineE2 -> || E3 lineE2 | vazio
    def lineE2(self, herdE2, sintE2):
        varE3 = sintE2Linha = herdE2Linha = C3E()
        if (self.currentToken == 'TK_OR'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E3(varE3)):
                herdE2Linha.place = self.createTemp()
                herdE2Linha.code = f'{herdE2.code + varE3.code + herdE2Linha.place} = {herdE2.place + op + varE3.place}\n'
                if (self.lineE2(herdE2Linha, sintE2Linha)):
                    sintE2.place = sintE2Linha.place
                    sintE2.code = sintE2Linha.code
                    return True
                else:
                    return False
        sintE2.place = herdE2.place
        sintE2.code = herdE2.code
        return True

    #E3 -> E4 lineE3
    def E3(self, varE3):
        varE4 = sintE3 = herdE3 = C3E()
        if (self.E4(varE3)):
            herdE3.place = varE4.place
            herdE3.code  = varE4.code
            if (self.lineE2(herdE3, sintE3)):
                varE3.place = sintE3.place
                varE3.code = sintE3.code
                return True
            else:
                return False
        else:
            return False

    #lineE3 -> && E4 lineE3 | vazio
    def lineE3(self, herdE3, sintE3):
        varE4 = sintE3Linha = herdE3Linha = C3E()
        if (self.currentToken == 'TK_AND'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E4(varE4)):
                herdE3Linha.place = self.createTemp()
                herdE3Linha.code = f'{herdE3.code + varE4.code + herdE3Linha.place} = {herdE3.place + op + varE4.place}\n'
                if (self.lineE3(herdE3Linha, sintE3Linha)):
                    sintE3.place = sintE3Linha.place
                    sintE3.code = sintE3Linha.code
                    return True
                else:
                    return False
        sintE3.place = herdE3.place
        sintE3.code = herdE3.code
        return True
    #E4 -> E5 lineE4'
    def E4(self, varE4):
        varE5 = sintE4 = herdE4 = C3E()
        if (self.E5(varE5)):
            herdE4.place = varE4.place
            herdE4.code  = varE4.code
            if (self.lineE4(herdE4, sintE4)):
                varE4.place = sintE4.place
                varE4.code  = sintE4.code
                return True
            else:
                return False
        else:
            return False
    def lineE4(self, herdE4, sintE4):
        varE5 = sintE4Linha = herdE4Linha = C3E()
        if (self.currentToken == 'TK_LOGICOR'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E5(varE5)):
                herdE4Linha.place = self.createTemp()
                herdE4Linha.code = f'{herdE4.code + varE5.code + herdE4Linha.place} = {herdE4.place + op + varE5.place}\n'
                if (self.lineE4(herdE4Linha, sintE4Linha)):
                    sintE4.place = sintE4Linha.place
                    sintE4.code = sintE4Linha.code
                    return True
                else:
                    return False
        sintE4.place = herdE4.place
        sintE4.code = herdE4.code
        return True

    #E5 -> E6 lineE5
    def E5(self, varE5):
        varE6 = sintE5 = herdE5 = C3E()
        if (self.E6(varE6)):
            herdE5.place = varE5.place
            herdE5.code  = varE5.code
            if (self.lineE5(herdE5, sintE5)):
                varE5.place = sintE5.place
                varE5.code  = sintE5.code
                return True
            else:
                return False
        else:
            return False
    #E5' -> | E6 E5' | e
    def lineE5(self, herdE5, sintE5):
        varE6 = sintE5Linha = herdE5Linha = C3E()
        if (self.currentToken == 'TK_CIRCUMFLEX'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E6(varE6)):
                herdE5Linha.place = self.createTemp()
                herdE5Linha.code = f'{herdE5.code + varE6.code + herdE5Linha.place} = {herdE5.place + op + varE6.place}\n'
                if (self.lineE5(herdE5Linha, sintE5Linha)):
                    sintE5.place = sintE5Linha.place
                    sintE5.code = sintE5Linha.code
                    return True
                else:
                    return False
        sintE5.place = herdE5.place
        sintE5.code = herdE5.code
        return True

    def E6(self, varE6):
        varE7 = sintE6 = herdE6 = C3E()
        if (self.E7(varE7)):
            herdE6.place = varE6.place
            herdE6.code  = varE6.code
            if (self.lineE6(herdE6, sintE6)):
                varE6.place = sintE6.place
                varE6.code  = sintE6.code
                return True
            else:
                return False
        else:
            return False

    def lineE6(self, herdE6, sintE6):
        varE7 = sintE6Linha = herdE6Linha = C3E()
        if (self.currentToken == 'TK_LOGICAND'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E7(varE7)):
                herdE6Linha.place = self.createTemp()
                herdE6Linha.code = f'{herdE6.code + varE7.code + herdE6Linha.place} = {herdE6.place + op + varE7.place}\n'
                if (self.lineE6(herdE6Linha, sintE6Linha)):
                    sintE6.place = sintE6Linha.place
                    sintE6.code = sintE6Linha.code
                    return True
                else:
                    return False
        sintE6.place = herdE6.place
        sintE6.code = herdE6.code
        return True

    def E7(self, varE7):
        varE8 = sintE7 = herdE7 = C3E()
        if (self.E8(varE8)):
            herdE7.place = varE7.place
            herdE7.code  = varE7.code
            if (self.lineE7(herdE7, sintE7)):
                varE7.place = sintE7.place
                varE7.code  = sintE7.code
                return True
            else:
                return False
        else:
            return False

    def lineE7(self, herdE7, sintE7):
        varE8 = sintE7Linha = herdE7Linha = C3E()
        if (self.currentToken == 'TK_EQUALEQUAL' or self.currentToken == 'TK_NOTEQUAL'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E8(varE8)):
                herdE7Linha.place = self.createTemp()
                herdE7Linha.code = f'{herdE7.code + varE8.code + herdE7Linha.place} = {herdE7.place + op + varE8.place}\n'
                if (self.lineE7(herdE7Linha, sintE7Linha)):
                    sintE7.place = sintE7Linha.place
                    sintE7.code = sintE7Linha.code
                    return True
                else:
                    return False
        sintE7.place = herdE7.place
        sintE7.code = herdE7.code
        return True

    def E8(self, varE8):
        varE9 = sintE8 = herdE8 = C3E()
        if (self.E9(varE9)):
            herdE8.place = varE8.place
            herdE8.code  = varE8.code
            if (self.lineE8(herdE8, sintE8)):
                varE8.place = sintE8.place
                varE8.code  = sintE8.code
                return True
            else:
                return False
        else:
            return False

    def lineE8(self, herdE8, sintE8):
        varE9 = sintE8Linha = herdE8Linha = C3E()
        if (self.currentToken == 'TK_LESS' or self.currentToken == 'TK_GREATER' or
            self.currentToken == 'TK_LESSEQUAL' or self.currentToken == 'TK_GREATEREQUAL'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E9(varE9)):
                herdE8Linha.place = self.createTemp()
                herdE8Linha.code = f'{herdE8.code + varE9.code + herdE8Linha.place} = {herdE8.place + op + varE9.place}\n'
                if (self.lineE8(herdE8Linha, sintE8Linha)):
                    sintE8.place = sintE8Linha.place
                    sintE8.code = sintE8Linha.code
                    return True
                else:
                    return False
        sintE8.place = herdE8.place
        sintE8.code = herdE8.code
        return True

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

