from analyzers.Lexical import Lexical
from analyzers.Syntatic import Syntatic
import sys, getopt
import keyboard

def main(argv):

    USAGE = """
    c3e.py [OPTIONS]
        -i --ifile Arquivo .c de entrada
        -o --ofile Arquivo de saída
        -I --interactive Modo interativo
        -h --help Mostra esse menu
    """

    inputfile = ''
    outputfile = ''
    interactive = True

    try:
        opts, _ = getopt.getopt(argv,"Ihi:o:",["interactive","help","ifile=","ofile="])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg.lstrip()
            interactive = False
        elif opt in ("-o", "--ofile"):
            outputfile = arg.lstrip()
        elif opt in ("-I", "--interactive"):
            interactive = interactive and True
 

    file = ""
    if not interactive:
        with open(inputfile, 'r') as f:
            file = f.readlines()
            doAnalisis(file,outputfile)
    else:
        while True:
            file = getUserInput()
            doAnalisis(file,outputfile)
            resp = input("Continuar ? s/n ")
            if resp == 's':
                continue
            break


def doAnalisis(file,outputfile):
    lexical  = Lexical()
    tokensList = lexical.analyser(file)
    syntatic = Syntatic(tokensList)

    print("Análise Léxica:")
    printLex(tokensList)

    result = syntatic.analyser()

    if outputfile != '':
        if result:
            with open(outputfile,'w') as o:
                o.write(syntatic.resultCode.code)
                o.close
    else:
        print("\nCodigo C3E:")
        if result:            
            print(syntatic.resultCode.code)
        else:
            print("Não foi possível gerar o código C3E")

def printLex(lex):
    for l in lex:
        print(l)

def getUserInput():
    editing = True
    ret = []
    def done():
        nonlocal editing
        editing = False
    
    keyboard.add_hotkey('ctrl+enter',done)
    print("Lendo entrada, ctrl+enter para terminar")
    while editing:
        ret.append(input() + '\n')
    
    keyboard.clear_all_hotkeys()

    return ret


if __name__ == "__main__":
    main(sys.argv[1:])