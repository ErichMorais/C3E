DEBUG = False
class threeAddressCode(object):
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
        self.nextToken()

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
    resultCode = threeAddressCode()
        
    def nextToken(self):
        self.index = self.index + 1
        if(self.index < len(self.tokenList)):
            self.currentToken = self.tokenList[self.index].token
        else:
            self.currentToken = None
        
    def currentRow(self):
        return self.tokenList[self.index].row

    def currentColumn(self):
        return self.tokenList[self.index].col
    
    def currentLexeme(self): 
        return self.tokenList[self.index].lexeme

    def alreadyExists(self):
        symb = filter(lambda s: s.lexeme == self.currentLexeme(),self.symbolTable)
        try:
            next(symb)
            # TODO Adicionar reconhecimento de escopo
            return True
        except:
            return False

    def newTemp(self):
        self.tempCont += 1
        return f'T{self.tempCont}'
    
    def newLabel(self):
        self.labelCont += 1
        return f'L{self.labelCont}'
    
    def verifyExistance(self, rcvVar):
        symb = filter(lambda s: s.lexeme == self.currentLexeme(),self.symbolTable)
        try:
            next(symb)
            return False
        except:
            rcvVar.scope = self.currentScope
            rcvVar.lexeme = self.currentLexeme()
            self.symbolTable.append(rcvVar)
            
        return True
            
    
    def analyser(self):
        ld = threeAddressCode()
        if (self.LD(ld)):
            self.resultCode.code += ld.code
            if (self.currentToken == 'TK_EOF'):
                return True
        return False

    def LD(self, ld):
        dec = threeAddressCode()
        if (self.DEC(dec)):
            #print(dec)
            ld.code += dec.code
            rld = threeAddressCode()
            if (self.RLD(rld)):
                ld.code += rld.code
                Debug(f'Debug73: {ld.place} || {ld.code}')
                return True
            else: return False
        else: return False

    def RLD(self, rld):
        ld = threeAddressCode()
        if (self.LD(ld)):
            #print(ld)
            rld.code += ld.code
            Debug(f'Debug72: {rld.place} || {rld.code}')
            return True
        else: return True

    def DEC(self, dec):
        var = Variable()
        if (self.Type(var)):
            #print(var)
            self.nextToken()
            if (self.currentToken == "TK_ID"):
                if (not self.verifyExistance(var)):
                    print(f"Variável {var.lexeme} já está em uso.", )
                    return False
                self.nextToken()
                if (self.RDEC(dec, var)):
                        return True
                else:
                    return False
            else:
                print(f"Erro: esperava token 'id' na linha {self.currentRow()} coluna {self.currentColumn()}.")
                return False           
        else: return False
        
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
            df = threeAddressCode()
            if(self.DF(df)):
                dec.code += df.code
                Debug(f'Debug71: {dec.place} || {dec.code}')
                return True
            else:
                return False
        elif self.currentToken == "TK_SEMICOLON":
            self.nextToken()
            return True
        elif self.currentToken == "TK_EQUAL":
            self.nextToken()
            constant = self.currentLexeme()
            aux = self.newTemp()
            if(var.type == 'int'):
                if self.currentToken == "TK_CONST_INT":
                    self.nextToken()
                    if(self.currentToken == "TK_SEMICOLON"):
                        dec.code += f"{aux} = {constant}\n{var.lexeme} = {aux}\n"
                        Debug(f'Debug70: {dec.place} || {dec.code}')
                        self.nextToken()
                        return True
                    else:
                        ##TODO CRIAR ALERTAS
                        print(f'Erro: esperava o token ";" na linha {self.currentRow()} coluna ${self.currentColumn()}.')
                        return False
                else:
                    #TODO CRIAR ALERTAS
                    print(f'Erro: esperava o token "const_int" na linha {self.currentRow()} coluna ${self.currentColumn()}.')

                    return False
            if(var.type == 'float'):
                if self.currentToken == "TK_CONST_REAL":
                    self.nextToken()
                    if(self.currentToken == "TK_SEMICOLON"):
                        dec.code += f"{aux} = {constant}\n {var.lexeme} = {aux}"
                        Debug(f'Debug69: {dec.place} || {dec.code}')
                        self.nextToken()
                        return True
                    else:
                        print(f'Erro: esperava o token ";" na linha {self.currentRow()} coluna ${self.currentColumn()}.')                        
                        return False
                else:
                    print(f'Erro: esperava o token "const_real" na linha {self.currentRow()} coluna ${self.currentColumn()}.')
                    return False
            else:
                print(f'Erro: esperava o o tipo int ou float na linha {self.currentRow()} coluna ${self.currentColumn()}.')
                return False
        else:
                print(f'Erro: esperava o  ;, ) ou , na linha {self.currentRow()} coluna ${self.currentColumn()}.')
                return False

    def DV(self, rcvtype):
        var = Variable()
        var.type = rcvtype
        if (self.currentToken == 'TK_ID'):
            if (not self.verifyExistance(var)):
                return False
            self.nextToken()
            if( self.RDV(rcvtype)):
                return True
            else:
                return False
        else:
            print(f"Erro: esperava token 'id' na linha {self.currentRow()} coluna {self.currentColumn()}.")
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
            print(f"Erro: esperava token , ou ; na linha {self.currentRow()} coluna {self.currentColumn()}.")
            return False

    def DF(self, df):
        if(self.LP()):
            if (self.currentToken == 'TK_RIGHTPAR'):
                self.nextToken()
                threeAddressCodeBlock = threeAddressCode()
                if (self.blockCode(threeAddressCodeBlock)):
                    df.code += threeAddressCodeBlock.code
                    Debug(f'Debug68: {df.place} || {df.code}')
                    return True
                elif(self.currentToken == 'TK_SEMICOLON'):
                    self.currentScope = 'Global'
                    self.nextToken()
                    return True
                else:
                    print(f"Erro: esperava token "+ '{' + f"ou ; na linha {self.currentRow()} coluna {self.currentColumn()}.")
                    return False
            else:
                    print(f"Erro: esperava token "+ ')' + f"ou ; na linha {self.currentRow()} coluna {self.currentColumn()}.")
                    return False
        else:
            return False

    def LP(self):
        var = Variable()
        if (self.Type(var)):
            self.nextToken()
            if self.currentToken == 'TK_ID':
                if (not self.verifyExistance(var)):
                    return False
                self.nextToken()
                if (self.RLP()):
                    return True
                else:
                    return False
            else:
                print(f"Erro: esperava token 'id' na linha {self.currentRow()} coluna {self.currentColumn()}.")
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
                    if (not self.verifyExistance(var)):
                        return False
                    self.nextToken()
                    if (self.RLP()):
                        return True
                    else:
                        return False
                else:
                    print(f"Erro: esperava token 'id' na linha {self.currentRow()} coluna {self.currentColumn()}.")
                    return False
            else:
                return False
        else:
            return True
    
    def blockCode(self, threeAddressCodeBlock):
        if(self.currentToken == 'TK_LEFTBRAC'):
            self.nextToken()
            lcd = threeAddressCode()
            if(self.LCD(lcd)):
                threeAddressCodeBlock.code += lcd.code
                Debug(f'Debug67: {threeAddressCodeBlock.place} || {threeAddressCodeBlock.code}')
                if(self.currentToken == 'TK_RIGHTBRAC'):
                    self.currentScope = 'Global'
                    self.nextToken()
                    return True
                else:
                    print(f"Erro: esperava token "+ '}' + f"ou ; na linha {self.currentRow()} coluna {self.currentColumn()}.")
        return False

    def LCD(self, lcd):
        var = Variable()
        cmd = threeAddressCode()
        if(self.COM(cmd)):
            lcd.code += cmd.code
            Debug(f'Debug66: {lcd.place} || {lcd.code}')
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
        expression = threeAddressCode()
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
                Debug(f'Debug65: {cmd.place} || {cmd.code}')
                self.COM(cmd)
                return True
            return False
        elif(self.currentToken == "TK_CONTINUE"):
            self.nextToken()
            if(self.currentToken == "TK_SEMICOLON"):
                self.nextToken()
                cmd.code += f'goto {self.tempContinue}\n'
                Debug(f'Debug64: {cmd.place} || {cmd.code}')
                self.COM(cmd)
                return True
            return False
        elif (self.Type(var)) :
            self.nextToken()    
            if(self.currentToken == 'TK_ID'):
                if (not self.verifyExistance(var)):
                    return False
                self.nextToken()  
                rdec = threeAddressCode()  
                if(self.RDEC(rdec, var)):
                    cmd.code +=rdec.code
                    Debug(f'Debug63: {cmd.place} || {cmd.code}')
                    return True
                else:
                    return False
            else:
                print(f"Erro: esperava token 'id' na linha {self.currentRow()} coluna {self.currentColumn()}.")
                return False
        elif(self.E(expression)):
            cmd.code += expression.code
            Debug(f'Debug62: {cmd.place} || {cmd.code}')
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
                print(f"Erro: esperava token ; na linha {self.currentRow()} coluna {self.currentColumn()}.")
                return False
        else:
            return False

    def IFcommand(self, rcvCode):
        expression = threeAddressCode()
        threeAddressCodeBlock = threeAddressCode()
        elseCmd =  threeAddressCode()
        if(self.currentToken == "TK_LEFTPAR"):
            self.nextToken()
            if(self.E(expression)):
                if(self.currentToken == "TK_RIGHTPAR"):
                    self.nextToken()
                    if(self.blockCode(threeAddressCodeBlock)):
                        endLabel = self.newLabel()
                        sintElse = self.ELSEcommand("", endLabel, elseCmd)
                        rcvCode.code = expression.code + f'if {expression.place} = 0 goto {sintElse}\n' + threeAddressCodeBlock.code +elseCmd.code+f'{endLabel}:\n'
                        Debug(f'Debug61: {rcvCode.place} || {rcvCode.code}')
                        return True
        return False

    def ELSEcommand(self,sintElse, endLabel, elseCmd):
        threeAddressCodeBlock = threeAddressCode()
        if(self.currentToken == "TK_ELSE"):
            self.nextToken()
            if(self.blockCode(threeAddressCodeBlock)):
                elseLabel = self.newLabel()
                elseCmd.code = f'goto {endLabel} \n{elseLabel}:\n' + threeAddressCodeBlock.code
                Debug(f'Debug60: {elseCmd.place} || {elseCmd.code}')
                sintElse = elseLabel
                return sintElse
        sintElse = endLabel
        return sintElse

    def WHILEcommand(self, rcvCode):
        expression =  threeAddressCode()
        threeAddressCodeBlock = threeAddressCode()
        if(self.currentToken == "TK_LEFTPAR"):
            self.nextToken()
            if(self.E(expression)):
                if(self.currentToken == "TK_RIGHTPAR"):
                    self.nextToken()
                    self.tempContinue = iLabel = self.newLabel()
                    self.tempFim = fLabel = self.newLabel()
                    if(self.blockCode(threeAddressCodeBlock)):
                        rcvCode.code = f'{iLabel}:\n{expression.code}if {expression.place} = 0 goto {fLabel}\n{threeAddressCodeBlock.code}goto {iLabel}\n{fLabel}:\n'
                        Debug(f'Debug59: {rcvCode.place} || {rcvCode.code}')
                        return True
        return False

    def DOWHILEcommand(self,rcvCode):
        expression  = threeAddressCode()
        threeAddressCodeBlock = threeAddressCode()
        iLabel = self.newLabel()
        fLabel = self.newLabel()
        self.tempFim = fLabel
        self.tempContinue = iLabel
        if(self.blockCode(threeAddressCodeBlock)):
            if(self.currentToken == "TK_WHILE"):
                self.nextToken()
                if(self.currentToken == "TK_LEFTPAR"):
                    self.nextToken()
                    if(self.E(expression)):
                        if(self.currentToken == "TK_RIGHTPAR"):
                            self.nextToken()
                            if(self.currentToken == "TK_SEMICOLON"):
                                self.nextToken()
                                rcvCode.code =  f'{iLabel}:\n{threeAddressCodeBlock.code + expression.code}if {expression.place} = 0 goto {fLabel}\n'
                                rcvCode.code += f'goto {iLabel}\n{fLabel}:\n'
                                Debug(f'Debug58: {rcvCode.place} || {rcvCode.code}')
                                return True
        return False

    def FORcommand(self, rcvCode):
        firstExp = threeAddressCode()
        secExp = threeAddressCode()
        trdExp = threeAddressCode()
        threeAddressCodeBlock = threeAddressCode()

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
                                    iLabel = self.newLabel()
                                    self.tempFim = fLabel = self.newLabel()
                                    self.tempContinue = self.newLabel()
                                    if(self.blockCode(threeAddressCodeBlock)):
                                        rcvCode.code = firstExp.code + f'{iLabel}:\n{secExp.code}if {secExp.place} = 0 goto {fLabel}\n{threeAddressCodeBlock.code+self.tempContinue}:\n{trdExp.code}goto {iLabel}\n{fLabel}:\n'
                                        Debug(f'Debug57: {rcvCode.place} || {rcvCode.code}')
                                        return True
        return False     
    #*************************************************************EXPRESSÕES*****************************************************************************
    #E -> lineE E1
    def E(self, E): 
        varE1 = threeAddressCode()
        sintE = threeAddressCode()
        herdE = threeAddressCode()
        if (self.E1(varE1)):
            herdE.place = varE1.place
            herdE.code = varE1.code
            Debug(f'Debug56: {herdE.place} || {herdE.code}')
            if (self.lineE(herdE, sintE)):
                E.place = sintE.place
                E.code = sintE.code
                Debug(f'Debug55: {E.place} || {E.code}')
                return True
            else: 
                return False
        else: 
            return False
    
    #lineE -> ,E1 lineE | vazio
    def lineE(self, herdE, sintE):
        varE1 = threeAddressCode()
        sintELinha = threeAddressCode()
        herdELinha = threeAddressCode()
        if (self.currentToken == 'TK_COMMA'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E1(varE1)):
                herdELinha.place = self.newTemp()
                herdELinha.code = (herdE.code + varE1.code + 
                f'{herdELinha.place} = {herdE.place} {op} {varE1.place}\n')
                Debug(f'Debug54: {herdELinha.place} || {herdELinha.code}')
                if (self.lineE(herdELinha, sintELinha)):
                    sintE.code = sintELinha.code
                    sintE.place = sintELinha.place
                    Debug(f'Debug53: {sintE.place} || {sintE.code}')
                    return True
                else:
                    return False
        sintE.place = herdE.place
        sintE.code = herdE.code
        Debug(f'Debug52: {sintE.place} || {sintE.code}')
        return True

    #E1 -> E2 = E1 | E2 += E1 | E2 -= E1 | E2 *= E1 | E2 ÷= E1 | E2 %= E1 E2
    def E1(self, varE1):
        herdE1 = threeAddressCode()
        varE2 = threeAddressCode()
        if (self.E2(varE2)):
            if (self.currentToken == 'TK_EQUAL' or self.currentToken == 'TK_STAREQUAL' or self.currentToken == 'TK_SLASHEQUAL'
                or self.currentToken == 'TK_PERCENTEQUAL' or self.currentToken == 'TK_PLUSEQUAL' or self.currentToken == 'TK_MINEQUAL'):
                op = self.currentLexeme()
                self.nextToken()
                if (self.E1(herdE1)):
                    varE1.place = herdE1.place
                    if (op == '='):
                        varE1.code = f'{herdE1.code + varE2.code + varE2.place} = {varE1.place}\n'
                        Debug(f'Debug51: {varE1.place} || {varE1.code}')
                    else:
                        varE1.code = f'{herdE1.code + varE2.code + varE2.place} = {varE2.place}{op[0]}{varE1.place}\n'
                        Debug(f'Debug50: {varE1.place} || {varE1.code}')
                    return True
                else:
                    return False      
            else:
                varE1.place = varE2.place
                varE1.code = varE2.code
                Debug(f'Debug49: {varE1.place} || {varE1.code}')
                return True
        else:
            return False

    # E2 -> E3 lineE2
    def E2(self, varE2):
        varE3 = threeAddressCode()
        sintE2 = threeAddressCode()
        herdE2 = threeAddressCode()
        if (self.E3(varE3)):
            herdE2.place = varE3.place
            herdE2.code  = varE3.code
            Debug(f'Debug48: {herdE2.place} || {herdE2.code}')
            if (self.lineE2(herdE2, sintE2)):
                varE2.place = sintE2.place
                varE2.code = sintE2.code
                Debug(f'Debug47: {varE2.place} || {varE2.code}')
                return True
            else:
                return False
        else:
            return False

    # lineE2 -> || E3 lineE2 | vazio
    def lineE2(self, herdE2, sintE2):
        varE3 = threeAddressCode()
        sintE2Linha = threeAddressCode() 
        herdE2Linha = threeAddressCode()
        if (self.currentToken == 'TK_OR'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E3(varE3)):
                herdE2Linha.place = self.newTemp()
                herdE2Linha.code = f'{herdE2.code + varE3.code + herdE2Linha.place} = {herdE2.place + op + varE3.place}\n'
                Debug(f'Debug46: {herdE2Linha.place} || {herdE2Linha.code}')
                if (self.lineE2(herdE2Linha, sintE2Linha)):
                    sintE2.place = sintE2Linha.place
                    sintE2.code = sintE2Linha.code
                    Debug(f'Debug45: {sintE2.place} || {sintE2.code}')
                    return True
                else:
                    return False
        sintE2.place = herdE2.place
        sintE2.code = herdE2.code
        Debug(f'Debug44: {sintE2.place} || {sintE2.code}')
        return True

    #E3 -> E4 lineE3
    def E3(self, varE3):
        varE4 = threeAddressCode()
        sintE3 = threeAddressCode()
        herdE3 = threeAddressCode()
        if (self.E4(varE4)):
            herdE3.place = varE4.place
            herdE3.code  = varE4.code
            Debug(f'Debug43: {herdE3.place} || {herdE3.code}')
            if (self.lineE3(herdE3, sintE3)):
                varE3.place = sintE3.place
                varE3.code = sintE3.code
                Debug(f'Debug42: {varE3.place} || {varE3.code}')
                return True
            else:
                return False
        else:
            return False

    #lineE3 -> && E4 lineE3 | vazio
    def lineE3(self, herdE3, sintE3):
        varE4 = threeAddressCode()
        sintE3Linha = threeAddressCode()
        herdE3Linha = threeAddressCode()
        if (self.currentToken == 'TK_AND'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E4(varE4)):
                herdE3Linha.place = self.newTemp()
                herdE3Linha.code = f'{herdE3.code + varE4.code + herdE3Linha.place} = {herdE3.place + op + varE4.place}\n'
                Debug(f'Debug41: {herdE3Linha.place} || {herdE3Linha.code}')
                if (self.lineE3(herdE3Linha, sintE3Linha)):
                    sintE3.place = sintE3Linha.place
                    sintE3.code = sintE3Linha.code
                    Debug(f'Debug40: {sintE3.place} || {sintE3.code}')
                    return True
                else:
                    return False
        sintE3.place = herdE3.place
        sintE3.code = herdE3.code
        Debug(f'Debug39: {sintE3.place} || {sintE3.code}')
        return True
    #E4 -> E5 lineE4'
    def E4(self, varE4):
        varE5 = threeAddressCode()
        sintE4 = threeAddressCode()
        herdE4 = threeAddressCode()
        if (self.E5(varE5)):
            herdE4.place = varE5.place
            herdE4.code  = varE5.code
            Debug(f'Debug38: {herdE4.place} || {herdE4.code}')
            if (self.lineE4(herdE4, sintE4)):
                varE4.place = sintE4.place
                varE4.code  = sintE4.code
                Debug(f'Debug37: {varE4.place} || {varE4.code}')
                return True
            else:
                return False
        else:
            return False
    def lineE4(self, herdE4, sintE4):
        varE5 = threeAddressCode()
        sintE4Linha = threeAddressCode()
        herdE4Linha = threeAddressCode()
        if (self.currentToken == 'TK_LOGICOR'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E5(varE5)):
                herdE4Linha.place = self.newTemp()
                herdE4Linha.code = f'{herdE4.code + varE5.code + herdE4Linha.place} = {herdE4.place + op + varE5.place}\n'
                Debug(f'Debug36: {herdE4Linha.place} || {herdE4Linha.code}')
                if (self.lineE4(herdE4Linha, sintE4Linha)):
                    sintE4.place = sintE4Linha.place
                    sintE4.code = sintE4Linha.code
                    Debug(f'Debug35: {sintE4.place} || {sintE4.code}')
                    return True
                else:
                    return False
        sintE4.place = herdE4.place
        sintE4.code = herdE4.code
        Debug(f'Debug34: {sintE4.place} || {sintE4.code}')
        return True

    #E5 -> E6 lineE5
    def E5(self, varE5):
        varE6 = threeAddressCode()
        sintE5 = threeAddressCode()
        herdE5 = threeAddressCode()
        if (self.E6(varE6)):
            herdE5.place = varE6.place
            herdE5.code  = varE6.code
            Debug(f'Debug33: {herdE5.place} || {herdE5.code}')
            if (self.lineE5(herdE5, sintE5)):
                varE5.place = sintE5.place
                varE5.code  = sintE5.code
                Debug(f'Debug32: {varE5.place} || {varE5.code}')
                return True
            else:
                return False
        else:
            return False
    #E5' -> | E6 E5' | e
    def lineE5(self, herdE5, sintE5):
        varE6 = threeAddressCode()
        sintE5Linha = threeAddressCode() 
        herdE5Linha = threeAddressCode()
        if (self.currentToken == 'TK_CIRCUMFLEX'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E6(varE6)):
                herdE5Linha.place = self.newTemp()
                herdE5Linha.code = f'{herdE5.code + varE6.code + herdE5Linha.place} = {herdE5.place + op + varE6.place}\n'
                Debug(f'Debug31: {herdE5Linha.place} || {herdE5Linha.code}')
                if (self.lineE5(herdE5Linha, sintE5Linha)):
                    sintE5.place = sintE5Linha.place
                    sintE5.code = sintE5Linha.code
                    Debug(f'Debug30: {sintE5.place} || {sintE5.code}')
                    return True
                else:
                    return False
        sintE5.place = herdE5.place
        sintE5.code = herdE5.code
        Debug(f'Debug29: {sintE5.place} || {sintE5.code}')
        return True

    def E6(self, varE6):
        varE7 = threeAddressCode()
        sintE6 = threeAddressCode()
        herdE6 = threeAddressCode()
        if (self.E7(varE7)):
            herdE6.place = varE7.place
            herdE6.code  = varE7.code
            Debug(f'Debug28: {herdE6.place} || {herdE6.code}')
            if (self.lineE6(herdE6, sintE6)):
                varE6.place = sintE6.place
                varE6.code  = sintE6.code
                Debug(f'Debug27: {varE6.place} || {varE6.code}')
                return True
            else:
                return False
        else:
            return False

    def lineE6(self, herdE6, sintE6):
        varE7 =  threeAddressCode()
        sintE6Linha = threeAddressCode() 
        herdE6Linha = threeAddressCode()
        if (self.currentToken == 'TK_LOGICAND'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E7(varE7)):
                herdE6Linha.place = self.newTemp()
                herdE6Linha.code = f'{herdE6.code + varE7.code + herdE6Linha.place} = {herdE6.place + op + varE7.place}\n'
                Debug(f'Debug26: {herdE6Linha.place} || {herdE6Linha.code}')
                if (self.lineE6(herdE6Linha, sintE6Linha)):
                    sintE6.place = sintE6Linha.place
                    sintE6.code = sintE6Linha.code
                    Debug(f'Debug25: {sintE6.place} || {sintE6.code}')
                    return True
                else:
                    return False
        sintE6.place = herdE6.place
        sintE6.code = herdE6.code
        Debug(f'Debug24: {sintE6.place} || {sintE6.code}')
        return True

    def E7(self, varE7):
        varE8 = threeAddressCode()
        sintE7 = threeAddressCode()
        herdE7 = threeAddressCode()
        if (self.E8(varE8)):
            herdE7.place = varE8.place
            herdE7.code  = varE8.code
            Debug(f'Debug23: {herdE7.place} || {herdE7.code}')
            if (self.lineE7(herdE7, sintE7)):
                varE7.place = sintE7.place
                varE7.code  = sintE7.code
                Debug(f'Debug22: {varE7.place} || {varE7.code}')
                return True
            else:
                return False
        else:
            return False

    def lineE7(self, herdE7, sintE7):
        varE8 = threeAddressCode()
        sintE7Linha = threeAddressCode() 
        herdE7Linha = threeAddressCode()
        if (self.currentToken == 'TK_EQUALEQUAL' or self.currentToken == 'TK_NOTEQUAL'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E8(varE8)):
                herdE7Linha.place = self.newTemp()
                herdE7Linha.code = f'{herdE7.code + varE8.code + herdE7Linha.place} = {herdE7.place + op + varE8.place}\n'
                Debug(f'Debug21: {herdE7Linha.place} || {herdE7Linha.code}')
                if (self.lineE7(herdE7Linha, sintE7Linha)):
                    sintE7.place = sintE7Linha.place
                    sintE7.code = sintE7Linha.code
                    Debug(f'Debug20: {sintE7.place} || {sintE7.code}')
                    return True
                else:
                    return False
        sintE7.place = herdE7.place
        sintE7.code = herdE7.code
        Debug(f'Debug19: {sintE7.place} || {sintE7.code}')
        return True

    def E8(self, varE8):
        varE9 = threeAddressCode()
        sintE8 = threeAddressCode()
        herdE8 = threeAddressCode()
        if (self.E9(varE9)):
            herdE8.place = varE9.place
            herdE8.code  = varE9.code
            Debug(f'Debug18: {herdE8.place} || {herdE8.code}')
            if (self.lineE8(herdE8, sintE8)):
                varE8.place = sintE8.place
                varE8.code  = sintE8.code
                Debug(f'Debug17: {varE8.place} || {varE8.code}')
                return True
            else:
                return False
        else:
            return False

    def lineE8(self, herdE8, sintE8):
        varE9 = threeAddressCode()
        sintE8Linha = threeAddressCode() 
        herdE8Linha = threeAddressCode()
        if (self.currentToken == 'TK_LESS' or self.currentToken == 'TK_GREATER' or
            self.currentToken == 'TK_LESSEQUAL' or self.currentToken == 'TK_GREATEREQUAL'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E9(varE9)):
                herdE8Linha.place = self.newTemp()
                herdE8Linha.code = f'{herdE8.code + varE9.code + herdE8Linha.place} = {herdE8.place + op + varE9.place}\n'
                Debug(f'Debug16: {herdE8Linha.place} || {herdE8Linha.code}')
                if (self.lineE8(herdE8Linha, sintE8Linha)):
                    sintE8.place = sintE8Linha.place
                    sintE8.code = sintE8Linha.code
                    Debug(f'Debug15: {sintE8.place} || {sintE8.code}')
                    return True
                else:
                    return False
        sintE8.place = herdE8.place
        sintE8.code = herdE8.code
        Debug(f'Debug14: {sintE8.place} || {sintE8.code}')
        return True

    def E9(self, varE9):
        varE10 = threeAddressCode()
        sintE9 = threeAddressCode()
        herdE9 = threeAddressCode()
        if (self.E10(varE10)):
            herdE9.place = varE10.place
            herdE9.code  = varE10.code
            Debug(f'Debug13: {herdE9.place} || {herdE9.code}')
            if (self.lineE9(herdE9, sintE9)):
                varE9.place = sintE9.place
                varE9.code  = sintE9.code
                Debug(f'Debug12: {varE9.place} || {varE9.code}')
                return True
            else:
                return False
        else:
            return False

    def lineE9(self, herdE9, sintE9):
        varE10 = threeAddressCode()
        sintE9Linha = threeAddressCode() 
        herdE9Linha = threeAddressCode()
        if (self.currentToken == 'TK_PLUS' or self.currentToken == 'TK_MINUS'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E10(varE10)):
                herdE9Linha.place = self.newTemp()
                herdE9Linha.code = f'{herdE9.code + varE10.code + herdE9Linha.place} = {herdE9.place + op + varE10.place}\n'
                Debug(f'Debug11: {herdE9Linha.place} || {herdE9Linha.code}')
                if (self.lineE9(herdE9Linha, sintE9Linha)):
                    sintE9.place = sintE9Linha.place
                    sintE9.code = sintE9Linha.code
                    Debug(f'Debug10: {sintE9.place} || {sintE9.code}')
                    return True
                else:
                    return False
        sintE9.place = herdE9.place
        sintE9.code = herdE9.code
        Debug(f'Debug9: {sintE9.place} || {sintE9.code}')
        return True

    def E10(self, varE10):
        varE11 = threeAddressCode()
        sintE10 = threeAddressCode()
        herdE10 = threeAddressCode()
        if (self.E11(varE11)):
            herdE10.place = varE11.place
            herdE10.code  = varE11.code
            Debug(f'Debug8: {herdE10.place} || {herdE10.code}')
            if (self.lineE10(herdE10, sintE10)):
                varE10.place = sintE10.place
                varE10.code  = sintE10.code
                Debug(f'Debug7: {varE10.place} || {varE10.code}')
                return True
            else:
                return False
        else:
            return False

    def lineE10(self, herdE10, sintE10):
        varE11 = threeAddressCode()
        sintE10Linha = threeAddressCode() 
        herdE10Linha = threeAddressCode()
        if (self.currentToken == 'TK_STAR' or self.currentToken == 'TK_SLASH' or self.currentToken == 'TK_PERCENT'):
            op = self.currentLexeme()
            self.nextToken()
            if (self.E11(varE11)):
                herdE10Linha.place = self.newTemp()
                herdE10Linha.code = f'{herdE10.code + varE11.code + herdE10Linha.place} = {herdE10.place + op + varE11.place}\n'
                Debug(f'Debug6: {herdE10Linha.place} || {herdE10Linha.code}')
                if (self.lineE10(herdE10Linha, sintE10Linha)):
                    sintE10.place = sintE10Linha.place
                    sintE10.code = sintE10Linha.code
                    Debug(f'Debug5: {sintE10.place} || {sintE10.code}')
                    return True
                else:
                    return False
        sintE10.place = herdE10.place
        sintE10.code = herdE10.code
        Debug(f'Debug4: {sintE10.place} || {sintE10.code}')
        return True
    
    # E11 -> cte | id RE | (E)
    def E11(self,varE11):
        if (self.currentToken == "TK_CONST_INT" or self.currentToken == "TK_CONST_REAL"):
            tempAtr = self.newTemp()
            varE11.code += f'{tempAtr} = {self.currentLexeme()}\n'
            varE11.place = tempAtr
            Debug(f'Debug3: {varE11.place} || {varE11.code}')
            self.nextToken()
            return True
        elif (self.currentToken == "TK_ID"):
            if (not self.alreadyExists()):
                print(f'Erro: variável {self.currentLexeme()} não declarada.')
                return False

            varE11.code = ""
            varE11.place = self.currentLexeme()
            Debug(f'Debug2: {varE11.place} || {varE11.code}')
            self.nextToken()
            if (self.RE()):
                return True
            else:
                return False
        elif (self.currentToken == "TK_LEFTPAR"):
            self.nextToken()
            exp = threeAddressCode()
            if (self.E(exp)):
                varE11.place = exp.place
                varE11.code = exp.code
                Debug(f'Debug1: {varE11.place} || {varE11.code}')
                if (self.currentToken == "TK_RIGHTPAR"):
                    self.nextToken()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    
    # RE -> (LP) | e
    def RE(self):
        if(self.currentToken == "TK_LEFTPAR"):
            self.nextToken()
            if (self.LP()):
                if (self.currentToken == "TK_RIGHTPAR"):
                    self.nextToken()
                    return True
                else:
                    print(f'Erro: esperava token ")" na linha {self.currentRow()} coluna {self.currentColumn()}.')
                    return False
            else:
                return False
        else:
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

def Debug(strmsg):
    if DEBUG:
        print(strmsg)
