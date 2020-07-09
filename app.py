from analyzers.Lexical import Lexical
from analyzers.Syntatic import Syntatic

def main():
    lexical  = Lexical()
    with open('./archives/entrada_2.txt', 'r') as f:
        file = f.readlines()

    tokensList = lexical.analyser(file)
    syntatic = Syntatic(tokensList)
    result = syntatic.analyser()

    if(result):
        print(syntatic.currentToken())
    # with open('./archives/saida_2.txt', 'w') as f:
    # # Print list
    #     for token in tokensList: f.write(str(token)+'\n')
    #     f.close()

if __name__ == "__main__":
    main()