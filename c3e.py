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
            inputfile = arg
            interactive = False
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-I", "--interactive"):
            interactive = interactive and True
 

    lexical  = Lexical()

    if not interactive:
        with open(inputfile, 'r') as f:
            file = f.readlines()
    else:
        file = getUserInput()

    tokensList = lexical.analyser(file)
    syntatic = Syntatic(tokensList)

    printLex(tokensList)

    result = syntatic.analyser()

    if result:
        if outputfile != '':
            with open(outputfile,'w') as o:
                o.write(syntatic.resultCode)
                o.close
        else:
            print(syntatic.resultCode)


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
        ret.append(input())
    
    return ret


if __name__ == "__main__":
    main(sys.argv[1:])