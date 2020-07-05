from analyzers.Lexical import Lexical
from analyzers.Syntatic import Syntatic

def main():
    lexical  = Lexical()
    with open('./archives/entrada_2.txt', 'r') as f:
        file = f.readlines()

    tokensList = lexical.analyser(file)
    syntatic = Syntatic(tokensList)
    result = syntatic.analyser()

    # Print list
    #for token in tokensList: print(token)

if __name__=="__main__":
    main()