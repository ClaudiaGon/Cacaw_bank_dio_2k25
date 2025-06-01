from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self, conta):
        self.contas.append(conta)
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print('\nOperação FALHOU! Você não tem saldo suficiente, Escolha outro valor.')
        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True
        else:
            print('Operação falhou, O valor informado é invalido')
        return False
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Deposito realizado com sucesso!')
        else:
            print('Operação FALHOU! O valo informado é inválido. Tente Novamente.')
            return False
        return True
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        if excedeu_limite:
            print('Operação Falhou! O valor do saque exece o seu limite. Tente novaente com um valor menor.')
        if excedeu_saques:
            print('Operação Falhou!! Números máximo de saques excedido!!')
        else:
            return super().sacar(valor)
        return False
    def __str__(self):
        return textwrap.dedent(f"""\
        Agência: {self.agencia}
        C/C: {self.numero}
        Títular: {self.cliente.nome}
        """)
class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%s"),
            }
        )
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta):
        pass
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
def escreva(msg):
    tam = len(msg) + 5
    print('-' * tam)
    print(f'  {msg}')
    print('-' * tam)
def menu():
    menu = """
    Escolha uma das opções abaixo:
    [NU] NOVO USÚARIO
    [NC] NOVA CONTA
    [LC] LISTAR CONTAS
    [D] DEPOSITAR
    [S] SACAR
    [E] EXTRATO
    [Q] SAIR
    Informe aqui a opção escolhida: """
    return input(textwrap.dedent(menu))
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        escreva('Cliente não possui conta!')
        return None

    for i, conta in enumerate(cliente.contas, start=1):
        print(f"{i}. {conta}")
    indice = int(input("Escolha o número da conta: ")) + 1
    return cliente.contas[indice] if 0 <= indice < len(cliente.contas) else None

def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        escreva('Cliente não encontrado!')
        return
    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)
def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        escreva('Cliente não encontrado!')
        return
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)
def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        escreva("Cliente não encontrado!")
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    escreva('EXTRATO')
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas mocimentações na conta."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
        escreva(extrato)
        escreva(f"Saldo: \n\tR$ {conta.saldo:.2f}")
def criar_cliente(clientes):
    cpf = input('Informe o CPF (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        escreva('Já existe cliente com esse CPF!')
        return
    nome = input('Informe o nome completo do cliente:')
    data_nascimento = input('Informe a data de nascimento do cliente: (dd-mm-aaaa): ')
    endereco = input('Informe o endereço completo do cliente (logadouro - bairro - cidade /sigla estado)')
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    escreva('Cliente criado com sucesso!')
def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        escreva('Cliente não encontrado, Tente Novamente. Fluxo encerrado')
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    escreva('Conta criada com Sucesso!')
def listar_contas(contas):
    for conta in contas:
        escreva(textwrap.dedent(str(conta)))
def main():
    clientes = []
    contas = []
    while True:
        opcao = menu().upper().strip()
        if opcao == "D":
            depositar(clientes)
        elif opcao == "S":
            sacar(clientes)
        elif opcao == "E":
            exibir_extrato(clientes)
        elif opcao == "NU":
            criar_cliente(clientes)
        elif opcao == "NC":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "LC":
            listar_contas(contas)
        elif opcao == "Q":
            break
        else:
            escreva('Operação invalida, por favor selecione novamente uma opcao valida.')
escreva("Cacaw Bank")
main()