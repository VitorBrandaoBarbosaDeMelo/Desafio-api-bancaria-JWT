import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import json
import os

# --- Constantes e Configurações ---
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTAS = "contas.json"
AGENCIA = "0001"
LIMITE_CONTAS_POR_USUARIO = 10
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500

# 1. CLASSES DE MODELAGEM DE NEGÓCIO

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        return transacao.registrar(conta) # Retorna o sucesso da transação
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def to_dict(self):
        return {"nome": self.nome, "data_nascimento": self.data_nascimento, "cpf": self.cpf, "endereco": self.endereco}

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = AGENCIA
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero): return cls(numero, cliente)

    # Propriedades Condensadas
    @property
    def saldo(self): return self._saldo
    @property
    def numero(self): return self._numero
    @property
    def agencia(self): return self._agencia
    @property
    def cliente(self): return self._cliente
    @property
    def historico(self): return self._historico

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def to_dict(self):
        return {"numero": self.numero, "cpf_cliente": self.cliente.cpf, "saldo": self.saldo, "historico_transacoes": self.historico.transacoes}

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=LIMITE_VALOR_SAQUE, limite_saques=LIMITE_SAQUES):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        num_saques = len([t for t in self.historico.transacoes if t["tipo"] == Saque.__name__])
        
        if valor > self._limite:
            print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}. @@@")
        elif num_saques >= self._limite_saques:
            print(f"\n@@@ Operação falhou! Número máximo de {self._limite_saques} saques excedido. @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""Agência:\t{self.agencia}\nC/C:\t\t{self.numero}\nTitular:\t{self.cliente.nome}\nSaldo:\t\tR$ {self.saldo:.2f}"""
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({"limite": self._limite, "limite_saques": self._limite_saques, "tipo_conta": "ContaCorrente"})
        return base_dict

class Historico:
    def __init__(self): self._transacoes = []
    
    @property
    def transacoes(self): return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
    
    def gerar_extrato(self):
        return "\n".join([f"{t['tipo']} ({t['data']}):\n\tR$ {t['valor']:.2f}" for t in self._transacoes]) or "Não foram realizadas movimentações."

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self): pass

    @abstractclassmethod
    def registrar(self, conta): pass

class Saque(Transacao):
    def __init__(self, valor): self._valor = valor
    @property
    def valor(self): return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print("\n=== Saque realizado com sucesso! ===")
            return True
        return False

class Deposito(Transacao):
    def __init__(self, valor): self._valor = valor
    @property
    def valor(self): return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        return False

# =========================================================================
# 2. FUNÇÕES DE PERSISTÊNCIA
# =========================================================================

def _carregar(arquivo, default=[]):
    if not os.path.exists(arquivo): return default
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            return json.loads(conteudo) if conteudo else default
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"\n⚠️ ERRO DE LEITURA DO ARQUIVO {arquivo}: {e}")
        return default

def _salvar(arquivo, dados_serializaveis):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_serializaveis, f, indent=4)

def carregar_usuarios():
    usuarios_s = _carregar(ARQUIVO_USUARIOS)
    return [PessoaFisica(nome=u['nome'], data_nascimento=u['data_nascimento'], cpf=u['cpf'], endereco=u['endereco']) for u in usuarios_s]

def salvar_usuarios(clientes):
    _salvar(ARQUIVO_USUARIOS, [c.to_dict() for c in clientes if isinstance(c, PessoaFisica)])

def carregar_contas(clientes):
    contas_s = _carregar(ARQUIVO_CONTAS)
    contas_obj = []
    for c_s in contas_s:
        cliente = filtrar_cliente(c_s.get("cpf_cliente"), clientes)
        if not cliente: continue
        
        conta = ContaCorrente(
            numero=c_s['numero'], cliente=cliente, 
            limite=c_s.get('limite', LIMITE_VALOR_SAQUE), limite_saques=c_s.get('limite_saques', LIMITE_SAQUES)
        )
        conta._saldo = c_s['saldo']
        conta.historico._transacoes = c_s.get('historico_transacoes', [])
        cliente.adicionar_conta(conta)
        contas_obj.append(conta)
    return contas_obj

def salvar_contas(contas):
    _salvar(ARQUIVO_CONTAS, [c.to_dict() for c in contas])
        
# =========================================================================
# 3. FUNÇÕES DE SERVIÇO/API
# =========================================================================

def menu():
    m = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(m))

def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    return cliente.contas[0] # Retorna a primeira (FIXME: não permite escolha)

def _executar_transacao(clientes, contas, TransacaoCls):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input(f"Informe o valor do {TransacaoCls.__name__.lower()}: "))
    transacao = TransacaoCls(valor)
    
    if cliente.realizar_transacao(conta, transacao):
        salvar_contas(contas)

def depositar(clientes, contas):
    _executar_transacao(clientes, contas, Deposito)

def sacar(clientes, contas):
    _executar_transacao(clientes, contas, Saque)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    print(f"Conta: {conta.agencia}-{conta.numero} | Cliente: {conta.cliente.nome}")
    print("-----------------------------------------")
    print(conta.historico.gerar_extrato())
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    clientes.append(PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco))
    salvar_usuarios(clientes)
    print("\n=== Cliente criado com sucesso e salvo! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    if len(cliente.contas) >= LIMITE_CONTAS_POR_USUARIO:
        print(f"\n@@@ Usuário já possui o limite de {LIMITE_CONTAS_POR_USUARIO} contas cadastradas. @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    
    contas.append(conta)
    cliente.adicionar_conta(conta)
    salvar_contas(contas)
    print("\n=== Conta criada com sucesso e salva! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# =========================================================================
# 4. FUNÇÃO PRINCIPAL
# =========================================================================

def main():
    clientes = carregar_usuarios()
    contas = carregar_contas(clientes)

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes, contas)
        elif opcao == "s":
            sacar(clientes, contas)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            criar_conta(len(contas) + 1, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema bancário. Até mais!")
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()


   # Titulo: Sistema bancário que combina a estrutura de Programação Orientada a Objetos (POO) 
   # com a persistência de dados (JSON) para criar um sistema bancário modular.

###funcionalidades e estruturas do código ###
    # Funcionalidades:
    # - Criação e gerenciamento de clientes e contas bancárias.
    # - Realização de transações como depósitos e saques.
    # - Geração de extratos detalhados das contas.
    # - Persistência de dados usando arquivos JSON para armazenar informações de clientes e contas.
    
    # Estruturas do código:
    # - Classes para modelar clientes, contas, transações e histórico.
    # - Funções para carregar e salvar dados em arquivos JSON.
    # - Funções de serviço para interagir com o usuário e executar operações bancárias.
    # - Uma função principal que orquestra o fluxo do programa, apresentando um menu interativo ao usuário.
