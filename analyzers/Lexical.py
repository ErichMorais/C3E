from utils.Condition import Condition
from utils.Token import Token

class Lexical(object):
    def __init__(self):
        pass
        
    def analyser(self, file):    
        flagChangePosition = flagGoNextCol = False
        cond = Condition()
        tokens = []
        jmpCont = 0
        for row, line in enumerate(file):
            for col, char in enumerate(line):
                if flagGoNextCol: 
                    flagGoNextCol = False
                    continue
                if  flagChangePosition:
                    jmpCont = jmpCont - 1    
                    if(jmpCont <= 1):
                        flagChangePosition = False
                    continue

                if cond.isNewLine(char): continue
                if cond.isWhiteSpace(char): continue
                if cond.isHashTag(char): break

                if cond.isComment(line): continue
                if cond.isOpenClose(char) or cond.isSemiColon(char):
                    tokens.append(Token(char, row, col))
                    continue
                
                nextChar = line[col+1]
                if cond.isExclamation(char) and cond.isEqual(nextChar):
                    if cond.isEqual(nextChar):
                        tokens.append(Token(char+nextChar, row, col))
                        flagGoNextCol = True
                        continue
                    tokens.append(Token(char + nextChar, row, col))
                    continue

                if (cond.isEqual(char) or cond.isAndBitwise(char) or cond.isOrBitwise(char) or
                    cond.isXorBitwise(char) or cond.isPercent(char)):
                    if cond.isEqual(nextChar):
                        tokens.append(Token(char+nextChar, row, col))
                        flagGoNextCol = True                
                        continue
                    tokens.append(Token(char, row, col))
                    continue            
                
                if cond.isAndBitwise(char) or cond.isAndBitwise(nextChar):
                    tokens.append(Token(char + nextChar, row, col))
                    flagGoNextCol = True
                    continue
            
                if cond.isOrBitwise(char) and cond.isOrBitwise(nextChar):
                    tokens.append(Token(char + nextChar, row, col))
                    flagGoNextCol = True
                    continue

                if cond.isPlus(char) or cond.isMinus(char):
                    if ((cond.isPlus(char) and cond.isPlus(nextChar)) or 
                        (cond.isMinus(char) and cond.isMinus(nextChar))):
                        tokens.append(Token(char + nextChar, row, col))
                        flagGoNextCol = True
                        continue
                    elif cond.isEqual(nextChar):
                        tokens.append(Token(char + nextChar, row, col))
                        flagGoNextCol = True
                        continue
                    tokens.append(Token(char, row, col))
                    continue

                if (cond.isStar(char) or cond.isSlash(char) or 
                    cond.isLess(char) or cond.isGreater(char)):
                    if cond.isEqual(nextChar):
                        tokens.append(Token(char+nextChar, row, col))
                        flagGoNextCol = True                
                        continue
                    tokens.append(Token(char, row, col))
                    continue    
                    
                if cond.isNum(char):
                    flagDot = False
                    jmpCont = col + 1
                    while(cond.isNum(nextChar)):
                        char = char + nextChar
                        jmpCont = jmpCont + 1 
                        nextChar = line[jmpCont]
                        flagChangePosition = True           
                    if(cond.isDot(nextChar)):
                        char = char + nextChar
                        jmpCont = jmpCont + 1 
                        nextChar = line[jmpCont]
                        flagChangePosition = True
                        flagDot = True
                    while(cond.isNum(nextChar)):
                        char = char + nextChar
                        jmpCont = jmpCont + 1 
                        nextChar = line[jmpCont]
                        flagChangePosition = True
                    jmpCont = jmpCont - col
                    if flagDot:
                        tokens.append(Token(float(char), row, col))
                    else:
                        tokens.append(Token(int(char), row, col))
                    continue

                if cond.isChar(char):
                    jmpCont = col + 1
                    while(cond.isChar(nextChar)):
                        char = char + nextChar
                        jmpCont = jmpCont + 1 
                        nextChar = line[jmpCont]
                        flagChangePosition = True
                    jmpCont = jmpCont - col
                    tokens.append(Token(char, row, col))
                    continue

        tokens.append(Token("$", row, col))
        return tokens            
        # Print list
        #for token in tokens: print(token)

