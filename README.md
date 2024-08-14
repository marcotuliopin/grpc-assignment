# grpc-assignment


### Exemplo de Execução do Make

```

make run_cli_banco arg1=Dorgival arg2=0.0.0.0:5555
make run_serv_banco arg1=5555
make run_serv_loja arg1=10 arg2=6666 arg3=Dorgival arg4=0.0.0.0:5555
make run_cli_loja arg1=Bezos arg2=0.0.0.0:5555 arg3=0.0.0.0:6666

```

### Servidor de Carteira

O programa servidor deve receber *apenas um parâmetro* de linha de comando: o número do porto a ser usado pelo servidor (inteiro, entre 2048 e 65535). Além disso, ao iniciar ele deve ler da entrada padrão uma lista de carteiras: linhas cada uma com o identificador (string) e o valor (inteiro positivo) de uma carteira, separados por um espaço. Um exemplo de conteúdo para essa entrada seria:

```

Dorgival 10
Bezos 1000000
Papai_Noel 100000

```

### Cliente de Carteira

O cliente de carteira deve receber *dois parâmetros* (strings): o primeiro será o identificador da carteira do cliente (p.ex., "Papai_Noel") e o segundo será um "string identificador de servidor" (como definido anteriormente) indicando onde o servidor está executando. Ele deve ler comandos da entrada padrão, um por linha, segundo a seguinte forma:

- S - consulta o saldo no servidor de carteiras para a carteira do cliente e escreve o valor retornado;
- O valor - faz um pedido de criação de uma ordem de pagamento no valor indicado a partir da carteira do cliente e escreve o valor de retorno fornecido pelo servidor, que será o identificador da ordem ou um código de erro;
- X opag valor string - aciona o método de transferência do servidor usando o inteiro opag como o identificador da ordem da ordem de pagamento criada anteriormente com o comando O, usando o valor dado para conferência do valor da ordem e usando o string como identificador da carteira de destino; o cliente deve escrever o valor inteiro devolvido pelo servidor ao executar o comando;
- F - dispara o procedimento de fim de execução do servidor, escreve o valor retornado e termina (somente nesse caso o cliente deve terminar a execução do servidor; se a entrada terminar sem um comando F, o servidor não deve terminar).


### Servidor de Loja

O servidor da "loja" recebe *quatro parâmetros* da linha de comando: um inteiro que será o preço do seu produto (com estoque infinito), o número do porto que ele deve utilizar para receber conexões dos clientes, um string identificador da conta do vendedor no servidor de carteiras e um "string identificador de servidor" (como descrito anteriormente) indicando onde o servidor de carteiras executa.


### Cliente de Loja

O cliente dessa segunda parte recebe como parâmetros um string identificador da conta do comprador no servidor de carteiras, um string "identificador do servidor" de carteiras e um "string identificador do servidor" do vendedor. Ao iniciar ele deve executar o método de consulta de preço da loja e escrever na saída o valor retornado. Em seguida deve ler comandos da entrada padrão, de um dos tipos a seguir:

- C - faz a compra de um produto; para isso, executa o RPC de emissão de ordem de pagamento no servidor de carteiras com o valor do produto e, se não há erros, executa a RPC de venda no servidor da loja; escreve na saída uma linha com o valor de retorno do procedimento de ordem de serviço e, se não houver erro na primeira operação, na linha seguinte escreve o valor de retorno da operação de venda da loja;
- T - dispara a operação de término do servidor da loja, escreve na saída padrão os dois valor de retorno recebidos (mesma linha, separados por espaço) e termina a execução; se a entrada terminar sem um comando T, o cliente deve terminar sem acionar o fim dos servidores.