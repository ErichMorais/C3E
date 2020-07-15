

TOKENS = {
        "id": "TK_ID",
        "$": "TK_EOF",

        #Types
        "void": "TK_VOID",
        "int": "TK_INT",
        "char": "TK_CHAR",
        "float": "TK_FLOAT",
        "double": "TK_DOUBLE",
        "const_int": "TK_CONST_INT",
        "const_real": "TK_CONST_REAL",

        #Reserverd Words
        "while": "TK_WHILE",
        "else": "TK_ELSE",
        "if": "TK_IF",
        "break": "TK_BREAK",
        "for": "TK_FOR",
        "return": "TK_RETURN",
        "continue": "TK_CONTINUE",
        "do": "TK_DO",

        #Ops
        ",": "TK_COMMA",
        ".": "TK_DOT",
        "'": "TK_BACKQUOTE",
        "(": "TK_LEFTPAR",
        ")": "TK_RIGHTPAR",
        "{": "TK_LEFTBRAC",
        "}": "TK_RIGHTBRAC",
        "!": "TK_NOT",
        "!=": "TK_NOTEQUAL",
        ":": "TK_COLON",
        ";": "TK_SEMICOLON",
        "+": "TK_PLUS",
        "+=": "TK_PLUSEQUAL",
        "-": "TK_MINUS",
        "-=": "TK_MINEQUAL",
        "*": "TK_STAR",
        "*=": "TK_STAREQUAL",
        "/": "TK_SLASH",
        "/=": "TK_SLASHEQUAL",
        "|": "TK_LOGICOR",
        "||": "TK_OR",
        "&": "TK_LOGICAND",
        "&&": "TK_AND",
        "<": "TK_LESS",
        "<=": "TK_LESSEQUAL",
        ">": "TK_GREATER",
        ">=": "TK_GREATEREQUAL",
        "=": "TK_EQUAL",
        "==": "TK_EQUALEQUAL",
        "%": "TK_PERCENT",
        "%=": "TK_PERCENTEQUAL",
        "^": "TK_CIRCUMFLEX"
}