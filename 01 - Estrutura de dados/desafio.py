from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from textwrap import dedent


#---------------------------------Cliente-----------------------------------
class Cliente: 
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


#---------------------------------Categoriavalor------------------------------
class CategoriaConta(Enum):
    PLUS = 2500
    PREMIUM = 6000
    MASTER = 15000
    SELECT = 15001


#--------------------------------PessoaFisica-------------------------------------
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco, salario_mensal):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.salario_mensal = salario_mensal


#---------------------------------Conta----------------------------------------------
class Conta: 
    def __init__(self, numero, cliente, categoria: CategoriaConta, salario_mensal):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        self._categoria = categoria
        self._salario_mensal = salario_mensal
    
    @classmethod
    def nova_conta(cls, cliente, numero, categoria, salario_mensal):
        return cls(numero, cliente, categoria, salario_mensal)
    
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
    
    @property
    def categoria(self):
        return self._categoria.name.title()
    
    @property
    def salario_mensal(self):
        return self._salario_mensal
    
    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Operação falhou! Saldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado.")
            return True
        
        else:
            print("O valor informado é inválido.")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado.")
            return True

        print("Valor informado é inválido.")
        return False


#---------------------------------ContaCorrente-------------------------------------
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, categoria, salario_mensal, limite=500, limite_saques=3):
        super().__init__(numero, cliente, categoria, salario_mensal)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            t for t in self.historico.transacoes if t["tipo"] == Saque.__name__
        ])

        if valor > self.limite:
            print("Operação falhou! O valor excede o limite.")
        elif numero_saques >= self.limite_saques:
            print("Operação falhou! Número máximo de saques atingido.")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
Agência: {self.agencia}
Conta: {self.numero}
Titular: {self.cliente.nome}
Categoria: {self.categoria}
Salario Mensal: R$ {self.salario_mensal}
"""


#---------------------------------Historico--------------------------------------------------
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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


#---------------------------------Transacao-----------------------------------------------------
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


#---------------------------------Saque-----------------------------------------
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

#---------------------------------Deposito-----------------------------------
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


#---------------------------------OpçõesMenu---------------------------------------
def menu():
    opcoes = """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Novo Usuário
    [5] Nova Conta
    [6] Listar Contas
    [7] Sair
    """
    return input(dedent(opcoes))


def filtrar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta.")
        return None
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Valor do depósito: R$ "))
    conta = recuperar_conta_cliente(cliente)

    if conta:
        cliente.realizar_transacao(conta, Deposito(valor))


def sacar(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Valor do saque: R$ "))
    conta = recuperar_conta_cliente(cliente)

    if conta:
        cliente.realizar_transacao(conta, Saque(valor))


def exibir_extrato(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n===== EXTRATO =====")
    if not conta.historico.transacoes:
        print("Nenhuma movimentação.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['tipo']:10} R$ {t['valor']:7.2f} - {t['data']}")

    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("====================\n")


def criar_cliente(clientes):
    cpf = input("CPF: ")

    if filtrar_cliente(cpf, clientes):
        print("Já existe cliente com este CPF!")
        return

    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço: ")
    salario_mensal = float(input("Caso tenha renda, informe o valor: "))

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco, salario_mensal)
    clientes.append(cliente)

    print("Cliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    salario_mensal = float(input("Caso possua rende, informe o salario: "))
    if salario_mensal < 0:
        print("Salario invalido")
        return

    elif salario_mensal <= 2500:
        categoria = CategoriaConta.PLUS
    
    elif salario_mensal <= 6000:
        categoria = CategoriaConta.PREMIUM
    
    elif salario_mensal <= 15000:
        categoria = CategoriaConta.MASTER
    
    else:
        categoria = CategoriaConta.SELECT


    conta = ContaCorrente(numero_conta, cliente, categoria, salario_mensal)
    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("Conta criada com sucesso!")


def listar_contas(contas):
    for conta in contas:
        print("=" * 40)
        print(conta)
    if not contas:
        print("Nenhuma conta cadastrada.")


# ---------------------mainfinish-----------------------

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            criar_conta(len(contas)+1, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

