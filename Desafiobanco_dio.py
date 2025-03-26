import textwrap

def escreva(msg):
    tam = len(msg) + 5
    print('-' * tam)
    print(f'  {msg}')
    print('-' * tam)

def menu():
    menu = escreva("Cacaw's Bank")
    menu = """Olá, aqui estão as opções dispiniveis
    [D] DEPOSITAR
    [S] SACAR
    [E] EXTRATO
    [NC] NOVA CONTA
    [LC] LISTAR CONTAS
    [NU] NOVO USUARIO
    [Q] SAIR
    A opçõo escolhida é:
    """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Deposito: R$ {valor:.2f}\n'
        print(f'Deposito realizado com sucesso. O valor R${valor}; Foi depositado em sua conta')
    else:
        print('Operação FALHOU! O valor informado  é inválido.')

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
     excedeu_saldo = valor >saldo
     excedeu_limite = valor > limite
     excedeu_saque = numero_saques > limite_saques
     if excedeu_saldo:
        print('\nOperação FALHOU! Você não tem saldo suficiente, Escolha outro valor.')

     elif excedeu_limite:
          print('\nOperação FALHOU! O valor do saque excede o limite.')

     elif excedeu_saque:
        print('\nOperação FALHOU! Número maximo de saques atigindo.')

     elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R$ {valor:.2f}\n'
        numero_saques += 1
        escreva('Saque realizado com Sucesso!')
        print(f'O valor atual da sua aconta agora é: R${saldo}')
     else:
        print('\nOperação FALHOU!! O valor informado é invalido.')
     return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
        escreva("EXTRATO")
        print('Não foram realizadas movimentações.' if not extrato else extrato)
        print(f'\nSaldo: R$ {saldo:.2f}')
        print('-' * 30)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('Já existe usuario com este CPF!, Tente Novamente')
        return
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaa): ')
    endereço = input('Informe o Endereço completo: ')

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço} )
    escreva('Usuaio criado com sucesso!')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf ]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        escreva('Conta criada com SUCESSO!')
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    escreva('Usuario Não encontrado, tente novamente.')

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agéncia:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 30)
        print(textwrap.dedent(linha))

def principal():
    AGENCIA = '0001'
    LIMITE_SAQUE = 3

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opção = menu().upper().strip()

        if opção == 'D': #DEPOSITO
            valor = float(input('Informe o valor do depósito: '))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opção == 'S': #SAQUE
            valor = float(input('informe o valor do saque:' ))
            saldo, extrato = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUE
            )
        elif opção == 'E': #EXTRATO
             exibir_extrato(saldo, extrato=extrato)

        elif opção == 'NU': #NOVO USUARIO
             criar_usuario(usuarios)

        elif opção == "NC": #NOVA CONTA
            #numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta :
                contas.append(conta)
                numero_conta += 1

        elif opção == "LC":
            listar_contas(contas)

        elif opção == "Q":
            escreva('Tenha um Exelente dia')
            break
        else:
            print("Operação inválida, por favor selecioe novamente a operação desejada.")

principal()