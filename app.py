from analyzers.Lexical import Lexical
from analyzers.Syntatic import Syntatic

def main():
    lexical  = Lexical()
    syntatic = Syntatic()
    with open('entrada.txt', 'r') as f:
        file = f.readlines()

    tokensList = lexical.analyser(file)
    tokensList = syntatic.analyser(tokensList)

    # Print list
    for token in tokensList: print(token)

if __name__=="__main__":
    main()