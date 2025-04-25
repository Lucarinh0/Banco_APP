import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco, senha):
        self.endereco = endereco
        self.senha = senha
        self.contas = []

    def autenticar(self, senha):
        return self.senha == senha

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome_completo, data_nascimento, cpf, endereco, senha):
        super().__init__(endereco, senha)
        self.nome_completo = nome_completo
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
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
        if valor > self._saldo:
            print("\n⚠️ Saque não autorizado: saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            print(f"\n✅ Saque de R$ {valor:.2f} realizado com sucesso.")
            return True
        else:
            print("\n⚠️ Valor inválido para saque.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n✅ Depósito de R$ {valor:.2f} efetuado com sucesso.")
            return True
        else:
            print("\n⚠️ Valor inválido para depósito.")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        saques_realizados = len([
            transacao for transacao in self.historico.transacoes
            if transacao["tipo"] == Saque.__name__
        ])
        if valor > self._limite:
            print("\n⚠️ Limite de saque excedido.")
        elif saques_realizados >= self._limite_saques:
            print("\n⚠️ Limite diário de saques atingido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
Agência:\t{self.agencia}
Número:\t\t{self.numero}
Titular:\t{self.cliente.nome_completo}
"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu_principal():
    opcoes = """\n
========= BANCO PY =========
[d] Realizar depósito
[s] Realizar saque
[e] Consultar extrato
[nu] Cadastrar novo cliente
[nc] Criar nova conta
[lc] Listar contas
[q] Sair
=> """
    return input(textwrap.dedent(opcoes))


def encontrar_cliente_por_cpf(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def selecionar_conta(cliente):
    if not cliente.contas:
        print("\n⚠️ Nenhuma conta encontrada para este cliente.")
        return None

    print("\nContas disponíveis:")
    for idx, conta in enumerate(cliente.contas):
        print(f"[{idx}] Conta {conta.numero} - Agência {conta.agencia}")

    try:
        indice = int(input("Selecione a conta pelo índice: "))
        return cliente.contas[indice]
    except (ValueError, IndexError):
        print("⚠️ Índice inválido.")
        return None


def realizar_deposito(clientes):
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("⚠️ Cliente não encontrado.")
        return

    senha = input("Digite sua senha: ")
    if not cliente.autenticar(senha):
        print("⚠️ Autenticação falhou.")
        return

    conta = selecionar_conta(cliente)
    if not conta:
        return

    try:
        valor = float(input("Valor do depósito: R$ "))
        cliente.realizar_transacao(conta, Deposito(valor))
    except ValueError:
        print("⚠️ Valor inválido.")


def realizar_saque(clientes):
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("⚠️ Cliente não encontrado.")
        return

    senha = input("Digite sua senha: ")
    if not cliente.autenticar(senha):
        print("⚠️ Autenticação falhou.")
        return

    conta = selecionar_conta(cliente)
    if not conta:
        return

    try:
        valor = float(input("Valor do saque: R$ "))
        cliente.realizar_transacao(conta, Saque(valor))
    except ValueError:
        print("⚠️ Valor inválido.")


def exibir_extrato(clientes):
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("⚠️ Cliente não encontrado.")
        return

    senha = input("Digite sua senha: ")
    if not cliente.autenticar(senha):
        print("⚠️ Autenticação falhou.")
        return

    conta = selecionar_conta(cliente)
    if not conta:
        return

    print("\n=========== EXTRATO ===========")
    if not conta.historico.transacoes:
        print("Nenhuma movimentação registrada.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("================================")


def cadastrar_cliente(clientes):
    cpf = input("CPF (apenas números): ")
    if encontrar_cliente_por_cpf(cpf, clientes):
        print("⚠️ Já existe um cliente com esse CPF.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (Rua, Número - Bairro - Cidade/UF): ")
    senha = input("Crie uma senha: ")

    novo_cliente = PessoaFisica(nome, nascimento, cpf, endereco, senha)
    clientes.append(novo_cliente)
    print("✅ Cliente cadastrado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("CPF do titular: ")
    cliente = encontrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("⚠️ Cliente não encontrado.")
        return

    nova_conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta)
    print("✅ Conta criada com sucesso!")


def listar_todas_contas(contas):
    for conta in contas:
        print("=" * 40)
        print(conta)


def iniciar_sistema_bancario():
    clientes = []
    contas = []

    while True:
        escolha = menu_principal()

        if escolha == "d":
            realizar_deposito(clientes)
        elif escolha == "s":
            realizar_saque(clientes)
        elif escolha == "e":
            exibir_extrato(clientes)
        elif escolha == "nu":
            cadastrar_cliente(clientes)
        elif escolha == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif escolha == "lc":
            listar_todas_contas(contas)
        elif escolha == "q":
            print("Obrigado por usar nosso sistema. Volte sempre!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")


iniciar_sistema_bancario()
