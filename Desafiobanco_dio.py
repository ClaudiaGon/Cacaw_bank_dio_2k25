print('-' * 30)
print('{:^30}'.format("Cacaw's Bank"))
print('-' * 30)
menu = """
[D] DEPOSITAR
[S] SACAR
[E] EXTRATO
[Q] SAIR
"""
print()
saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUE = 3
while True:
    opção = str(input(f'Olá, aqui estão as opções dispiniveis {menu}A opçõo escolhida é: ')).upper().strip()
    if opção == 'D': #DEPOSITO
        valor = float(input('Informe o valor do depósito: '))
        if valor > 0:
            saldo += valor
            extrato += f'Deposito: R$ {valor:.2f}\n'
            print(f'O valor R${valor}, foi depositado em sua conta')
        else:
            print('Operação FALHOU! O valor informado  é inválido.')
    elif opção == 'S': #SAQUE
        valor = float(input('informe o valor do saque:' ))
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        exedeu_saque = numero_saques >= LIMITE_SAQUE
        if excedeu_saldo:
            print('\nOperação FALHOU! Você não tem saldo suficiente, Escolha outro valor.')
        elif excedeu_limite:
            print('\nOperação FALHOU! O valor do saque excede o limite.')
        elif exedeu_saque:
            print('\nOperação FALHOU! Número maximo de saques atigindo.')
        elif valor > 0:
            saldo -= valor
            extrato += f'Saque: R$ {valor:.2f}\n'
            numero_saques += 1
            print(f'O valor atual da sua aconta agora é: R${saldo}')
        else:
            print('\nOperação FALHOU!! O valor informado é invalido.')
    elif opção == 'E': #EXTRATO
        print('-' * 30)
        print('{:^30}'.format("EXTRATO"))
        print('-' * 30)
        print('Não foram realizadas movimentações.' if not extrato else extrato)
        print(f'\nSaldo: R$ {saldo:.2f}')
        print('-' * 30)
    elif opção == 'Q': #SAIR
        print('Tenha um Otimo dia!')
        break
    else:
        print('\nOperação Invalida, por favor selecione uma das opções listadas.')
        