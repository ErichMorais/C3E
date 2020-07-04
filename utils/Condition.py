class Condition(object):
    def __init__(self):
        pass

    def isNewLine(self, char):
        return char == '\n'
    
    def isComment(self, line):
        return line[0] == '/' and line[1] == '/'
    
    def isWhiteSpace(self, char):
        return char == ' ' or  char == ''

    def isHashTag(self, char):
        return char == '#'
    
    def isOpenClose(self, char):
        return ((char == '{' or char == '}') or 
                (char == '(' or char == ')') or 
                (char == '[' or char == ']') or 
                (char == ',' or char == ':'))
    
    def isSemiColon(self, char):
        return char == ';'
    
    def isExclamation(self, char):
        return char == '!'
    
    def isEqual(self, char):
        return char == '='
    
    def isAndBitwise(self, char):
        return char == '&'
    
    def isOrBitwise(self, char):
        return char == '|'
    
    def isXorBitwise(self, char):
        return char == '^'

    def isPercent(self, char):
        return char == '%'
    
    def isPlus(self, char):
        return char == '+'
    
    def isMinus(self, char):
        return char == '-'

    def isLess(self, char):
        return char == '<'

    def isGreater(self, char):
        return char == '>'

    def isSlash(self, char):
        return char == '/'

    def isStar(self, char):
        return char == '*'
    
    def isDot(self, char):
        return char == '.'

    def isNum(self, char):
        return char in [f'{i}' for i in range(10)]
    
    def isChar(self, char):
        return ((char >= 'a' and char <= 'z') or 
                (char >= 'A' and char <= 'Z') or char == '_')
