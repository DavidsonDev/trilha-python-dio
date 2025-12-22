import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


# ================= CLIENTES =================
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# ================= CONTAS =================
class Conta:
    AGENCIA_PADRAO = "0001"

    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
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
        return self.AGENCIA_PADRAO

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor):
        if valor <= 0:
            return False, "Valor inválido para depósito"
        self._saldo += valor
        return True, "Depósito realizado com sucesso"

    def sacar(self, valor):
        if valor <= 0:
            return False, "Valor inválido para saque"
        if valor > self._saldo:
            return False, "Saldo insuficiente"
        self._saldo -= valor
        return True, "Saque realizado com sucesso"


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        saques_realizados = sum(
            1 for t in self.historico.transacoes if t["tipo"] == "Saque"
        )

        if valor > self.limite:
            return False, "Saque excede o limite permitido"
        if saques_realizados >= self.limite_saques:
            return False, "Limite diário de saques atingido"

        return super().sacar(valor)

    def __str__(self):
        return f"""
Agência:\t{self.agencia}
Conta:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""


# ================= HISTÓRICO =================
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
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


# ================= TRANSAÇÕES =================
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
        sucesso, _ = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso, _ = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ================= FUNÇÕES AUXILIARES =================
def menu():
    texto = """
    ================ MENU ================
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova conta
    [5] Listar contas
    [6] Novo cliente
    [0] Sair
    => """
    return input(textwrap.dedent(texto))


def buscar_cliente(clientes):
    cpf = input("CPF: ")
    cliente = next((c for c in clientes if c.cpf == cpf), None)
    if not cliente:
        print("-------------- Cliente não encontrado! --------------")
    return cliente


def obter_conta(cliente):
    if not cliente.contas:
        print("-------------- Cliente não possui conta! --------------")
        return None
    return cliente.contas[0]


def executar_transacao(clientes, transacao_cls):
    cliente = buscar_cliente(clientes)
    if not cliente:
        return

    valor = float(input("Valor: "))
    conta = obter_conta(cliente)
    if not conta:
        return

    transacao = transacao_cls(valor)
    sucesso, mensagem = (
        conta.depositar(valor)
        if isinstance(transacao, Deposito)
        else conta.sacar(valor)
    )

    print(f"\n-------------- {mensagem} --------------")
    if sucesso:
        cliente.realizar_transacao(conta, transacao)


# ================= OPERAÇÕES =================
def exibir_extrato(clientes):
    cliente = buscar_cliente(clientes)
    if not cliente:
        return

    conta = obter_conta(cliente)
    if not conta:
        return

    print("\n=========== EXTRATO ===========")
    if not conta.historico.transacoes:
        print("Nenhuma movimentação registrada.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['tipo']} | R$ {t['valor']:.2f} | {t['data']}")

    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("===============================")


def criar_cliente(clientes):
    cpf = input("CPF: ")
    if any(c.cpf == cpf for c in clientes):
        print("-------------- CPF já cadastrado! --------------")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento: ")
    endereco = input("Endereço: ")

    clientes.append(PessoaFisica(nome, nascimento, cpf, endereco))
    print("=== Cliente criado com sucesso! ===")


def criar_conta(clientes, contas):
    cliente = buscar_cliente(clientes)
    if not cliente:
        return

    numero = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente, numero)

    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 40)
        print(conta)


# ================= MAIN =================
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            executar_transacao(clientes, Deposito)
        elif opcao == "2":
            executar_transacao(clientes, Saque)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            criar_conta(clientes, contas)
        elif opcao == "5":
            listar_contas(contas)
        elif opcao == "6":
            criar_cliente(clientes)
        elif opcao == "0":
            break
        else:
            print("-------------- Opção inválida! --------------")


main()
