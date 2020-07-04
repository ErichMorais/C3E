class C3E(object):
    def __init__(self, place = '', code = ''):
        self.place = place
        self.code = code
class Syntatic(object):
    def __init__(self):
        pass
    
    resultC3E = C3E()
    index = -1
    currentToken = ''
    currentScope = 'Global'
    symbolTable = []
    tempCont = -1
    labelCont = -1
    tempFim = ''
    tempContinue = ''
    def analyser(self, tokenList):
        ld = C3E()
        if (self.LD(ld)):
            self.resultC3E.code += ld.code
            if (self.currentToken == 'TK_EOF'):
                return True
        return False

    def LD(self, ld):
        pass