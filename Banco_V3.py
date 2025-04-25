from abc import ABC

class cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._conta = []

    def realizar_transacao(self, Conta, transacao):
        Transacaoes.Registrar_conta(conta)

    def adicionar_conta(self, conta: "Contas()"):
        pass

class Contas:
    def __init__(self, saldo, numero, agencia, cliente, historico):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    def saldo (self):
        return self._saldo

    def nova_conta_cliente(self):
        pass

    def sacar(self, valor):
        if valor >= 0 and self._saldo >= valor:
            self._saldo -= valor
            Historico()

    def depositar(self):
        pass

class Conta_Coreente(Contas):
    pass

class Transacaoes(ABC):
    def Registrar_conta(conta):
        pass

class Historico:
    def adicionar_transacao(transacao: Transacaoes):
        pass

class depoisoto(Transacaoes):
    pass

class saques(Transacaoes):
    pass

class Pessoa_Fisica(cliente):
    pass

