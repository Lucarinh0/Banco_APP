import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

# -------- CLASSES PRINCIPAIS --------

class Cliente:
    def __init__(self, nome, cpf, nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        try:
            transacao.registrar(conta)
        except Exception as e:
            print(f"Erro ao realizar transação: {e}")

    def adicionar_conta(self, conta):
        self.contas.append(conta)


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
            print("Saldo insuficiente.")
            return False
        if valor <= 0:
            print("Valor inválido.")
            return False

        self._saldo -= valor
        print("Saque realizado com sucesso.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido.")
            return False
        self._saldo += valor
        print("Depósito realizado com sucesso.")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        saques = [t for t in self.historico.transacoes if t["tipo"] == "Saque"]
        if len(saques) >= self._limite_saques:
            print("Limite de saques excedido.")
            return False
        if valor > self._limite:
            print("Saque acima do limite permitido.")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""\
Agência: {self.agencia}
Número da Conta: {self.numero}
Titular: {self.cliente.nome}
"""


# -------- HISTÓRICO E TRANSAÇÕES --------

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
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


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


# -------- FUNÇÕES DE INTERFACE COM USUÁRIO --------

def menu():
    menu = """\n=========== MENU ===========
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q] Sair
=> """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui contas.")
        return None
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    try:
        valor = float(input("Valor do depósito: "))
    except ValueError:
        print("Valor inválido. Use apenas números.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    try:
        valor = float(input("Valor do saque: "))
    except ValueError:
        print("Valor inválido. Use apenas números.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n====== EXTRATO ======")
    if not conta.historico.transacoes:
        print("Sem movimentações.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("======================")


def criar_cliente(clientes):
    cpf = input("CPF (somente números): ").strip()
    if not cpf or not cpf.isdigit():
        print("CPF inválido.")
        return

    if filtrar_cliente(cpf, clientes):
        print("Já existe cliente com este CPF.")
        return

    nome = input("Nome completo: ").strip()
    nascimento = input("Data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Endereço: ").strip()

    if not nome or not nascimento or not endereco:
        print("Todos os campos são obrigatórios.")
        return

    novo_cliente = Cliente(nome, cpf, nascimento, endereco)
    clientes.append(novo_cliente)
    print("Cliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("Conta criada com sucesso!")


def listar_contas(contas):
    if not contas:
        print("Nenhuma conta registrada.")
        return

    for conta in contas:
        print("=" * 30)
        print(conta)


# -------- EXECUÇÃO PRINCIPAL --------

def main():
    clientes = []
    contas = []

    while True:
        try:
            opcao = menu().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando sistema.")
            break

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            criar_conta(len(contas) + 1, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida.")

main()
