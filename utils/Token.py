from utils.Tokens import TOKENS

class Token(object):
    def __init__(self, lexeme, row, col):
        self.row = row
        self.col = col
        
        if lexeme in TOKENS:
            self.lexeme = lexeme
            self.token  = TOKENS[self.lexeme]
        else:
            if isinstance(lexeme, str): #String
                self.lexeme = lexeme
                self.token  = TOKENS['id']
            elif isinstance(lexeme, int): #inteiro
                self.lexeme = int(lexeme)
                self.token = TOKENS['const_int']
            elif isinstance(lexeme, float): #float
                self.lexeme = float(lexeme)
                self.token = TOKENS['const_real']
    
    def __repr__(self):
        return f'lexema: {self.lexeme}, row: {self.row}, col: {self.col}, token: {self.token}'