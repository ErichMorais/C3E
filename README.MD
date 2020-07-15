# Gerador Código de 3 endereços
Trabalho referente a disciplina de compiladores(SIS0454A) na Universidade de Caxias do Sul

## Uso

No modo em que é feita a leitura do arquivo (não-iterativo) é necessario inserir o local de execução, como demonstra os exemplos:
### Windows
$ python3 c3e.py -i archives/entrada.txt
### Linux
Será necessario instalar a lib Keyboard e executar o terminal como adminstrador (sudo)
$ pip3 install keyboard
$ sudo python3 c3e.py -i archives/entrada.txt

Para utilizar o programa em modo Iterativo(escrever o código de entrada), deve se utilizar o parametro -I
$ python3 c3e.py -I
$ *(Código..)*
$ Ctrl+Enter para executar

Autores: Erich Morais e William Steffler